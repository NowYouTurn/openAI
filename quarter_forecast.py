import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta

INPUT_FILE = "year_transits.txt"
SIGNIFICANT_ASPECTS = {"conjunction", "opposition", "square", "trine", "sextile"}
EXCLUDED_TRANSIT_POINTS = {"Moon", "Ascendant"}
MAX_ORB = 1.5

PATTERN = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2})\t"  # date
    r"(?P<aspect>\w+)\t"               # aspect
    r"(?P<from>[^\t]+)\t->\t"         # transit point
    r"(?P<to>[^\t]+)\s+\(орб=(?P<orb>[-\d\.]+)"  # natal point + orb
)


def load_transits(path: Path) -> pd.DataFrame:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = PATTERN.search(line)
        if not m:
            continue
        orb = float(m.group("orb"))
        records.append(
            {
                "date": pd.to_datetime(m.group("date")),
                "aspect": m.group("aspect"),
                "from_point": m.group("from").strip(),
                "to_point": m.group("to").strip(),
                "orb": orb,
                "abs_orb": abs(orb),
                "original_line": line,
            }
        )
    return pd.DataFrame(records)


def main(path: str = INPUT_FILE) -> None:
    df = load_transits(Path(path))

    today = datetime.today()
    q1_end = today + relativedelta(months=3)
    q2_end = today + relativedelta(months=6)
    q3_end = today + relativedelta(months=9)
    q4_end = today + relativedelta(months=12)

    df = df[(df["date"] >= today) & (df["date"] <= q4_end)]
    df = df[df["aspect"].isin(SIGNIFICANT_ASPECTS)]
    df = df[~df["from_point"].isin(EXCLUDED_TRANSIT_POINTS)]
    df = df[df["abs_orb"] <= MAX_ORB]
    df = df.sort_values(["date", "abs_orb"])

    quarters = {
        "I квартал": (today, q1_end),
        "II квартал": (q1_end, q2_end),
        "III квартал": (q2_end, q3_end),
        "IV квартал": (q3_end, q4_end),
    }

    for title, (start, end) in quarters.items():
        subset = df[(df["date"] >= start) & (df["date"] < end)]
        top_transits = subset.groupby("to_point").first().reset_index()
        print(f"\n\U0001F52E {title} ({start.date()} — {end.date()}):")
        if top_transits.empty:
            print("  — важных транзитов не найдено.")
        else:
            for _, row in top_transits.iterrows():
                print("  " + row["original_line"])


if __name__ == "__main__":
    main()
