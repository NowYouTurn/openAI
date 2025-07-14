# Astrology Example

This repository demonstrates basic usage of the [Kerykeion](https://pypi.org/project/kerykeion/) Python library for astrology. The example script prints a birth chart report for a sample person born in Taganrog, Russia. A second script can generate (or reuse) a full year of planetary transits.

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

### Yearly transit data

To generate or view a year's worth of planetary transits run:

```bash
python transits_year.py
```

The script writes the results to `year_transits.txt` if the file does not
already exist. The file uses tab-separated columns so it can be fed
directly into `forecast.py`. Only the beginning of the file is printed to
avoid flooding the console.

### Building a yearly forecast

To create a text forecast from a file of transit data, use `forecast.py`.
The script expects the input in the following format:

```
<дата>\t<аспект>\t<транзитная точка>\t->\t<натальная точка>\t(орб=<значение>)
```

Run the script with the file path as an argument (by default it looks for
`year_transits.txt`):

```bash
python forecast.py
```

It filters the transits for the coming year, groups them by natal point and
prints up to five with the smallest orbs for each point.

To build a forecast focused specifically on finances, use `finance_forecast.py`:

```bash
python finance_forecast.py
```

### Sample output

```
+- Kerykeion report for Sample Person -+
+-----------+-------+--------------+-----------+----------+
| Date      | Time  | Location     | Longitude | Latitude |
| 15/9/1990 | 13:30 | Taganrog, RU | 38.9053   | 47.23627 |
...
```

### Example: Arkhangelsk birth chart

To build a chart for someone born in Arkhangelsk on 17 January 1999 at 16:35,
run:

```bash
python arkhangelsk_chart.py
```


This project is distributed under the terms of the AGPL-3.0 License. See [LICENSE](LICENSE) for details.
