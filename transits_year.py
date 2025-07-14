"""Generate or read a year's worth of astrological transits.

If ``year_transits.txt`` already exists, the script simply prints the
contents of that file. Otherwise the transits are computed using the
Kerykeion library and written to ``year_transits.txt`` for future use.

The output format matches the expectations of ``forecast.py``:

```
<date>\t<aspect>\t<transit point>\t->\t<natal point>\t(орб=<value>)
```

Only the first few lines are displayed when printing to avoid flooding
the console with tens of thousands of lines.
"""

from datetime import datetime, timedelta
from pathlib import Path

from kerykeion import (
    AstrologicalSubject,
    EphemerisDataFactory,
    Report,
    TransitsTimeRangeFactory,
)


def build_natal() -> AstrologicalSubject:
    """Return the natal chart for the Taganrog native."""

    return AstrologicalSubject(
        "Мужчина из Таганрога",
        year=1990,
        month=9,
        day=15,
        hour=13,
        minute=30,
        city="Taganrog",
        nation="Russia",
        lat=47.23627,
        lng=38.9053,
        tz_str="Europe/Moscow",
    )


def compute_transits(natal: AstrologicalSubject) -> list[str]:
    """Return a list of text lines with transit data for one year."""

    start = datetime.utcnow()
    end = start + timedelta(days=365)

    factory = EphemerisDataFactory(
        start_datetime=start,
        end_datetime=end,
        step_type="days",
        step=1,
        lat=natal.lat,
        lng=natal.lng,
        tz_str=natal.tz_str,
    )

    ephemeris_subjects = factory.get_ephemeris_data_as_astrological_subjects()
    transits_factory = TransitsTimeRangeFactory(natal, ephemeris_subjects)
    transits_model = transits_factory.get_transit_moments()

    lines: list[str] = []
    for moment in transits_model.transits:
        # ``moment.date`` is a string in ISO format ``YYYY-MM-DDTHH:MM:SS``
        # Keep only the date part so the output is stable.
        date = moment.date.split("T", 1)[0]
        for aspect in moment.aspects:
            lines.append(
                f"{date}\t{aspect.aspect}\t{aspect.p1_name}\t->\t{aspect.p2_name}\t(орб={aspect.orbit})"
            )

    return lines


def main() -> None:
    natal = build_natal()
    report = Report(natal)
    print(report.get_full_report())

    path = Path("year_transits.txt")

    if path.exists():
        lines = path.read_text().splitlines()
    else:
        lines = compute_transits(natal)
        path.write_text("\n".join(lines))

    # Print only the beginning of the file to avoid huge output
    for line in lines[:20]:
        print(line)


if __name__ == "__main__":
    main()
