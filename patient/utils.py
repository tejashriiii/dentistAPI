from datetime import datetime


def get_age(birth_date):
    return datetime.now().year - birth_date.year
