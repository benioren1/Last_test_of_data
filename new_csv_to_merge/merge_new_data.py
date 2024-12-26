import pandas as pd
import requests
import csv
from sqlalchemy.orm import sessionmaker
from data_base.db_connection.db import engine, session  # הנח שההתחברות מתבצעת דרך engine שלך
from models import Event, Location
from models.types import Types
import time

# מפתח ה-API שלך ב-OpenCage
API_KEY = '8f115f04ffd44908b3b0ff9d242f428b'
csv_file = r"C:\Users\yyyy\PycharmProjects\Last_test_of_data\RAND_Database_of_Worldwide_Terrorism_Incidents - 5000 rows.csv"
# מיפוי שם חודש למספר
month_mapping = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}




# פונקציה לקבלת קואורדינטות מ-OpenCage
def get_lat_lon(city, country):
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={city},{country}&key={API_KEY}&language=en"
        response = requests.get(url)
        data = response.json()

        if data['results']:
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return lat, lon
        else:
            return None, None  # אם לא נמצא, נחזיר None
    except Exception as e:
        print(f"Error fetching coordinates for {city}, {country}: {e}")
        return None, None



# פונקציה למיפוי נתונים מה-CSV
def map_to_sqlalchemy(rows):
    for row in rows:
        try:
            # קבלת קואורדינטות באמצעות OpenCage
            lat, lon = get_lat_lon(row['City'], row['Country'])

            # יצירת או עדכון של רשומת Location
            location = Location(city=row['City'], country_txt=row['Country'], latitude=lat, longitude=lon)

            # הוספת הלוקציה לבסיס הנתונים (commit בנפרד)
            session.add(location)
            session.commit()  # התחייבות על כל לוקציה בנפרד

            # חלק את התאריך
            date_parts = row['Date'].split('-')
            day = int(date_parts[0])  # יום
            month_name = date_parts[1]  # שם החודש
            month = month_mapping.get(month_name, None)  # המרת שם החודש למספר
            year = int(date_parts[2])  # שנה

            if month is None:
                print(f"Invalid month format in row: {row['Date']}")
                continue

            # יצירת אירוע
            event = Event(
                year=year,
                month=month,
                day=day,
                summary=row['Description'],
                gname=row['Perpetrator'],
                killed=row['Fatalities'],
                wounded=row['Injuries'],
                location_id=location.location_id  # מפתח הלוקציה
            )

            # הוספת האירוע למסד הנתונים (commit בנפרד)
            session.add(event)
            session.commit()  # התחייבות על כל אירוע בנפרד

        except Exception as e:
            print(f"Error processing row: {row} - {e}")
            session.rollback()  # ביטול אם יש בעיה

# קריאה לקובץ ה-CSV והחזרת הנתונים על ידי שימוש ב-CSV reader
try:
    with open(csv_file, 'r', encoding='ISO-8859-1') as file:
        csv_reader = csv.DictReader(file)
        rows = []
        for row in csv_reader:
            rows.append(row)

        start_time = time.time()  # זמן התחלה
        map_to_sqlalchemy(rows)  # עיבוד כל השורות
        end_time = time.time()  # זמן סיום
        print(f"Total processing time: {end_time - start_time} seconds")



except FileNotFoundError:
    print(f"File {csv_file} not found.")
except Exception as e:
    print(f"Error reading CSV file: {e}")

# סגירת session
session.close()
