#!/usr/bin/env python3
"""Small, dependency-free Decisions API demo for a workshop."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
SAMPLE = (
    "実験メモ：Decisions APIでイベントの質問メモを分類する。まず架空の質問10件を用意して"
    "APIに送り、分類結果を人が確認する。成功条件は10件中8件以上が意図した分類になること。"
)
QUESTIONS = [
    {
        "type": "predicate",
        "name": "concrete_next_step",
        "instructions": (
            "Does the note explicitly state a specific next action that someone could take? "
            "Judge only what is written, not what could be inferred."
        ),
    },
    {
        "type": "choice",
        "name": "memo_type",
        "instructions": (
            "What is the main purpose of this event note? Choose experiment when it proposes "
            "a test or implementation, even if it also mentions questions or sharing. "
            "Choose other only when none of the listed purposes fits."
        ),
        "choices": [
            {"value": "experiment", "description": "A proposed test or implementation to try."},
            {"value": "question", "description": "A question requiring an answer or investigation."},
            {"value": "share", "description": "A fact or learning to pass on to others."},
            {"value": "other", "description": "None of the above or too little information."},
        ],
    },
    {
        "type": "score",
        "name": "readiness",
        "instructions": "How ready is the proposed work to start, based only on the note?",
        "levels": [
            {"label": "Idea", "description": "Only a topic or wish; no action is specified."},
            {"label": "Action", "description": "A next action is specified, but input or success criteria are missing."},
            {"label": "Testable", "description": "A next action, input, and success criterion are specified."},
        ],
    },
]


def read_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    path = ROOT / ".env.local"
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("OPENAI_API_KEY="):
                return line.partition("=")[2].strip().strip('"\'')
    raise RuntimeError("OPENAI_API_KEY が見つかりません（.env.local または環境変数）。")


def make_input(note: str, image_path: Path | None) -> str | list[dict]:
    if image_path is None:
        return note
    mime = mimetypes.guess_type(image_path.name)[0]
    if mime not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError("画像は PNG、JPEG、WebP を指定してください。")
    if image_path.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("デモでは画像を10MB以下に制限しています。")
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return [{
        "role": "user",
        "content": [
            {"type": "input_text", "text": note or "Classify this event note image."},
            {"type": "input_image", "image_url": f"data:{mime};base64,{encoded}"},
        ],
    }]


def decide(payload: dict, key: str) -> dict:
    request = Request(
        "https://api.openai.com/v1/decisions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        try:
            error = json.load(exc).get("error", {})
            code = error.get("code") or error.get("type") or "unknown"
        except (ValueError, OSError):
            code = "unknown"
        raise RuntimeError(f"API HTTP {exc.code} ({code})") from None
    except URLError as exc:
        raise RuntimeError(f"API接続に失敗しました: {exc.reason}") from None


def main() -> int:
    parser = argparse.ArgumentParser(description="イベントメモをDecisions APIで判定")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--text", help="判定したいメモ本文")
    group.add_argument("--file", type=Path, help="UTF-8のメモファイル")
    group.add_argument("--sample", action="store_true", help="架空の例を使用（既定）")
    parser.add_argument("--image", type=Path, help="任意の画像ファイル（PNG/JPEG/WebP）")
    parser.add_argument("--dry-run", action="store_true", help="APIへ送らずリクエストJSONを表示")
    args = parser.parse_args()

    try:
        note = args.file.read_text(encoding="utf-8") if args.file else (args.text if args.text is not None else SAMPLE)
        if not note.strip() and not args.image:
            raise ValueError("メモ本文または画像を指定してください。")
        payload = {"model": "gpt-6-luna", "input": make_input(note, args.image), "questions": QUESTIONS}
        if args.dry_run:
            preview = json.loads(json.dumps(payload))
            if args.image:
                preview["input"][0]["content"][1]["image_url"] = "<inline image omitted>"
            print(json.dumps(preview, ensure_ascii=False, indent=2))
            return 0
        result = decide(payload, read_key())
        print(json.dumps({"model": result.get("model"), "answers": result.get("answers"), "usage": result.get("usage")}, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
