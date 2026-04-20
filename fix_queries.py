import os
import re
from collections import Counter

articles_dir = "/home/lamanchy/dp/articles"
counts = Counter()

for fname in os.listdir(articles_dir):
    if not fname.endswith(".md"):
        continue
    with open(os.path.join(articles_dir, fname), encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'^dotaz:\s*(.+)$', content, re.MULTILINE)
    if m:
        counts[m.group(1).strip()] += 1

with open("/home/lamanchy/dp/search_queries.md", encoding="utf-8") as f:
    lines = f.readlines()

updated = []
changed = 0
for line in lines:
    m = re.match(r'^(\| )(.+?)( \| .+? \| hotovo \| )(\d+|—)( \|.*)$', line)
    if m:
        dotaz = m.group(2).strip()
        actual = counts.get(dotaz, 0)
        old = m.group(4)
        new_line = m.group(1) + m.group(2) + m.group(3) + str(actual) + m.group(5) + "\n"
        if old != str(actual):
            print(f"  {dotaz[:60]}: {old} -> {actual}")
            changed += 1
        updated.append(new_line)
    else:
        updated.append(line)

with open("/home/lamanchy/dp/search_queries.md", "w", encoding="utf-8") as f:
    f.writelines(updated)

print(f"\nAktualizováno {changed} řádků.")
