
from models.events import Event
from data_base.db_connection.db import session
from sqlalchemy import func


def get_deadliest_attack_types(session, top_n=5):
    # שלב 1: חישוב סך הנפגעים (הרוגים כפול 2, פצועים כפול 1)
    session.query(
        Event.types,
        func.sum(
            (Event.killed * 2) + Event.wounded
        ).label('total_victims')
    )

    # שלב 2: מיון לפי סך הנפגעים
    query = session.query(
        Event.types,
        func.sum(
            (Event.killed * 2) + Event.wounded
        ).label('total_victims')
    ).group_by(Event.types).order_by(func.sum((Event.killed * 2) + Event.wounded).desc())

    # שלב 3: בחירת 5 סוגי התקפות הקטלניים ביותר (אם top_n=5)
    if top_n:
        query = query.limit(top_n)

    # שלב 4: ביצוע השאילתא
    result = query.all()

    return result


print(get_deadliest_attack_types(session))