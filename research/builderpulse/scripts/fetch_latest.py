#!/usr/bin/env python3
"""Fetch the latest BuilderPulse daily report from GitHub.

Prints JSON with date, language, source URLs, path, and markdown content.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import subprocess
import urllib.request
from urllib.error import HTTPError, URLError

OWNER_REPO = "BuilderPulse/BuilderPulse"
BRANCH = "main"
RAW_BASE = f"https://raw.githubusercontent.com/{OWNER_REPO}/{BRANCH}"
API_BASE = f"https://api.github.com/repos/{OWNER_REPO}/contents"


def fetch_text(url: str, timeout: int = 25) -> str:
    """Fetch URL text.

    Prefer curl because this environment often needs SOCKS/HTTP proxy support
    that urllib cannot reliably provide without PySocks.
    """
    proxies = [
        os.environ.get("BUILDERPULSE_PROXY", ""),
        os.environ.get("HTTPS_PROXY", ""),
        os.environ.get("HTTP_PROXY", ""),
        "socks5h://127.0.0.1:1089",
        "http://127.0.0.1:7897",
        "",
    ]
    seen = set()
    errors = []
    for proxy in proxies:
        if proxy in seen:
            continue
        seen.add(proxy)
        cmd = ["curl", "-fsSL", "--connect-timeout", "10", "--max-time", str(timeout), "-A", "Hermes-BuilderPulse-Skill/1.0"]
        if proxy:
            cmd += ["--proxy", proxy]
        cmd.append(url)
        try:
            p = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return p.stdout
        except Exception as e:
            errors.append(f"curl proxy={proxy or 'direct'}: {e}")
    req = urllib.request.Request(url, headers={"User-Agent": "Hermes-BuilderPulse-Skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        errors.append(f"urllib: {e}")
        raise RuntimeError("; ".join(errors[-4:]))


def list_year_files(lang: str, year: int) -> list[str]:
    url = f"{API_BASE}/{lang}/{year}?ref={BRANCH}"
    data = json.loads(fetch_text(url))
    files = []
    for item in data:
        name = item.get("name", "")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", name):
            files.append(name[:-3])
    return sorted(files)


def find_latest(lang: str, start_year: int | None = None) -> str:
    year = start_year or dt.date.today().year
    for y in range(year, year - 3, -1):
        try:
            files = list_year_files(lang, y)
        except Exception:
            files = []
        if files:
            return files[-1]
    raise RuntimeError(f"No BuilderPulse reports found for lang={lang!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    parser.add_argument("--date", help="YYYY-MM-DD; defaults to latest available")
    parser.add_argument("--max-chars", type=int, default=0, help="truncate content to this many characters; 0 means full")
    args = parser.parse_args()

    date = args.date or find_latest(args.lang)
    year = date[:4]
    path = f"{args.lang}/{year}/{date}.md"
    raw_url = f"{RAW_BASE}/{path}"
    github_url = f"https://github.com/{OWNER_REPO}/blob/{BRANCH}/{path}"

    try:
        content = fetch_text(raw_url)
    except (HTTPError, URLError) as e:
        print(json.dumps({"ok": False, "error": str(e), "path": path, "raw_url": raw_url}, ensure_ascii=False), file=sys.stderr)
        return 2

    truncated = False
    if args.max_chars and len(content) > args.max_chars:
        content = content[: args.max_chars] + "\n\n[TRUNCATED]\n"
        truncated = True

    print(json.dumps({
        "ok": True,
        "date": date,
        "lang": args.lang,
        "path": path,
        "raw_url": raw_url,
        "github_url": github_url,
        "truncated": truncated,
        "content": content,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
