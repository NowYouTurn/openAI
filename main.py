from kerykeion import AstrologicalSubject, Report


def main():
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


if __name__ == "__main__":
    main()
