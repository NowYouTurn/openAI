# Astrology Example

This repository demonstrates basic usage of the [Kerykeion](https://pypi.org/project/kerykeion/) Python library for astrology. The example script prints a birth chart report for a sample person born in Taganrog, Russia.

## Setup

Install the dependency:

```bash
pip install kerykeion
```

## Running the example

```bash
python main.py
```

which executes the following code:

```python
from kerykeion import AstrologicalSubject, Report

subject = AstrologicalSubject(
    "Sample Person",
    year=1990,
    month=9,
    day=15,
    hour=13,
    minute=30,
    city="Taganrog",
    nation="RU",
    lat=47.23627,
    lng=38.9053,
    tz_str="Europe/Moscow",
)
report = Report(subject)
print(report.get_full_report())
```

### Sample output

```
+- Kerykeion report for Sample Person -+
+-----------+-------+--------------+-----------+----------+
| Date      | Time  | Location     | Longitude | Latitude |
| 15/9/1990 | 13:30 | Taganrog, RU | 38.9053   | 47.23627 |
...
```

This project is distributed under the terms of the AGPL-3.0 License. See [LICENSE](LICENSE) for details.
