#!/usr/bin/env python3
"""Inventory INE DSpace ZIP packages without downloading their payloads.

The INE repository exposes byte-range requests.  This script reads only each
ZIP central directory, which is enough to enumerate every contained path,
compressed size and uncompressed size while preserving the official URL.
"""

from __future__ import annotations

import argparse
import csv
from http.client import RemoteDisconnected
import json
import re
import ssl
import struct
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import certifi


EOCD_SIGNATURE = b"PK\x05\x06"
CENTRAL_SIGNATURE = b"PK\x01\x02"
USER_AGENT = "Mozilla/5.0 (compatible; PEF-2024-document-inventory/1.0)"


class BitstreamParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.archives: list[dict[str, str]] = []
        self._href: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href and "/bitstream/handle/" in href and href.lower().endswith(".zip"):
            self._href = urljoin(self.base_url, href)

    def handle_data(self, data: str) -> None:
        if not self._href:
            return
        label = " ".join(data.split())
        if label:
            match = re.match(r"(.+?\.zip)(?:\s+\(([^)]+)\))?$", label, re.I)
            self.archives.append(
                {
                    "archive_name": match.group(1) if match else label,
                    "display_size": match.group(2) if match and match.group(2) else "",
                    "archive_url": self._href,
                }
            )
            self._href = None


