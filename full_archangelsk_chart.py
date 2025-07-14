from kerykeion import AstrologicalSubject, Report


def build_subject() -> AstrologicalSubject:
    """Create the natal chart subject for a woman born in Arkhangelsk."""
    return AstrologicalSubject(
        "Девушка из Архангельска",
        year=1999,
        month=1,
        day=17,
        hour=16,
        minute=35,
        city="Arkhangelsk",
        nation="RU",
        lat=64.5401,
        lng=40.5433,
        tz_str="Europe/Moscow",
    )


def main() -> None:
    subject = build_subject()
    report = Report(subject)
    print(report.get_full_report())


if __name__ == "__main__":
    main()
