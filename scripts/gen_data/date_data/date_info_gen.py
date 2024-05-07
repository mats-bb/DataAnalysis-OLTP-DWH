import datetime
# import calendar
import holidays
# import json


no_holidays = holidays.country_holidays('NO')

def get_all_dates(year):
    
    all_dates_year = [datetime.date(year, 1, 1) + datetime.timedelta(days=i) for i in range(366)]

    return all_dates_year


def get_last_date_by_month(year):

    last_date_by_month = []

    for month in range(1, 13): 

        if month == 12:
            last_day_of_month = datetime.date(year, month, 31)
        else:
            last_day_of_month = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        

        last_date_by_month.append(last_day_of_month)

    return last_date_by_month


def get_day_number_of_week(date):

    return date.weekday() + 1


def get_day_number_of_month(date):

    day_number = date.day
    return day_number


def get_day_number_of_year(date):
   
    return int(date.strftime("%j"))


def get_week_number_of_year(date):

    iso_year, iso_week, _ = date.isocalendar()

    return iso_week


def get_day_name(date):

    return date.strftime("%A")
    

def get_month_name(date):

    return date.strftime("%B")


def get_year(date):

    return date.year


def generate_date_list(year):
    
    date_rows = []
    all_dates = get_all_dates(year)
    
    for date_ in all_dates:
        d = {}

        d["date"] = str(date_)
        d["day_of_week"] = get_day_number_of_week(date_)
        d["day_of_month"] = get_day_number_of_month(date_)
        d["day_of_year"] = get_day_number_of_year(date_)
        d["week_number"] = get_week_number_of_year(date_)
        d["year"] = get_year(date_)
        d["name_of_day"] = get_day_name(date_)
        d["name_of_month"] = get_month_name(date_)

        if date_ in get_last_date_by_month(year):
            d["month_end_flag"] = "Month end"
        else:
            d["month_end_flag"] = "Not month end"

        if get_day_name(date_) in ["Saturday", "Sunday"]:
            d["weekday_flag"] = "Weekend"
        else:
            d["weekday_flag"] = "Weekday"

        if date_ in no_holidays:
            d["holiday_flag"] = "Holiday"
        else:
            d["holiday_flag"] = "Not holiday"

        date_rows.append(d)

    return date_rows
