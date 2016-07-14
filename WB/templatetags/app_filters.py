from django import template
from WB.models import *

register = template.Library()

@register.filter(name='get_due_date_string')
def get_country_string(value):
	countries = Indicator_Country.objects.all()

    delta = value - date.today()

    if delta.days == 0:
        return "Today!"
    elif delta.days < 1:
        return "%s %s ago!" % (abs(delta.days),
            ("day" if abs(delta.days) == 1 else "days"))
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days > 1:
        return "In %s days" % delta.days