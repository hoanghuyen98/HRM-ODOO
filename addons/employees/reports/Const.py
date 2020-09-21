from odoo import models
import calendar
import pytz
from odoo import models, fields, api,  _
from datetime import datetime, date
DAY_MAP = {
    0: "Thứ 2",
    1: "Thứ 3",
    2: "Thứ 4",
    3: "Thứ 5",
    4: "Thứ 6",
    5: "Thứ 7",
    6: "Chủ nhật"
}

def _get_day_of_date(date):

    if date :
        date_day = date.weekday()
        return DAY_MAP[date_day]
    return 0

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