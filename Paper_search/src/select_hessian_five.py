"""Отбор 5 статей arXiv по аппроксимации гессиана и выгрузка PDF в papers/.

Опирается на отправные статьи проекта (papers/): AdamW (1711.05101), Shampoo
(1802.09568), Muon (2502.16982), Hessian Structure (2505.02809), MuonRec
(2603.00416). Метаданные — инструментом недели 5 research_mcp (OpenAlex).
PDF — открытые версии arXiv (только чтение внешних данных, запись в papers/).
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

import mcp.server.fastmcp as fm
fm.FastMCP.tool = lambda self, *a, **k: (lambda f: f)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "week_5" / "artefacts"))
import research_mcp as r  # noqa: E402

# 5 отобранных статей: OpenAlex id -> (arxiv id, к какой отправной статье тематически близка)
PICKS = {
    "W2155894447": ("1503.05671", "Shampoo 1802.09568; Hessian Structure 2505.02809"),
    "W4378509498": ("2305.14342", "AdamW 1711.05101; Muon 2502.16982; Hessian Structure 2505.02809"),
    "W4403707245": ("2409.11321", "Shampoo 1802.09568; Muon 2502.16982; AdamW 1711.05101"),
    "W3092641135": ("2010.04261", "Hessian Structure 2505.02809"),
    "W4287329019": ("2102.06737", "Shampoo 1802.09568; Hessian Structure 2505.02809"),
}

HEADERS = {"User-Agent": "AI4ScienceCourse/0.1 (research; hessian paper search)"}


def main() -> None:
    papers_dir = ROOT / "papers"
    records = []
    for wid, (arxiv_id, link) in PICKS.items():
        rec = json.loads(r.openalex_work(wid))["work"]
        rec["arxiv_id"] = arxiv_id
        rec["связь с papers/"] = link
        records.append(rec)
        print(f"\n### {rec['title']}  (arXiv:{arxiv_id}, {rec['year']}, цит. {rec['cited_by']})")
        print(f"    авторы: {', '.join(a['name'] for a in rec.get('authors', [])[:4])}")
        print(f"    DOI: {rec['doi']}  |  OA: {rec['oa_status']}")
        print(f"    связь: {link}")
        print(f"    аннотация: {(rec.get('abstract') or 'нет')[:300]}…")

        pdf = papers_dir / f"{arxiv_id}.pdf"
        if not pdf.exists():
            url = f"https://arxiv.org/pdf/{arxiv_id}"
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = resp.read()
                if data[:4] == b"%PDF":
                    pdf.write_bytes(data)
                    print(f"    PDF сохранён: papers/{pdf.name} ({len(data)//1024} КБ)")
                else:
                    print(f"    PDF не сохранён: получен не PDF ({len(data)} байт)")
            except Exception as e:  # noqa: BLE001
                print(f"    PDF не сохранён: {type(e).__name__}: {e}")
        else:
            print(f"    PDF уже есть: papers/{pdf.name}")

    out = ROOT / "data" / "hessian_five.json"
    out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nЗаписи сохранены: {out}")


if __name__ == "__main__":
    main()
