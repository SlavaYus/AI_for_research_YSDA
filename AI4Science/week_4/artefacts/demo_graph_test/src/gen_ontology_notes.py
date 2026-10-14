"""Generate ontology/<Класс>.md notes from ontology.yaml."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
ONT = ROOT / "ontology.yaml"
OUT = ROOT / "ontology"


def main() -> None:
    data = yaml.safe_load(ONT.read_text())
    classes = data["classes"]
    props = data["properties"]
    attrs = data["attributes"]

    OUT.mkdir(exist_ok=True)

    for name, spec in classes.items():
        parent = spec.get("parent")
        definition = spec["definition"].strip()

        # relations where this class is in domain
        rels = []
        for pname, pspec in props.items():
            dom = pspec["domain"]
            doms = dom if isinstance(dom, list) else [dom]
            if name in doms:
                rels.append(f"{pname}: {pspec['range']}")

        # attributes where this class is in domain
        ats = []
        for aname, aspec in attrs.items():
            if aspec["domain"] == name:
                ats.append(f"{aname}: {', '.join(aspec['values'])}")

        lines = [
            "---",
            "kind: класс",
            "---",
            f"# {name}",
            "",
            definition,
            "",
        ]
        if rels:
            lines.append("Отношения от этого класса: " + "; ".join(rels) + ".")
        else:
            lines.append("Отношения от этого класса: нет.")
        if ats:
            lines.append("Атрибуты: " + "; ".join(ats) + ".")
        else:
            lines.append("Атрибуты: нет.")
        lines.append("")
        lines.append("## Связи")
        if parent:
            lines.append(f"- подклассОт: [[{parent}]]")
        lines.append("")

        (OUT / f"{name}.md").write_text("\n".join(lines))

    print(f"generated {len(classes)} notes in {OUT}")


if __name__ == "__main__":
    main()