import pandas as pd
from models.events import Event

from models.location import Location
from models.types import Types

required_columns = ['iyear', 'imonth', 'iday', 'latitude', 'longitude', 'summary', 'gname', 'attacktype1', 'nperps',
                    'attacktype1_txt', 'targtype1', 'targtype1_txt', 'nkill', 'nwound', 'region', 'region_txt',
                    'country', 'country_txt', 'city'
                    ]


def load_data(path):
    df = pd.read_csv(path,
                     encoding='latin1',
                     usecols=required_columns)

    return df


def clean_and_save_location(row, session):

    location = Location(
        latitude=float(row['latitude']) if pd.notna(row['latitude']) else None,
        longitude=float(row['longitude']) if pd.notna(row['longitude']) else None,
        country=row['country'],
        country_txt=row['country_txt'],
        city=row['city'],
        region=row['region'],
        region_txt=row['region_txt']
    )

    session.add(location)
    session.commit()
    session.refresh(location)

    return location.location_id



def clean_and_save_types(row, session):
    # חפש אם ה-Type כבר קיים לפי attacktype1 ו- targtype1
    type = session.query(Types).filter(Types.attacktype1 == int(row['attacktype1']),
                                        Types.targtype1 == int(row['targtype1'])).first()

    # אם לא קיים, צור Type חדש
    if not type:
        type = Types(
            attacktype1=int(row['attacktype1']),
            attacktype1_txt=row['attacktype1_txt'],
            targtype1=int(row['targtype1']),
            targtype1_txt=row['targtype1_txt']
        )
        session.add(type)
        session.commit()
        session.refresh(type)

    return type.types_id


def clean_and_save_event(row,types_id,location_id, session):
    if row['iyear'] <= 0:
        row['iyear'] = None

    if row['imonth'] <= 0:
        row['imonth'] = None

    if row['iday'] <= 0:
        row['iday'] = None

    if pd.isna(row['nkill']) or row['nkill'] < 0:
        row['nkill'] = None

    if pd.isna(row['nwound']) or row['nwound'] < 0:
        row['nwound'] = None

    if pd.isna(row['nperps']) or row['nperps'] < 0:
        row['nperps'] = None

    event = Event(
        year=int(row['iyear']) if pd.notna(row['iyear']) else None,
        month=int(row['imonth']) if pd.notna(row['imonth']) else None,
        day=int(row['iday']) if pd.notna(row['iday']) else None,
        summary=row['summary'] if pd.notna(row['summary']) else None,
        nperps=float(row['nperps']) if pd.notna(row['nperps']) else None,
        killed=float(row['nkill']) if pd.notna(row['nkill']) else None,
        wounded=float(row['nwound']) if pd.notna(row['nwound']) else None,
        gname=row['gname'],
        location_id = location_id,
        types_id=types_id

    )
    session.add(event)
    session.commit()


def convert_nan_to_none(row):
    for column in row.index:
        if pd.isna(row[column]):
            row[column] = None

    return row