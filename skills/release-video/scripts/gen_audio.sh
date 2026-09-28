#!/usr/bin/env bash
# ElevenLabs audio for a release video. Needs ELEVENLABS_API_KEY.
#   gen_audio.sh sfx <name> "<prompt>" <seconds> [outdir]    one sound effect -> outdir/<name>.mp3
#   gen_audio.sh music <plan.json> <out.mp3>                 composed track from a sectioned plan
set -euo pipefail
: "${ELEVENLABS_API_KEY:?set ELEVENLABS_API_KEY}"
case "${1:-}" in
  sfx)
    out="${5:-sfx}"; mkdir -p "$out"
    body=$(python3 -c 'import json,sys; print(json.dumps({"text": sys.argv[1], "duration_seconds": float(sys.argv[2]), "prompt_influence": 0.6}))' "$3" "$4")
    curl -sf -X POST "https://api.elevenlabs.io/v1/sound-generation" -H "xi-api-key: $ELEVENLABS_API_KEY" \
      -H "Content-Type: application/json" -d "$body" -o "$out/$2.mp3"
    echo "$out/$2.mp3" ;;
  music)
    curl -sf -X POST "https://api.elevenlabs.io/v1/music" -H "xi-api-key: $ELEVENLABS_API_KEY" \
      -H "Content-Type: application/json" -d @"$2" -o "$3"
    echo "$3" ;;
  *) sed -n 2,4p "$0"; exit 2 ;;
esac
