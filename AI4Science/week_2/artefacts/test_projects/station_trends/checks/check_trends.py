"""Проверка результата: python checks/check_trends.py. Код 0 — принято, 1 — нет.
Эталон считается здесь же из data/raw: наклон МНК, °C за десятилетие."""
import csv, hashlib, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
raw = root / "data" / "raw"
h = hashlib.sha256()
for f in sorted(raw.rglob("*")):
    if f.is_file():
        h.update(f.relative_to(raw).as_posix().encode()); h.update(f.read_bytes())
errors = []
if h.hexdigest() != (root / "checks" / "data_hash.txt").read_text().strip():
    errors.append("исходные данные в data/raw изменены")
res = root / "results" / "trends.csv"
if not res.is_file():
    print("нет файла results/trends.csv"); sys.exit(1)
got = {r["station"]: r for r in csv.DictReader(open(res, encoding="utf-8"))}
for f in sorted(raw.glob("station_*.csv")):
    st = f.stem.split("_")[1]
    pts = [(int(r["year"]), float(r["t_mean_c"])) for r in csv.DictReader(open(f, encoding="utf-8"))]
    if st not in got:
        errors.append(f"станции {st} нет в результате"); continue
    r = got[st]
    if len(pts) < 0.7 * 35:                          # больше 30 % пропусков
        if str(r.get("flag", "")).strip() != "1":
            errors.append(f"станция {st}: пропусков больше 30 %, нужен flag = 1")
        continue
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    slope = 10 * sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    try:
        s, lo, hi = float(r["slope_c_per_decade"]), float(r["ci_low"]), float(r["ci_high"])
    except (KeyError, ValueError):
        errors.append(f"станция {st}: нет числового наклона или интервала"); continue
    if abs(s - slope) > 0.01:
        errors.append(f"станция {st}: наклон {s} расходится с эталоном {slope:.3f}")
    if not lo < slope < hi:
        errors.append(f"станция {st}: интервал [{lo}, {hi}] не содержит эталон")
print("\n".join(errors) if errors else "принято: наклоны и интервалы сходятся с эталоном")
sys.exit(1 if errors else 0)
