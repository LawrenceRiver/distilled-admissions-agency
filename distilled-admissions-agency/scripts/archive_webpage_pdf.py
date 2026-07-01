#!/usr/bin/env python3
"""Archive an official webpage as PDF, text, HTML, and validation metadata."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

try:
    import websocket
except ImportError:  # pragma: no cover - environment dependent
    websocket = None


def slugify(value: str, fallback: str = "page") -> str:
    value = re.sub(r"https?://", "", value.strip().lower())
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value).strip("-")
    return value[:96] or fallback


def find_chrome() -> str | None:
    candidates = [
        os.environ.get("CHROME_PATH"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chrome"),
        shutil.which("msedge"),
    ]
    for item in candidates:
        if item and Path(item).exists():
            return item
    return None


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def http_json(url: str, timeout: float = 1.0, method: str = "GET") -> dict:
    request = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_json(url: str, timeout_s: float = 10.0) -> dict:
    deadline = time.time() + timeout_s
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            return http_json(url)
        except Exception as exc:  # noqa: BLE001 - preserve startup errors
            last_error = exc
            time.sleep(0.1)
    raise RuntimeError(f"Chrome DevTools did not start: {last_error}")


class CDP:
    def __init__(self, ws_url: str) -> None:
        if websocket is None:
            raise RuntimeError(
                "Python websocket module is missing. Install with: python3 -m pip install websocket-client"
            )
        self.ws = websocket.create_connection(ws_url, timeout=10)
        self.next_id = 0

    def close(self) -> None:
        self.ws.close()

    def send(self, method: str, params: dict | None = None) -> dict:
        self.next_id += 1
        message_id = self.next_id
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == message_id:
                if "error" in msg:
                    raise RuntimeError(f"CDP {method} failed: {msg['error']}")
                return msg.get("result", {})

    def wait_event(self, event_name: str, timeout_s: float = 30.0) -> None:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            self.ws.settimeout(max(0.1, deadline - time.time()))
            try:
                msg = json.loads(self.ws.recv())
            except Exception:
                continue
            if msg.get("method") == event_name:
                return
        raise RuntimeError(f"Timed out waiting for {event_name}")


def launch_chrome(chrome: str, port: int, user_data_dir: Path) -> subprocess.Popen:
    cmd = [
        chrome,
        "--headless=new",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--remote-allow-origins=*",
        "about:blank",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def create_target(port: int) -> str:
    url = f"http://127.0.0.1:{port}/json/new"
    try:
        target = http_json(url, timeout=3, method="PUT")
    except urllib.error.HTTPError:
        target = http_json(url + "?about:blank", timeout=3)
    ws_url = target.get("webSocketDebuggerUrl")
    if not ws_url:
        raise RuntimeError("Chrome target did not return a websocket URL")
    return ws_url


def evaluate(cdp: CDP, expression: str) -> str:
    result = cdp.send(
        "Runtime.evaluate",
        {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        },
    )
    value = (result.get("result") or {}).get("value")
    return "" if value is None else str(value)


def print_pdf(cdp: CDP, path: Path) -> None:
    result = cdp.send(
        "Page.printToPDF",
        {
            "printBackground": True,
            "preferCSSPageSize": True,
            "marginTop": 0.4,
            "marginBottom": 0.4,
            "marginLeft": 0.35,
            "marginRight": 0.35,
        },
    )
    data = base64.b64decode(result["data"])
    path.write_bytes(data)


def inject_color_enhancement(cdp: CDP) -> None:
    css = r"""
