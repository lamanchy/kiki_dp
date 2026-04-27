#!/usr/bin/env python3
"""Přejmenuje soubory v articles/ tak, aby fungovaly na Windows.

Windows zakazuje v názvech souborů znaky: < > : " / \\ | ? *
Skript je nahradí bezpečnými alternativami.
"""

from pathlib import Path

ARTICLES_DIR = Path(__file__).parent / "articles"

REPLACEMENTS = {
    ":": " -",
    '"': "'",
    "?": "",
    "<": "(",
    ">": ")",
    "|": "-",
    "*": "",
    "\\": "-",
    "/": "-",
}


def sanitize(name: str) -> str:
    for bad, good in REPLACEMENTS.items():
        name = name.replace(bad, good)
    # Windows nepovoluje koncové mezery a tečky (kromě přípony)
    stem, dot, ext = name.rpartition(".")
    if dot:
        name = stem.rstrip(" .") + "." + ext
    return name


def main() -> None:
    if not ARTICLES_DIR.is_dir():
        raise SystemExit(f"Adresář neexistuje: {ARTICLES_DIR}")

    renamed = 0
    for path in ARTICLES_DIR.iterdir():
        if not path.is_file():
            continue
        new_name = sanitize(path.name)
        if new_name == path.name:
            continue
        new_path = path.with_name(new_name)
        if new_path.exists():
            print(f"PŘESKOČENO (cíl existuje): {path.name} -> {new_name}")
            continue
        path.rename(new_path)
        print(f"{path.name} -> {new_name}")
        renamed += 1

    print(f"\nHotovo. Přejmenováno souborů: {renamed}")


if __name__ == "__main__":
    main()
