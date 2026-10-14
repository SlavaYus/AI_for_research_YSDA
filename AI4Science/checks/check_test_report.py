"""Проверка отчёта о тестах: python3 checks/check_test_report.py. Код 0 — принято, 1 — нет."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "test_report.md"
errors = []

# 1. Отчёт существует
if not REPORT.is_file():
    print(f"нет файла {REPORT.relative_to(ROOT)}")
    sys.exit(1)

content = REPORT.read_text(encoding="utf-8")

# 2. Содержит ключевые секции
if "passed" not in content.lower() and "passed" not in content:
    errors.append("в отчёте нет информации о passed тестах")
if "failed" not in content.lower() and "failed" not in content:
    errors.append("в отчёте нет информации о failed тестах")
if "skipped" not in content.lower() and "skipped" not in content:
    errors.append("в отчёте нет информации о skipped тестах")

# 3. Есть число тестов
import re
nums = re.findall(r'\d+', content)
if not nums:
    errors.append("в отчёте нет чисел")

# 4. Проверка: запустим pytest и сравним summary
import subprocess
result = subprocess.run(
    ["python3", "-m", "pytest", "tests/", "-v", "--tb=no", "-q"],
    capture_output=True, text=True,
    cwd=str(ROOT),
    env={**__import__("os").environ, "ALL_PROXY": "", "all_proxy": ""}
)
lines = result.stdout.strip().split("\n")
last_line = lines[-1] if lines else ""
m = re.search(r'(\d+) passed', last_line)
expected_passed = int(m.group(1)) if m else None
m = re.search(r'(\d+) failed', last_line)
expected_failed = int(m.group(1)) if m else None

if expected_passed is not None:
    # Ищем "passed: N" или "N passed" или "passed (N)"
    pm = re.search(r'passed\s*[:\(]?\s*(\d+)', content, re.IGNORECASE)
    if pm:
        actual_passed = int(pm.group(1))
        if abs(actual_passed - expected_passed) > 2:
            errors.append(f"passed: в отчёте {actual_passed}, pytest показал {expected_passed}")
    else:
        errors.append("не найдено число passed в отчёте")

if expected_failed is not None and expected_failed > 0:
    fm = re.search(r'failed\s*[:\(]?\s*(\d+)', content, re.IGNORECASE)
    if fm:
        actual_failed = int(fm.group(1))
        if abs(actual_failed - expected_failed) > 2:
            errors.append(f"failed: в отчёте {actual_failed}, pytest показал {expected_failed}")
    else:
        errors.append("не найдено число failed в отчёте")

print("\n".join(errors) if errors else "принято: отчёт корректен")
sys.exit(1 if errors else 0)