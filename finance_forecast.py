import argparse
from typing import Dict, List

import forecast

# Natal points associated with financial matters
FINANCE_POINTS = {"Venus", "Jupiter"}


def main(path: str = "year_transits.txt") -> None:
    """Print a financial forecast for the coming year."""
    transits = forecast.read_transits(path)
    groups = forecast.filter_and_sort(transits)

    finance_groups: Dict[str, List[forecast.Transit]] = {
        k: v for k, v in groups.items() if k in FINANCE_POINTS
    }

    if not finance_groups:
        print("Транзитов, относящихся к финансам, не найдено.")
        return

    print(forecast.format_forecast(finance_groups))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Финансовый прогноз по транзитам")
    parser.add_argument(
        "file",
        nargs="?",
        default="year_transits.txt",
        help="Путь к файлу с транзитами",
    )
    args = parser.parse_args()
    main(args.file)
