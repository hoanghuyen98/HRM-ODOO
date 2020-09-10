from odoo import models
import calendar
import pytz
from odoo import models, fields, api,  _
from datetime import datetime, date

def _get_day_of_date(date):

    if date :
        selected = fields.Datetime.from_string(date)
        date_day = calendar.day_name[selected.weekday()]
        if date_day == "Monday":
            date_day = "Thứ 2"
        if date_day == "Tuesday":
            date_day = "Thứ 3"
        if date_day == "Wednesday":
            date_day = "Thứ 4"
        if date_day == "Thursday":
            date_day = "Thứ 5"
        if date_day == "Friday":
            date_day = "Thứ 6"
        if date_day == "Saturday":
            date_day = "Thứ 7"
        if date_day == "Sunday":
            date_day = "Chủ nhật" 
    return date_day

def number_of_days(m, y):
    leap = 0
    if y% 400 == 0:
        leap = 1
    elif y % 100 == 0:
        leap = 0
    elif y% 4 == 0:
        leap = 1
    if m==2:
        return 28 + leap
    list = [1,3,5,7,8,10,12]
    if m in list:
        return 31
    return 30