def request_bytes(url: str, byte_range: str | None = None) -> bytes:
    headers = {"User-Agent": USER_AGENT}
    if byte_range:
        headers["Range"] = f"bytes={byte_range}"
    context = ssl.create_default_context(cafile=certifi.where())
    for attempt in range(3):
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=120, context=context) as response:
                return response.read()
        except (HTTPError, URLError, RemoteDisconnected, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(1 + attempt)
    raise RuntimeError("unreachable")


def remote_size(url: str) -> int:
    context = ssl.create_default_context(cafile=certifi.where())
    for attempt in range(3):
        request = Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
        try:
            with urlopen(request, timeout=120, context=context) as response:
                content_length = response.headers.get("Content-Length")
                if content_length:
                    return int(content_length)
                raise ValueError("HEAD response omitted Content-Length")
        except (
            HTTPError,
            URLError,
            RemoteDisconnected,
            TimeoutError,
            ValueError,
        ):
            if attempt == 2:
                raise
            time.sleep(1 + attempt)
    raise RuntimeError("unreachable")


def list_archives(handle_url: str) -> list[dict[str, str]]:
    parser = BitstreamParser(handle_url)
    parser.feed(request_bytes(handle_url).decode("utf-8", errors="replace"))
    return parser.archives


def remote_zip_entries(
    url: str,
) -> tuple[int, list[dict[str, int | str]]]:
    archive_size = remote_size(url)
    if archive_size > 2_147_483_647:
        raise OverflowError(
            "The INE range endpoint rejects offsets above signed 32-bit"
        )
    tail_start = max(0, archive_size - 131072)
    tail = request_bytes(url, f"{tail_start}-{archive_size - 1}")
    eocd_at = tail.rfind(EOCD_SIGNATURE)
    if eocd_at < 0:
        raise ValueError("ZIP end-of-central-directory record not found")
    eocd = tail[eocd_at : eocd_at + 22]
    (
        _signature,
        _disk_number,
        _central_disk,
        _entries_on_disk,
        total_entries,
        central_size,
        central_offset,
        _comment_length,
    ) = struct.unpack("<4s4H2IH", eocd)
    if central_size == 0xFFFFFFFF or central_offset == 0xFFFFFFFF:
        raise ValueError("ZIP64 archive is not supported yet")

    central = request_bytes(
        url,
        f"{central_offset}-{central_offset + central_size - 1}",
    )
    entries: list[dict[str, int | str]] = []
    cursor = 0
    while cursor < len(central):
        header = central[cursor : cursor + 46]
        if len(header) < 46 or header[:4] != CENTRAL_SIGNATURE:
            raise ValueError(f"Invalid central directory at byte {cursor}")
        compressed_size = struct.unpack_from("<I", header, 20)[0]
        uncompressed_size = struct.unpack_from("<I", header, 24)[0]
        compression_method = struct.unpack_from("<H", header, 10)[0]
        local_header_offset = struct.unpack_from("<I", header, 42)[0]
        name_length = struct.unpack_from("<H", header, 28)[0]
        extra_length = struct.unpack_from("<H", header, 30)[0]
        comment_length = struct.unpack_from("<H", header, 32)[0]
        flags = struct.unpack_from("<H", header, 8)[0]
        name_start = cursor + 46
        name_bytes = central[name_start : name_start + name_length]
        encoding = "utf-8" if flags & 0x800 else "cp437"
        entries.append(
            {
                "path": name_bytes.decode(encoding, errors="replace"),
                "compressed_size": compressed_size,
                "uncompressed_size": uncompressed_size,
                "compression_method": compression_method,
                "local_header_offset": local_header_offset,
            }
        )
        cursor = name_start + name_length + extra_length + comment_length

    if len(entries) != total_entries:
        raise ValueError(
            f"Expected {total_entries} entries, parsed {len(entries)}"
        )
    return archive_size, entries


def write_inventory(
    records: list[dict[str, int | str]],
    json_path: Path,
    csv_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handle", required=True, help="INE DSpace handle URL")
    parser.add_argument("--stage", required=True, help="precampana or campana")
    parser.add_argument("--output-prefix", required=True, type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    archives = list_archives(args.handle)
    if args.limit:
        archives = archives[: args.limit]
    if not archives:
        print("No ZIP archives found", file=sys.stderr)
        return 1

    json_path = args.output_prefix.with_suffix(".json")
    records: list[dict[str, int | str]] = []
    completed_archives: set[str] = set()
    if args.resume and json_path.exists():
        records = json.loads(json_path.read_text(encoding="utf-8"))
        completed_archives = {
            str(record["archive_name"]) for record in records
        }
    for index, archive in enumerate(archives, start=1):
        if archive["archive_name"] in completed_archives:
            print(
                f"[{index}/{len(archives)}] skip {archive['archive_name']}",
                file=sys.stderr,
                flush=True,
            )
            continue
        print(
            f"[{index}/{len(archives)}] {archive['archive_name']}",
            file=sys.stderr,
            flush=True,
        )
        try:
            archive_size, entries = remote_zip_entries(archive["archive_url"])
            for entry in entries:
                records.append(
                    {
                        "stage": args.stage,
                        **archive,
                        "archive_bytes": archive_size,
                        "inventory_status": "complete",
                        "inventory_note": "",
                        **entry,
                    }
                )
        except (
            OverflowError,
            HTTPError,
            URLError,
            ValueError,
            RemoteDisconnected,
            TimeoutError,
            TypeError,
        ) as error:
            try:
                archive_size: int | str = remote_size(archive["archive_url"])
            except (
                HTTPError,
                URLError,
                RemoteDisconnected,
                TimeoutError,
                ValueError,
                TypeError,
            ):
                archive_size = ""
            records.append(
                {
                    "stage": args.stage,
                    **archive,
                    "archive_bytes": archive_size,
                    "inventory_status": "archive_only",
                    "path": "",
                    "compressed_size": "",
                    "uncompressed_size": "",
                    "inventory_note": str(error),
                }
            )
        write_inventory(
            records,
            args.output_prefix.with_suffix(".json"),
            args.output_prefix.with_suffix(".csv"),
        )
        time.sleep(0.1)

    write_inventory(
        records,
        args.output_prefix.with_suffix(".json"),
        args.output_prefix.with_suffix(".csv"),
    )
    print(
        json.dumps(
            {
                "archives": len(archives),
                "entries": len(records),
                "json": str(args.output_prefix.with_suffix(".json")),
                "csv": str(args.output_prefix.with_suffix(".csv")),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
