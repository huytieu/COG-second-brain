#!/usr/bin/env bash
# Turn a screen recording into the frames + manifest compose_demo.py reads.
#   frames_from_video.sh <recording.mp4|.mov> <name> [fps]   -> <name>.frames/ and <name>.manifest.json
set -euo pipefail
src=$1; name=$2; fps=${3:-30}
mkdir -p "$name.frames"
ffmpeg -v error -y -i "$src" -vf "fps=$fps" -q:v 3 -start_number 0 "$name.frames/%05d.jpg"
python3 - "$name" "$fps" <<'PY'
import json, os, sys
from PIL import Image
name, fps = sys.argv[1], int(sys.argv[2])
d = f"{name}.frames"; n = len([f for f in os.listdir(d) if f.endswith(".jpg")])
w, h = Image.open(f"{d}/00000.jpg").size
json.dump({"frames_dir": os.path.abspath(d), "fps": fps, "frame_count": n, "img_w": w, "img_h": h, "duration": n / fps},
          open(f"{name}.manifest.json", "w"), indent=1)
print(f"{name}.manifest.json  {n} frames  {w}x{h}  {n / fps:.1f}s")
PY
