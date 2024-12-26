import pandas as pd

from sqlalchemy import func

from data_base.db_connection.db import session
from models import Event, Location


def load_data(path):
    df = pd.read_csv(path,
                     encoding='latin1')

    return df


def parse_date(date_str):
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    try:
        day, month_str, year_str = date_str.split('-')

        month = month_map[month_str]

        year = int(year_str)
        if year < 100:
            year = 1900 + year if year >= 25 else 2000 + year

        return {
            'year': year,
            'month': month,
            'day': int(day)
        }
    except (ValueError, KeyError) as e:
        return {
            'year': None,
            'month': None,
            'day': None
        }


def clean_and_save_event(row, city_id, group_id, attack_type_id, session=None):
    location = Location()


    try:
        date_parts = parse_date(row['Date'])

        new_event = Event(
            summary=row['Description'],
            killed=row['Fatalities'] if pd.notna(row['Fatalities']) else None,
            wounded=row['Injuries'] if pd.notna(row['Injuries']) else None,
            location_id = location_id,
            year=date_parts['year'],
            month=date_parts['month'],
            day=date_parts['day']
        )

        session.add(new_event)
        session.commit()
        session.refresh(new_event)

        return new_event.id

    finally:
        if should_close_session:
            session.close()


def convert_nan_to_none(row):
    for column in row.index:
        if pd.isna(row[column]):
            row[column] = None

    return row