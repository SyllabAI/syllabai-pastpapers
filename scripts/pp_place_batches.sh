#!/bin/bash
# Batch runner for image placement (remaining codes), with disk guard between batches
set -u
cd /home/z/my-project
LOG=pp2026_placement/place_batches.log
echo "=== batches start $(date -u +%H:%M:%S) ===" >> $LOG
run() {
  local codes="$1"
  free=$(df --output=avail -B1 /home/z | tail -1)
  if [ "$free" -lt 1500000000 ]; then echo "!! disk guard: ${free}B free, abort before [$codes]" >> $LOG; exit 1; fi
  echo "--- batch [$codes] $(date -u +%H:%M:%S) free=${free}B" >> $LOG
  timeout 3600 python3 -u scripts/pp_place_commit.py "$codes" >> $LOG 2>&1
  rc=$?
  echo "--- batch [$codes] rc=$rc $(date -u +%H:%M:%S)" >> $LOG
  [ $rc -ne 0 ] && exit $rc
}
run "4BI1,4CH1,4PH1,4MB1"
run "4MA1,4PM0,4BI0"
run "4CH0,4PH0,4MB0"
run "WBI01,WCH01,WCH11,WPH01,WPH11"
run "4MA0"
run "0580,0620,0625"
run "9701,9702,9709"
echo "=== all batches done $(date -u +%H:%M:%S) ===" >> $LOG
