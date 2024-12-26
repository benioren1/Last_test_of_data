from flask import Blueprint, jsonify, request
from sqlalchemy import func

from models import Location
from models.events import Event
from models.types import Types
from data_base.db_connection.db import session

# יצירת Blueprint
query_bp = Blueprint('attack', __name__)

# הגדרת הפונקציה לשליפת סוגי ההתקפות הקטלניות ביותר
@query_bp.route('/deadliest_attack_types', methods=['POST'])
def get_deadliest_attack_types():

    result = (session.query(
        Types.attacktype1_txt,
        func.sum((Event.wounded * 1) + (Event.killed * 2)).label('total_score')
    ).join(Event, Event.types_id == Types.types_id)
              .group_by(Types.attacktype1_txt).order_by(func.sum((Event.wounded * 1) + (Event.killed * 2))
                                                        .desc()).limit(5)).all()

    attack_types = [{'attack_type': attack_type, 'total_score': total_score} for attack_type, total_score in result]

    # החזרת התוצאה כ-JSON
    return jsonify(attack_types)

#פונקציה שמחזירה ממוצע של מספר נפגעים לפי איזור

@query_bp.route('/average_injuries_by_region', methods=['POST'])
def average_injuries_by_region():
    # פרמטר לבחירת Top-5 או כל הנתונים
    limit = request.json.get("limit", None)

    # ביצוע חישוב הממוצע לכל פיאיזור
    query = session.query(
        Location.region_txt,
        func.avg(Event.wounded + Event.killed).label('average_injuries')
    ).join(Location, Location.location_id == Event.location_id).group_by(Location.region_txt).order_by(func.avg(Event.wounded + Event.killed).desc())

    if limit:
        query = query.limit(limit)

    result = query.all()

    # ארגון התוצאה לפורמט JSON
    regions = [{'region': region, 'average_injuries': average_injuries} for region, average_injuries in result]

    return jsonify(regions)


@query_bp.route("/max_5_groups_injuries", methods=['POST'])
def max_5_groups_injuries():
    query = session.query(
        Event.gname,
        func.sum(func.coalesce(Event.wounded, 0) + func.coalesce(Event.killed, 0)).label('total_score')
    ).group_by(Event.gname).order_by(func.sum(func.coalesce(Event.wounded, 0) + func.coalesce(Event.killed, 0)).desc()).limit(5).all()

    groups = [
        {
            'group_name': group_name,
            'total_score': total_score
        }
        for group_name, total_score in query
    ]

    return jsonify(groups)



from flask import request, jsonify
from sqlalchemy import func, and_
from models import Event, Location  # import המודלים שלך

from sqlalchemy import func, case

@query_bp.route('/change_in_attacks', methods=['POST'])
def change_in_attacks():
    # קבלת הנתונים מהבקשה
    start_year = request.json.get('start_year')
    end_year = request.json.get('end_year')
    region = request.json.get('region')

    # אם חסר מידע כלשהו
    if not start_year or not end_year or not region:
        return jsonify({'error': 'יש למלא את כל השדות'}), 400

    # חישוב הפיגועים בשני השנים עבור האזור
    result = session.query(
        func.sum(Event.wounded + Event.killed).label('start_year_injuries')
    ).filter(Event.year == start_year, Location.region_txt == region).join(Location)\
    .first()

    start_year_injuries = result.start_year_injuries if result and result.start_year_injuries is not None else 0

    result = session.query(
        func.sum(Event.wounded + Event.killed).label('end_year_injuries')
    ).filter(Event.year == end_year, Location.region_txt == region).join(Location)\
    .first()

    end_year_injuries = result.end_year_injuries if result and result.end_year_injuries is not None else 0

    # חישוב אחוז השינוי
    if start_year_injuries > 0:
        percentage_change = ((end_year_injuries - start_year_injuries) / start_year_injuries) * 100
    else:
        percentage_change = 0

    # מחזירים את התוצאה
    return jsonify({
        'region': region,
        'start_year_injuries': start_year_injuries,
        'end_year_injuries': end_year_injuries,
        'percentage_change': percentage_change
    })


from sqlalchemy import func

@query_bp.route('/most_active_groups', methods=['POST'])
def most_active_groups():
    # קבלת הנתונים מהבקשה (אזור)
    region = request.json.get('region')

    # אם לא נבחר אזור, נחפש לכל האזורים
    if region:
        # חיפוש קבוצות טרור לפי אזור מסוים
        result = session.query(
            Event.gname,  # שם קבוצת הטרור
            func.count(Event.id).label('event_count')  # ספירת האירועים
        ).join(Location, Location.location_id == Event.location_id)\
         .filter(Location.region_txt == region)\
         .group_by(Event.gname)\
         .order_by(func.count(Event.id).desc())\
         .all()
    else:
        # אם לא נבחר אזור, נחפש את קבוצות הטרור הפעילות ביותר בכל האזורים
        result = session.query(
            Event.gname,  # שם קבוצת הטרור
            func.count(Event.id).label('event_count')  # ספירת האירועים
        ).group_by(Event.gname)\
         .order_by(func.count(Event.id).desc())\
         .all()

    # אם לא נמצאו קבוצות טרור
    if not result:
        return jsonify({'error': 'לא נמצאו קבוצות טרור פעילויות'}), 404

    # החזרת התוצאות
    active_groups = []
    for group_name, event_count in result:
        active_groups.append({
            'group_name': group_name,
            'event_count': event_count
        })

    return jsonify({'active_groups': active_groups})



