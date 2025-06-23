from datetime import datetime, timedelta
from kerykeion import (
    AstrologicalSubject,
    EphemerisDataFactory,
    TransitsTimeRangeFactory,
)


def main():
    natal = AstrologicalSubject(
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

    for moment in transits_model.transits:
        print("Дата:", moment.date)
        for aspect in moment.aspects:
            print(
                f"{aspect.aspect} {aspect.p1_name} -> {aspect.p2_name} (орб={aspect.orbit})"
            )
        print("-" * 40)


if __name__ == "__main__":
    main()
