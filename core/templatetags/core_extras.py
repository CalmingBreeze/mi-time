import datetime
from collections import OrderedDict
from django import template
from django.utils.translation import npgettext

register = template.Library()

def duration( duration ):
# """
# Usage: {% duration timedelta %}
# Returns seconds duration as weeks, days, hours, minutes, seconds
# Based on core timesince/timeuntil
# """

    def seconds_in_units(seconds):
    # """
    # Returns a tuple containing the most appropriate unit for the
    # number of seconds supplied and the value in that units form.

    # >>> seconds_in_units(7700)
    # (2, 'hour')
    # """

        unit_totals = OrderedDict()

        unit_limits = [
                       (npgettext("Duration Operator","week","weeks",1), 7 * 24 * 3600),
                       (npgettext("Duration Operator","day","days",1), 24 * 3600),
                       (npgettext("Duration Operator","hour","hours",1), 3600),
                       (npgettext("Duration Operator","minute","minutes",1), 60),
                       (npgettext("Duration Operator","second","seconds",1), 1)
                        ]
    
        # unit_limits = [
        #                ("week", 7 * 24 * 3600),
        #                ("day", 24 * 3600),
        #                ("hour", 3600),
        #                ("minute", 60),
        #                ("second", 1)
        #                 ]

        for unit_name, limit in unit_limits:
            if seconds >= limit:
                amount = int(float(seconds) / limit)
                # if amount != 1:
                #     unit_name += 's' # dodgy pluralisation
                pluralized_unit_name = npgettext("Duration Operator", '%(name)s', '%(name)ss', amount) % { "name": unit_name }
                unit_totals[pluralized_unit_name] = amount
                seconds = seconds - ( amount * limit )
        return unit_totals


    if duration:
        if isinstance( duration, datetime.timedelta ):
            if duration.total_seconds() > 0:
                unit_totals = seconds_in_units( duration.total_seconds() )
                return ', '.join([str(v)+" "+str(k) for (k,v) in unit_totals.items()])

    return 'None'

register.filter("duration", duration)

def format_mobile_number(val, style):
    match style:
        case "dotted":
            separator = "."
            return "".join(val[0:2]+separator+val[2:4]+separator+val[4:6]+separator+val[6:8]+separator+val[8:10])
        case "spaced":
            separator = " "
            return "".join(val[0:2]+separator+val[2:4]+separator+val[4:6]+separator+val[6:8]+separator+val[8:10])
        case "i18n":
            return "+33"+val[1:]
        case _:
            return val

register.filter("phone_format", format_mobile_number)