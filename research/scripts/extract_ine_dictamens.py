#!/usr/bin/env python3
"""Extract individual INE dictamen DOCX files through HTTP byte ranges."""

from __future__ import annotations

import argparse
import json
import re
import struct
import zlib
from pathlib import Path

from inventory_ine_archives import remote_zip_entries, request_bytes


LOCAL_SIGNATURE = b"PK\x03\x04"


def read_member(url: str, entry: dict[str, int | str]) -> bytes:
    offset = int(entry["local_header_offset"])
    header = request_bytes(url, f"{offset}-{offset + 29}")
    if header[:4] != LOCAL_SIGNATURE:
        raise ValueError(f"Invalid local header for {entry['path']}")
    name_length = struct.unpack_from("<H", header, 26)[0]
    extra_length = struct.unpack_from("<H", header, 28)[0]
    data_start = offset + 30 + name_length + extra_length
    compressed_size = int(entry["compressed_size"])
    payload = request_bytes(
        url,
        f"{data_start}-{data_start + compressed_size - 1}",
    )
    method = int(entry["compression_method"])
    if method == 0:
        return payload
    if method == 8:
        return zlib.decompress(payload, -zlib.MAX_WBITS)
    raise ValueError(f"Unsupported ZIP compression method {method}")


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True, type=Path, nargs="+")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    rows: list[dict[str, str | int]] = []
    for inventory_path in args.inventory:
        rows.extend(json.loads(inventory_path.read_text(encoding="utf-8")))
    targets: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        path = str(row.get("path", ""))
        if path.lower().endswith(".docx") and re.search(
            r"(^|/)(dic|dictamen)", path, re.I
        ):
            targets[(str(row["archive_url"]), path)] = row

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str | int]] = []
    for (url, target_path), row in targets.items():
        print(f"Indexing {row['archive_name']}", flush=True)
        _size, entries = remote_zip_entries(url)
        match = next(entry for entry in entries if entry["path"] == target_path)
        content = read_member(url, match)
        output_name = (
            f"{row['stage']}-{slug(str(row['archive_name']))}-"
            f"{Path(target_path).name}"
        )
        output_path = args.output_dir / output_name
        output_path.write_bytes(content)
        manifest.append(
            {
                "stage": str(row["stage"]),
                "archive_name": str(row["archive_name"]),
                "archive_url": url,
                "member_path": target_path,
                "output_path": str(output_path),
                "bytes": len(content),
            }
        )

    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"documents": len(manifest)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
