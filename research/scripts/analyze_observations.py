#!/usr/bin/env python3
"""Count observation blocks in INE individual consolidated opinions.

The unit of analysis is an ``ID`` immediately followed by ``Observación`` in
the individual opinion text.  This deliberately does not count sanctioning
conclusions, amounts, findings, or rows in annexes.
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEXT_DIR = ROOT / "research" / "derived" / "dictamenes_txt"
OUT_DIR = ROOT / "research" / "derived"

FILES = {
    "campana-cgex202407-22-dp-7-1-a2-02-pri-zip-DIC_PRI_FD.txt": ("campaña", "PRI"),
    "campana-cgex202407-22-dp-7-1-a2-03-prd-zip-DIC_PRD.txt": ("campaña", "PRD"),
    "campana-cgex202407-22-dp-7-1-a2-04-pt-zip-DIC_PT.txt": ("campaña", "PT"),
    "campana-cgex202407-22-dp-7-1-a2-06-mc-01-zip-DIC_MC.txt": ("campaña", "MC"),
    "campana-cgex202407-22-dp-7-1-a2-07-morena-01-zip-DIC_MORENA_FD.txt": (
        "campaña",
        "Morena",
    ),
    "precampana-cgor202402-27-dp-8-a2-01-pan-zip-DIC_PAN_FD.txt": (
        "precampaña",
        "PAN",
    ),
    "precampana-cgor202402-27-dp-8-a2-02-pri-zip-DIC_PRI_FD.txt": (
        "precampaña",
        "PRI",
    ),
    "precampana-cgor202402-27-dp-8-a2-03-prd-zip-DIC_PRD.txt": (
        "precampaña",
        "PRD",
    ),
    "precampana-cgor202402-27-dp-8-a2-04-pt-zip-PT_FD.txt": ("precampaña", "PT"),
    "precampana-cgor202402-27-dp-8-a2-05-pvem-zip-DIC_PVEM.txt": (
        "precampaña",
        "PVEM",
    ),
    "precampana_MC_DIC_MC.txt": ("precampaña", "MC"),
    "precampana-cgor202402-27-dp-8-a2-07-morena-zip-DIC_MORENA.txt": (
        "precampaña",
        "Morena",
    ),
}

BLOCK_RE = re.compile(r"(?m)^ID\s*\n(\d+)\s*\nObservaci[oó]n\b")


def main() -> None:
    detail = []
    totals: dict[str, int] = defaultdict(int)

    for filename, (stage, party) in FILES.items():
        source = TEXT_DIR / filename
        text = source.read_text(encoding="utf-8", errors="replace")
        ids = [int(value) for value in BLOCK_RE.findall(text)]
        unique_ids = sorted(set(ids))
        if len(ids) != len(unique_ids):
            raise ValueError(f"Repeated observation IDs in {source}")

        row = {
            "party": party,
            "stage": stage,
            "observations": len(ids),
            "first_id": unique_ids[0] if unique_ids else None,
            "last_id": unique_ids[-1] if unique_ids else None,
            "source_text": str(source.relative_to(ROOT)),
        }
        detail.append(row)
        totals[party] += len(ids)

    stages_by_party = defaultdict(set)
    for row in detail:
        stages_by_party[row["party"]].add(row["stage"])

    summary = [
        {
            "party": party,
            "precampaign_and_campaign_observations": total,
            "coverage": "complete"
            if stages_by_party[party] == {"precampaña", "campaña"}
            else "partial",
        }
        for party, total in sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    ]

    payload = {
        "method": "Unique ID/Observación blocks in each INE individual opinion",
        "scope": "Federal ordinary electoral process 2023-2024; precampaign and campaign",
        "detail": detail,
        "summary": summary,
    }
    (OUT_DIR / "observation_counts.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (OUT_DIR / "observation_counts.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "party",
                "precampaign_and_campaign_observations",
                "coverage",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(summary)

    for row in summary:
        print(
            f"{row['party']:7} "
            f"{row['precampaign_and_campaign_observations']:3} "
            f"{row['coverage']}"
        )


if __name__ == "__main__":
    main()
