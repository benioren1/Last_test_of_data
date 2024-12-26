from flask import Flask
from data_base.clean_db import load_data, clean_and_save_location, clean_and_save_types, clean_and_save_event
from data_base.db_connection.db import Base, engine, session
from blu_prints.query_routes import query_bp
app = Flask(__name__)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
# טעינת הנתונים
df = load_data('data_base/globalterrorismdb_0718dist-1000 rows.csv')

try:
    # עבור כל שורה ב-DataFrame, מבצע את הניקוי וההכנסה למסד הנתונים
    for _, row in df.iterrows():
        location = clean_and_save_location(row, session)
        types = clean_and_save_types(row, session)
        clean_and_save_event(row, types, location, session)
finally:
    # סגירת ה-session בסיום
    session.close()

app.register_blueprint(query_bp,url_prefix="/api")

if __name__ == '__main__':
    # הרצת Flask
    app.run(debug=True)
