from datetime import datetime, date

WORKING_SHIFT = {
    "HCFT": {
        "start_time": 8.5,
        "end_time": 17.5
    },
    "TT": {
        "start_time": 8.5,
        "end_time": 12
    }
}

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_report_of_employee_between_two_date(employee_code, start_date, end_date, time_keeping):
    result = {}
    for single_date in daterange(start_date, end_date):
        start_time_keeping = "???"

        end_time_keeping = "???"
        report_of_date = get_report_of_employee_by_date(employee_code, date, start_time_keeping, end_time_keeping)

        result[date] = report_of_date
    return result

def get_report_of_employee_by_date(employee_code, date, start_time_keeping, end_time_keeping):
    working_shift = get_working_shift_by_date(employee_code, date)
    shift = 0
    for sch in WORKING_SHIFT:
        if sch==working_shift:
            start_time = WORKING_SHIFT[sch]['start_time']
            end_time = WORKING_SHIFT[sch]['end_time']
            if (start_time <= start_time_keeping)  and (end_time >= float(end_time_keeping)):
                shift = 1
            else:
                shift = 0.5
         
    return shift
    
def get_working_shift_by_date(employee_code, date):

        # Implement logic here
        # scheduler_query = """
        #     SELECT * FROM employees_scheduler 
        #     """
        # request.cr.execute(scheduler_query)
        # scheduler_query_obj = request.cr.fetchall() 

        for sche in WORKING_SHIFT:
            if sche == 'HCFT':
                DEFAULT_WORKING_SHIFT = sche
                check_point = "2020/09/18"
                # check_point = datetime.datetime.fromtimestamp(0807967564)
                day = date.weekday()

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