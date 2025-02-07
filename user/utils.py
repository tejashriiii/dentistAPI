from datetime import datetime, time, date
from zoneinfo import ZoneInfo


def get_age(birth_date):
    return datetime.now().year - birth_date.year


def get_IST(utc_time):
    utc_datetime = datetime.combine(
        date.today(), utc_time, tzinfo=ZoneInfo("UTC"))
    return utc_datetime.astimezone(ZoneInfo("Asia/Kolkata")).time()
