#!/usr/bin/env python3
"""Check if URL was already processed. Adds it if new. Exits 0=new, 1=exists."""
import sys
from pathlib import Path

URL_FILE = Path(__file__).parent / "checked_urls.md"

def main():
    if len(sys.argv) != 2:
        print("Usage: check_url.py <url>", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1].strip()

    existing = set()
    if URL_FILE.exists():
        existing = {line.strip() for line in URL_FILE.read_text(encoding="utf-8").splitlines() if line.strip()}

    if url in existing:
        sys.exit(1)

    with URL_FILE.open("a", encoding="utf-8") as f:
        f.write(url + "\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
