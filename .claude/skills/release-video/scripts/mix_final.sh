#!/usr/bin/env bash
# Mix picture + SFX track + optional music bed, duck the music under every effect, hit loudness.
#   mix_final.sh <video.mp4> <sfx-track.wav> [music.mp3] <out.mp4>
# Normalizes toward -18 LUFS integrated (single pass, within about 1 LU) with true peak under -1.5 dBTP (loudnorm), then reports both. Also writes <out>-web.mp4 (CRF 23).
set -euo pipefail
v=$1; fx=$2
if [ $# -eq 4 ]; then music=$3; out=$4; else music=""; out=$3; fi
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
fo=$(python3 -c "print(max(0, $dur - 1.6))")
if [ -n "$music" ]; then
  L=$(ffmpeg -i "$music" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
  G=$(python3 -c "print(round(-22 - ($L), 1))")   # bed ~4 dB under the effects
  fc="[1:a]asplit=2[fx][sc];[2:a]atrim=0:$dur,volume=${G}dB,afade=t=in:d=0.6,afade=t=out:st=$fo:d=1.6[m];[m][sc]sidechaincompress=threshold=0.05:ratio=2:attack=6:release=220:makeup=1[md];[fx][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-18:TP=-1.5:LRA=11,aresample=48000[a]"
  ffmpeg -v error -y -i "$v" -i "$fx" -i "$music" -filter_complex "$fc" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$out"
else
  ffmpeg -v error -y -i "$v" -i "$fx" -filter_complex "[1:a]afade=t=out:st=$fo:d=1.6,loudnorm=I=-18:TP=-1.5:LRA=11,aresample=48000[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$out"
fi
ffmpeg -v error -y -i "$out" -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "${out%.mp4}-web.mp4"
for f in "$out" "${out%.mp4}-web.mp4"; do
  echo "$f  $(ffmpeg -i "$f" -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tr -s ' ' | tr '\n' ' ')"
done
echo "silences over 1s (should be none mid-video):"
ffmpeg -i "$out" -af "silencedetect=n=-50dB:d=1" -f null - 2>&1 | grep -E "silence_(start|end)" || echo "  none"
