#!/usr/bin/env python3
"""Regression tests for the safe harness HTML report renderer."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts/render-harness-report.py"
TEMPLATE = ROOT / "04-projects/harness/templates/report.html"
ONE_PIXEL_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl6eQAAAABJRU5ErkJggg=="
)


def run_renderer(data: dict, directory: Path) -> subprocess.CompletedProcess[str]:
    data_path = directory / "report-data.json"
    output_path = directory / "report.html"
    data_path.write_text(json.dumps(data), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            str(RENDERER),
            "--template",
            str(TEMPLATE),
            "--data",
            str(data_path),
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def base_data() -> dict:
    injection = '</p><script>alert("x")</script><p>'
    return {
        "goal": injection,
        "north_star": "Ship <safe> evidence",
        "overall_status": 'done" onclick="alert(1)',
        "current_phase": "P1",
        "updated_at": "2026-08-07T08:00:00Z",
        "phases": [
            {
                "id": "P1",
                "goal": injection,
                "ac": "AC-1",
                "state": 'done" onclick="alert(2)',
                "evidence": "evidence/P1/",
            }
        ],
        "criteria": [
            {
                "id": "AC-1",
                "text": injection,
                "owner": "P1",
                "evidence": "CP-5",
                "status": "PASS",
            }
        ],
        "evidence": [
            {
                "ac": "AC-1",
                "checkpoint": "CP-5",
                "result": "PASS",
                "observation": injection,
                "artifact": 'artifact" onerror="alert(3)',
                "media": [
                    {
                        "data_uri": f"data:image/png;base64,{ONE_PIXEL_PNG}",
                        "alt": injection,
                        "caption": injection,
                    }
                ],
            }
        ],
        "open_items": [injection],
        "next_action": injection,
    }


def assert_rejected_media(data_uri: str, directory: Path, label: str) -> None:
    unsafe = base_data()
    unsafe["evidence"][0]["media"] = [{"data_uri": data_uri, "alt": label}]
    result = run_renderer(unsafe, directory)
    if result.returncode == 0:
        raise AssertionError(f"renderer accepted unsafe media: {label}")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        result = run_renderer(base_data(), directory)
        if result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)

        rendered = (directory / "report.html").read_text(encoding="utf-8")
        if '<script>alert("x")</script>' in rendered:
            raise AssertionError("raw script markup reached the rendered report")
        if '&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;' not in rendered:
            raise AssertionError("untrusted report text was not HTML-escaped")
        if 'onclick="alert(' in rendered or 'onerror="alert(' in rendered:
            raise AssertionError("untrusted event-handler markup reached the report")
        if f"data:image/png;base64,{ONE_PIXEL_PNG}" not in rendered:
            raise AssertionError("validated data-image media was not rendered")
        csp = "default-src 'none'; img-src data:; style-src 'unsafe-inline';"
        if csp not in rendered:
            raise AssertionError("rendered report is missing the restrictive CSP")

        token_probe = base_data()
        token_probe["goal"] = "{{evidence_blocks}}"
        token_result = run_renderer(token_probe, directory)
        if token_result.returncode != 0:
            raise AssertionError(token_result.stderr or token_result.stdout)
        token_rendered = (directory / "report.html").read_text(encoding="utf-8")
        if "{{evidence_blocks}}" not in token_rendered:
            raise AssertionError("user text that looks like a template token was reinterpreted")
        if token_rendered.count('<article class="evidence">') != 1:
            raise AssertionError("template-looking user text duplicated an evidence block")

        assert_rejected_media(
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
            directory,
            "HTML data URI",
        )
        assert_rejected_media(
            "data:image/svg+xml;base64,PHN2ZyBvbmxvYWQ9ImFsZXJ0KDEpIj48L3N2Zz4=",
            directory,
            "SVG data URI",
        )
        assert_rejected_media("javascript:alert(1)", directory, "javascript URI")

    print(
        "harness report renderer escapes text, uses one-pass tokens, enforces CSP, and rejects unsafe media"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