(() => {
  const style = document.createElement('style');
  style.setAttribute('data-distilled-admissions-archive', 'color-enhanced-print');
  style.textContent = `
    @media print {
      body, body * {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        text-shadow: none !important;
      }
      a, a * {
        color: #0645ad !important;
        -webkit-text-fill-color: #0645ad !important;
        text-decoration: underline !important;
      }
      input, textarea, select {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
      }
    }
  `;
  document.documentElement.appendChild(style);
  return true;
})()
"""
    cdp.send("Runtime.evaluate", {"expression": css, "returnByValue": True})


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def extract_pdf_text(pdf_path: Path, text_path: Path) -> str:
    tool = shutil.which("pdftotext")
    if not tool:
        return ""
    code, _, _ = run_command([tool, str(pdf_path), str(text_path)])
    if code != 0 or not text_path.exists():
        return ""
    return text_path.read_text(encoding="utf-8", errors="replace")


def pdf_pages(pdf_path: Path) -> int | None:
    tool = shutil.which("pdfinfo")
    if not tool:
        return None
    code, out, _ = run_command([tool, str(pdf_path)])
    if code != 0:
        return None
    match = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(match.group(1)) if match else None


def tokens(text: str) -> set[str]:
    found = re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_./%-]*|[\u4e00-\u9fff]{2,}", text.lower())
    return {item for item in found if len(item) >= 2}


def validate_text(dom_text: str, pdf_text: str) -> tuple[str, dict[str, object]]:
    dom_tokens = tokens(dom_text)
    pdf_tokens = tokens(pdf_text)
    common = dom_tokens & pdf_tokens
    denominator = max(1, min(len(dom_tokens), len(pdf_tokens)))
    overlap = len(common) / denominator
    if not pdf_text.strip():
        status = "no-pdf-text"
    elif len(pdf_text.strip()) < 100 or overlap < 0.18:
        status = "weak-text-match"
    else:
        status = "ok"
    return status, {
        "dom_text_chars": len(dom_text),
        "pdf_text_chars": len(pdf_text),
        "dom_unique_tokens": len(dom_tokens),
        "pdf_unique_tokens": len(pdf_tokens),
        "common_unique_tokens": len(common),
        "token_overlap_ratio": round(overlap, 4),
        "status": status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive a public official webpage as PDF and text.")
    parser.add_argument("url", help="Official webpage URL to archive")
    parser.add_argument("--out-dir", default="admissions-db/11_webpage_archive")
    parser.add_argument("--archive-id", help="Stable archive id; defaults to a URL slug")
    parser.add_argument("--school", default="")
    parser.add_argument("--program", default="")
    parser.add_argument("--wait-ms", type=int, default=2500)
    parser.add_argument("--timeout-s", type=int, default=45)
    parser.add_argument("--no-enhanced", action="store_true", help="Skip color-enhanced PDF")
    args = parser.parse_args()

    chrome = find_chrome()
    if not chrome:
        print(
            json.dumps(
                {
                    "status": "archive-failed",
                    "error": "chrome-not-found",
                    "next_action": "Install Google Chrome/Chromium or set CHROME_PATH.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    out_root = Path(args.out_dir).expanduser().resolve()
    archive_id = args.archive_id or slugify(args.url)
    dirs = {
        "pdf_original": out_root / "pdf-original",
        "pdf_enhanced": out_root / "pdf-enhanced",
        "html": out_root / "html",
        "text": out_root / "text",
        "validation": out_root / "validation",
    }
    for directory in dirs.values():
        directory.mkdir(parents=True, exist_ok=True)

    original_pdf = dirs["pdf_original"] / f"{archive_id}.pdf"
    enhanced_pdf = dirs["pdf_enhanced"] / f"{archive_id}.color-enhanced.pdf"
    html_path = dirs["html"] / f"{archive_id}.html"
    dom_text_path = dirs["text"] / f"{archive_id}.dom.txt"
    pdf_text_path = dirs["text"] / f"{archive_id}.pdf.txt"
    validation_path = dirs["validation"] / f"{archive_id}.validation.json"

    proc: subprocess.Popen | None = None
    with tempfile.TemporaryDirectory(prefix="distilled-webpage-archive-") as tmp:
        port = free_port()
        proc = launch_chrome(chrome, port, Path(tmp) / "chrome-profile")
        try:
            wait_for_json(f"http://127.0.0.1:{port}/json/version")
            cdp = CDP(create_target(port))
            try:
                cdp.send("Page.enable")
                cdp.send("Runtime.enable")
                cdp.send("Page.navigate", {"url": args.url})
                cdp.wait_event("Page.loadEventFired", timeout_s=args.timeout_s)
                if args.wait_ms > 0:
                    time.sleep(args.wait_ms / 1000)

                title = evaluate(cdp, "document.title")
                dom_text = evaluate(cdp, "document.body ? document.body.innerText : ''")
                html = evaluate(cdp, "document.documentElement ? document.documentElement.outerHTML : ''")
                html_path.write_text(html, encoding="utf-8")
                dom_text_path.write_text(dom_text + "\n", encoding="utf-8")

                print_pdf(cdp, original_pdf)
                pdf_text = extract_pdf_text(original_pdf, pdf_text_path)
                status, validation = validate_text(dom_text, pdf_text)
                validation.update(
                    {
                        "archive_id": archive_id,
                        "date": date.today().isoformat(),
                        "source_url": args.url,
                        "page_title": title,
                        "school": args.school,
                        "program": args.program,
                        "original_pdf_path": str(original_pdf),
                        "html_path": str(html_path),
                        "dom_text_path": str(dom_text_path),
                        "pdf_text_path": str(pdf_text_path),
                        "original_pdf_pages": pdf_pages(original_pdf),
                    }
                )

                enhanced_path_value = ""
                if not args.no_enhanced:
                    inject_color_enhancement(cdp)
                    print_pdf(cdp, enhanced_pdf)
                    enhanced_path_value = str(enhanced_pdf)
                validation["enhanced_pdf_path"] = enhanced_path_value
                validation["color_mode"] = "original+color-enhanced" if enhanced_path_value else "original-only"

                validation_path.write_text(
                    json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                print(json.dumps({"status": status, "validation_json": str(validation_path)}, ensure_ascii=False, indent=2))
            finally:
                cdp.close()
        finally:
            if proc:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
