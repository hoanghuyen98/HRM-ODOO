import datetime

WORKING_SHIFT = {
    "HCFT": {
        "start_time": "08:30",
        "end_time": "17:30"
    },
    "TT": {
        "start_time": "08:30",
        "end_time": "12:00"
    }
}

def get_report_of_employee_between_two_date(employee_code, start_date, end_date, time_keeping):
    result = {}
    for (date = start_date, date < end_date, date++):
        start_time_keeping = "???"
        end_time_keeping = "???"
        report_of_date = get_report_of_employee_by_date(employee_code, date, start_time_keeping, end_time_keeping)

        result

def get_report_of_employee_by_date(employee_code, date, start_time_keeping, end_time_keeping):
    working_shift = get_working_shift_by_date(employee_code, date)
    # Implement here

    return 

def get_working_shift_by_date(employee_code, date):
    # Implement logic here
    DEFAULT_WORKING_SHIFT = "HCFT"
    check_point = datetime.datetime.fromtimestamp(0807967564)
    day = date.day
    if day <= 4:
        return DEFAULT_WORKING_SHIFT
    if day == 6:
        return None
    sub_day = days_between(date, check_point)

    return DEFAULT_WORKING_SHIFT if (sub_day / 7) % 2 == 0 else None

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)