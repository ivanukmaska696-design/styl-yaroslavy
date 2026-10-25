#!/bin/zsh
# Trims transparent margins from PNGs (3D props from Higgsfield come as 1024x1024 with lots of empty space),
# so CSS sizes and positions apply to the visible object. Writes t-<name>.png next to each input.
# usage: trim_alpha.sh prop1.png prop2.png ...
FF=${FFMPEG:-$HOME/.local/bin/ffmpeg}
[[ -x $FF ]] || FF=$(command -v ffmpeg)
for f in "$@"; do
  c=$($FF -loglevel info -loop 1 -i "$f" -frames:v 3 -vf "alphaextract,cropdetect=limit=8:round=2:skip=0" -f null - 2>&1 | grep -o 'crop=[0-9:]*' | tail -1)
  [[ -z $c ]] && { echo "skip $f (no alpha?)"; continue; }
  out="$(dirname "$f")/t-$(basename "$f")"
  $FF -v error -y -i "$f" -vf "$c" "$out" && echo "$out $c"
done
