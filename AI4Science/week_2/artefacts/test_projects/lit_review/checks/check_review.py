"""Проверка результата: python checks/check_review.py. Код 0 — принято, 1 — нет."""

import csv, hashlib, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
lib = root / "library"
errors = []
h = hashlib.sha256()
for f in sorted(lib.rglob("*")):
    if f.is_file():
        h.update(f.relative_to(lib).as_posix().encode())
        h.update(f.read_bytes())
if h.hexdigest() != (root / "checks" / "library_hash.txt").read_text().strip():
    errors.append("библиотека library/ изменена")
meta = {}
for f in sorted(lib.glob("*.md")):
    m = re.search(r"^doi:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
    if m:
        meta[m.group(1)] = f.name
table, draft = root / "review" / "table.csv", root / "review" / "draft.md"
if not table.is_file() or not draft.is_file():
    print("нужны review/table.csv и review/draft.md")
    sys.exit(1)
rows = list(csv.DictReader(open(table, encoding="utf-8")))
dois = {r.get("doi", "").strip() for r in rows}
for doi, name in meta.items():
    if doi not in dois:
        errors.append(f"в таблице нет работы {doi} ({name})")
for r in rows:
    doi = r.get("doi", "").strip()
    if doi not in meta:
        errors.append(f"в таблице работа {doi}, которой нет в библиотеке")
    elif r.get("file", "").strip() != meta[doi]:
        errors.append(f"{doi}: указан файл {r.get('file')}, а должен быть {meta[doi]}")
cites = re.findall(r"\[(10\.[^\]\s]+)\]", draft.read_text(encoding="utf-8"))
for c in cites:
    if c not in dois:
        errors.append(f"в обзоре ссылка [{c}], которой нет в таблице")
if len(set(cites)) < 5:
    errors.append(f"в обзоре {len(set(cites))} разных ссылок, нужно не меньше 5")
print(
    "\n".join(errors)
    if errors
    else "принято: таблица и ссылки согласованы с библиотекой"
)
sys.exit(1 if errors else 0)
