import datetime
from . import models
from . import utils


def fetch_followups_by_date(date: datetime.datetime.date):
    """
    Returns list of all the followups for the given date
    """
    followups_for_date = models.FollowUp.objects.select_related(
        "complaint", "complaint__user", "complaint__user__details"
    ).filter(date=date)
    formatted_followups = []
    for followup in followups_for_date:
        formatted_followups.append(
            {
                "name": followup.complaint.user.name,
                "age": utils.get_age(followup.complaint.user.details.date_of_birth),
                "phonenumber": followup.complaint.user.phonenumber,
                "time": followup.time,
                "followup": followup.title,
            }
        )
    if not formatted_followups:
        return ["No followups today"]
    return formatted_followups
