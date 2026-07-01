#!/usr/bin/env python3
"""Best-effort OCR wrapper for admissions case screenshots.

The script intentionally fails openly when OCR tooling is unavailable. It should
produce a traceable artifact, not pretend that an image was understood.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run_tesseract(image: Path) -> tuple[str, str | None]:
    tesseract = shutil.which("tesseract")
    if not tesseract:
        return "", "tesseract-not-installed"

    attempts = [
        [tesseract, str(image), "stdout", "-l", "eng+chi_sim"],
        [tesseract, str(image), "stdout"],
    ]
    last_error = None
    for cmd in attempts:
        proc = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip(), None
        last_error = proc.stderr.strip() or f"exit-{proc.returncode}"
    return "", last_error or "empty-ocr-output"


def process_image(image: Path, out_dir: Path | None) -> dict[str, object]:
    result: dict[str, object] = {
        "image_path": str(image),
        "status": "pending",
        "method": "none",
        "text_path": None,
        "text": "",
        "error": None,
        "review_required": True,
        "privacy_note": "Review and redact names, handles, faces, chat IDs, phone numbers, emails, and exact personal identifiers before storing case fields.",
    }

    if not image.exists():
        result["status"] = "error"
        result["error"] = "image-not-found"
        return result
    if not image.is_file():
        result["status"] = "error"
        result["error"] = "not-a-file"
        return result

    text, error = run_tesseract(image)
    if text:
        result["status"] = "ok"
        result["method"] = "tesseract"
        result["text"] = text
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            text_path = out_dir / f"{image.stem}.ocr.txt"
            text_path.write_text(text + "\n", encoding="utf-8")
            result["text_path"] = str(text_path)
    else:
        result["status"] = "ocr_unavailable"
        result["error"] = error
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract text from admissions screenshots with local OCR when available."
    )
    parser.add_argument("images", nargs="+", help="Image paths to process")
    parser.add_argument("--out-dir", help="Directory for .ocr.txt outputs")
    parser.add_argument(
        "--jsonl",
        action="store_true",
        help="Print one JSON object per line instead of a JSON array",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else None
    results = [process_image(Path(p).expanduser().resolve(), out_dir) for p in args.images]

    if args.jsonl:
        for item in results:
            print(json.dumps(item, ensure_ascii=False))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

    return 0 if all(r["status"] in {"ok", "ocr_unavailable"} for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
