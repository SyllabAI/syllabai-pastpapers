#!/usr/bin/env python3
"""Task 33 probe — re-resolve ONE misfiled lane-B row to see if exam-mate now
serves correct 4MA1 PDF urls (vs the junk 0985 Accounting June-2026 pair).

Row choice: 47332 = 4MA1/1H_Summer_2025 (junk in paper_urls.json).
Prints the fresh viewer urls + verdict. No downloads.
"""
import json
import re
import sys

sys.path.insert(0, "/home/z/my-project/scripts")
from pp_harvest_2020 import ExamMateClient, setup_state, discover_rows, viewer_urls  # noqa

ROW = "47332"
BAD_PAT = re.compile(r"accounting|0985", re.I)
GOOD_PAT = re.compile(r"4ma1|mathematic", re.I)

def main():
    c = ExamMateClient(restore_state=False, verbose=True)
    try:
        setup_state(c, 21, 615, ["2024", "2025", "2026"])
        rows = discover_rows(c, 21, 615, ["2024", "2025", "2026"])
        print(f"discovered {len(rows)} rows")
        hit = [r for r in rows if r["id"] == ROW]
        if not hit:
            print(f"row {ROW} NOT visible in list — dumping ids")
            print([r["id"] for r in rows][:60])
            return 2
        print("row:", hit[0])
        info = viewer_urls(c, ROW)
        print(json.dumps(info, indent=1))
        qp = info.get("qp") or ""
        verdict = "STILL-JUNK" if BAD_PAT.search(qp) else (
            "LOOKS-GOOD" if GOOD_PAT.search(qp) else "UNCLEAR")
        print("VERDICT:", verdict)
        return 0
    finally:
        c.close()

if __name__ == "__main__":
    sys.exit(main())
