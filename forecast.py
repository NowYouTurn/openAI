import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict

# Mapping natal points to life spheres (in Russian)
SPHERES = {
    "Sun": "Личность, цели, жизненная энергия",
    "Moon": "Эмоции, семья, повседневное состояние",
    "Mercury": "Мышление, речь, логика",
    "Venus": "Отношения, финансы, симпатии",
    "Mars": "Действия, воля, конфликты",
    "Jupiter": "Возможности, удача, рост",
    "Saturn": "Ограничения, структура, зрелость",
    "Uranus": "Перемены, внезапные события",
    "Neptune": "Интуиция, иллюзии, вдохновение",
    "Pluto": "Сила, трансформация, контроль",
    "Ascendant": "Внешний облик, самоощущение, стиль",
}

@dataclass
class Transit:
    date: datetime
    aspect: str
    from_planet: str
    to_planet: str
    orb: float


def parse_line(line: str) -> Transit | None:
    """Parse a line from the input file and return a Transit object."""
    pattern = re.compile(
        r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
        r"(?P<aspect>\w+)\s+"
        r"(?P<from>[^\t]+)\s+->\s+"
        r"(?P<to>[^\t\s]+)\s+\(орб=(?P<orb>[-\d\.]+)"
    )
    m = pattern.match(line.strip())
    if not m:
        return None
    date = datetime.strptime(m.group("date"), "%Y-%m-%d").date()
    aspect = m.group("aspect")
    from_p = m.group("from")
    to_p = m.group("to")
    orb = float(m.group("orb"))
    return Transit(date=date, aspect=aspect, from_planet=from_p, to_planet=to_p, orb=orb)


def read_transits(path: str) -> List[Transit]:
    transits = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            tr = parse_line(line)
            if tr:
                transits.append(tr)
    return transits


def filter_and_sort(transits: List[Transit]) -> Dict[str, List[Transit]]:
    today = datetime.now().date()
    limit = today + timedelta(days=365)

    filtered = [t for t in transits if today <= t.date <= limit]
    filtered.sort(key=lambda t: abs(t.orb))

    groups: Dict[str, List[Transit]] = defaultdict(list)
    for t in filtered:
        groups[t.to_planet].append(t)

    for to_p in list(groups.keys()):
        groups[to_p].sort(key=lambda t: abs(t.orb))
        groups[to_p] = groups[to_p][:5]

    return groups


def format_forecast(groups: Dict[str, List[Transit]]) -> str:
    lines: List[str] = []
    for to_planet, transits in groups.items():
        sphere = SPHERES.get(to_planet, "")
        lines.append(f"{to_planet} – {sphere}")
        for tr in transits:
            sign = "+" if tr.orb >= 0 else "-"
            lines.append(
                f"{tr.date.isoformat()}: {tr.aspect} от {tr.from_planet} (орбис: {sign}{abs(tr.orb):.3f}°)"
            )
        lines.append("")
    return "\n".join(lines).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Астрологический прогноз по транзитам")
    parser.add_argument(
        "file",
        nargs="?",
        default="year_transits.txt",
        help="Путь к файлу с транзитами",
    )
    args = parser.parse_args()

    transits = read_transits(args.file)
    groups = filter_and_sort(transits)
    forecast = format_forecast(groups)
    print(forecast)


if __name__ == "__main__":
    main()
