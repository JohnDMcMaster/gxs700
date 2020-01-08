#!/usr/bin/env bash
set -ex

n=${CALN:-1}
d=$(python3 cal_dir.py)
echo "Output dir $d: writing $n files"
mkdir -p $d
python3 main.py --no-xray -n "$n" --dir "$d/df" --raw
python3 main.py --xray -n "$n" --dir "$d/ff" --raw
python3 cal.py $d/ff $d/df $d

