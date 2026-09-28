#!/usr/bin/env python3
"""Render a self-contained COG harness report from structured JSON safely."""

from __future__ import annotations

import argparse
import base64
import binascii
import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "04-projects/harness/templates/report.html"
ALLOWED_IMAGE_MIME = {"image/png", "image/jpeg", "image/webp", "image/gif"}
MAX_MEDIA_BYTES = 10 * 1024 * 1024
DATA_IMAGE_RE = re.compile(
    r"^data:(image/(?:png|jpeg|webp|gif));base64,([A-Za-z0-9+/=\s]+)$"
)
TOKEN_RE = re.compile(r"\{\{([a-z0-9_]+)\}\}")


def text(value: Any) -> str:
    """Convert a value to escaped HTML text."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def status_class(value: Any) -> str:
    """Map untrusted status text to one of the template's fixed CSS classes."""
    normalized = str(value or "").strip().lower()
    if normalized in {"pass", "passed", "done", "verified", "complete", "completed"}:
        return "pass"
    if normalized in {"fail", "failed", "blocked", "error"}:
        return "fail"
    return "open"


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    """Return a list field or fail closed when the input shape is invalid."""
    value = data.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    return value


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    """Return a mapping value or fail with a useful input error."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} entries must be objects")
    return value


def render_media(items: Any) -> str:
    """Render reviewed base64 data images only; arbitrary markup is never accepted."""
    if items in (None, []):
        return ""
    if not isinstance(items, list):
        raise ValueError("evidence media must be a list")

    rendered: list[str] = []
    for index, raw in enumerate(items):
        item = require_mapping(raw, f"media[{index}]")
        data_uri = str(item.get("data_uri", ""))
        match = DATA_IMAGE_RE.fullmatch(data_uri)
        if not match or match.group(1) not in ALLOWED_IMAGE_MIME:
            raise ValueError(
                "media data_uri must be a base64 data:image URI for png, jpeg, webp, or gif"
            )

        payload = re.sub(r"\s+", "", match.group(2))
        try:
            decoded = base64.b64decode(payload, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("media data_uri contains invalid base64") from exc
        if len(decoded) > MAX_MEDIA_BYTES:
            raise ValueError(f"media item exceeds {MAX_MEDIA_BYTES} bytes")

        safe_uri = f"data:{match.group(1)};base64,{payload}"
        alt = text(item.get("alt", "Evidence image"))
        caption = text(item.get("caption", ""))
        caption_html = f"<figcaption>{caption}</figcaption>" if caption else ""
        rendered.append(
            f'<figure><img src="{safe_uri}" alt="{alt}">{caption_html}</figure>'
        )
    return "\n".join(rendered)


def render_phase_rows(data: dict[str, Any]) -> str:
    """Render phase rows with every user-controlled field HTML-escaped."""
    rows: list[str] = []
    for index, raw in enumerate(require_list(data, "phases")):
        item = require_mapping(raw, f"phases[{index}]")
        state = item.get("state", "")
        rows.append(
            "<tr>"
            f"<td>{text(item.get('id'))}</td>"
            f"<td>{text(item.get('goal'))}</td>"
            f"<td>{text(item.get('ac'))}</td>"
            f'<td class="status {status_class(state)}">{text(state)}</td>'
            f"<td>{text(item.get('evidence'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_criterion_rows(data: dict[str, Any]) -> str:
    """Render acceptance-criterion rows without trusting input markup or classes."""
    rows: list[str] = []
    for index, raw in enumerate(require_list(data, "criteria")):
        item = require_mapping(raw, f"criteria[{index}]")
        state = item.get("status", "")
        rows.append(
            "<tr>"
            f"<td>{text(item.get('id'))}</td>"
            f"<td>{text(item.get('text'))}</td>"
            f"<td>{text(item.get('owner'))}</td>"
            f"<td>{text(item.get('evidence'))}</td>"
            f'<td class="status {status_class(state)}">{text(state)}</td>'
            "</tr>"
        )
    return "\n".join(rows)


def render_evidence_blocks(data: dict[str, Any]) -> str:
    """Render evidence observations and validated media without raw HTML substitution."""
    blocks: list[str] = []
    for index, raw in enumerate(require_list(data, "evidence")):
        item = require_mapping(raw, f"evidence[{index}]")
        result = item.get("result", "")
        media_html = render_media(item.get("media", []))
        blocks.append(
            '<article class="evidence">'
            f"<strong>{text(item.get('ac'))} | {text(item.get('checkpoint'))} | "
            f'<span class="{status_class(result)}">{text(result)}</span></strong>'
            f"<p>{text(item.get('observation'))}</p>"
            f"<small>Artifact: <code>{text(item.get('artifact'))}</code></small>"
            f"{media_html}"
            "</article>"
        )
    return "\n".join(blocks)


def render_open_items(data: dict[str, Any]) -> str:
    """Render open items as escaped list entries."""
    items = require_list(data, "open_items")
    if not items:
        return "<p>None</p>"
    return "<ul>" + "".join(f"<li>{text(item)}</li>" for item in items) + "</ul>"


def render(template: str, data: dict[str, Any]) -> str:
    """Fill supported tokens in one pass so inserted text is never reinterpreted."""
    replacements = {
        "goal": text(data.get("goal")),
        "north_star": text(data.get("north_star")),
        "overall_status": text(data.get("overall_status")),
        "current_phase": text(data.get("current_phase")),
        "updated_at": text(data.get("updated_at")),
        "phase_rows": render_phase_rows(data),
        "criterion_rows": render_criterion_rows(data),
        "evidence_blocks": render_evidence_blocks(data),
        "open_items": render_open_items(data),
        "next_action": text(data.get("next_action")),
    }

    def replace_token(match: re.Match[str]) -> str:
        key = match.group(1)
        try:
            return replacements[key]
        except KeyError as exc:
            raise ValueError(f"unsupported template token: {key}") from exc

    return TOKEN_RE.sub(replace_token, template)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for deterministic report rendering."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path, help="structured report JSON")
    parser.add_argument("--output", required=True, type=Path, help="rendered HTML path")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="HTML template")
    return parser.parse_args()


def main() -> int:
    """Load inputs, render safely, and write the report atomically enough for local use."""
    args = parse_args()
    raw = json.loads(args.data.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("report data root must be an object")

    rendered = render(args.template.read_text(encoding="utf-8"), raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
