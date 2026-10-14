"""Поиск статей arXiv по аппроксимации гессиана в оптимизации.

Использует инструменты недели 5 (week_5/artefacts/research_mcp.py): функции
_openalex/_brief/_provenance и фильтр по источнику arXiv (S4306400194).
Отправная точка — статьи в papers/:
  1711.05101 AdamW, 1802.09568 Shampoo, 2502.16982 Muon,
  2505.02809 Hessian Structure, 2603.00416 MuonRec.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import mcp.server.fastmcp as fm
fm.FastMCP.tool = lambda self, *a, **k: (lambda f: f)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "week_5" / "artefacts"))
import research_mcp as r  # noqa: E402

ARXIV_SOURCE = "S4306400194"
BRIEF = r.BRIEF_FIELDS


def arxiv_search(query: str, limit: int = 15, sort: str = "relevance"):
    """arXiv-only поиск через OpenAlex (неделя 5) с фильтром по источнику."""
    params = {
        "search": query,
        "filter": f"primary_location.source.id:{ARXIV_SOURCE}",
        "per_page": max(1, min(limit, 25)),
        "sort": r.SORT[sort],
        "select": BRIEF,
    }
    data, request = r._openalex("/works", params)
    return {
        "provenance": r._provenance("OpenAlex (arXiv only)", request),
        "query": query,
        "found": data.get("meta", {}).get("count"),
        "results": [r._brief(w) for w in data.get("results", [])],
    }


def main() -> None:
    queries = [
        "Hessian approximation optimizer neural network",
        "second-order optimization neural network Hessian",
        "Kronecker-factored approximate curvature K-FAC",
        "diagonal Hessian adaptive optimizer language model",
        "quasi-Newton deep learning optimizer",
        "preconditioned stochastic optimization Shampoo",
    ]
    all_hits: dict[str, dict] = {}
    for q in queries:
        try:
            out = arxiv_search(q, limit=15)
        except Exception as e:  # noqa: BLE001
            print(f"[ERR] {q}: {e}", file=sys.stderr)
            continue
        print(f"\n### {q}  (найдено в arXiv: {out['found']})")
        for w in out["results"]:
            print(f"  {w['year']} | цит. {w['cited_by']:>6} | {w['title']}  [{w['openalex_id']}]")
            all_hits[w["openalex_id"]] = w

    out_path = ROOT / "data" / "hessian_arxiv_candidates.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(list(all_hits.values()), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nВсего уникальных статей arXiv: {len(all_hits)} -> {out_path}")


if __name__ == "__main__":
    main()
