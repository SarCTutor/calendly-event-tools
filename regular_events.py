""" File for adding recurring appointments to the SQL database.  

Unrelated to Calendly, but useful for my setup. """
import pandas, sqlite3, os
import resolve_names as names
import datetime as dt
from datetime import datetime 

REGULAR_EVENTS = "regular_events.csv"

def import_week(week=None):
    appts = names.resolve_names(REGULAR_EVENTS)
    _generate_dates(appts, week)
    _generate_times(appts)
    df = pandas.DataFrame(appts)
    df = df[["id", "datetime", "length"]]
    df.rename(columns={"id": "Student_ID", "datetime": "Date_Time", "length": "Length"}, inplace=True)
    df.drop(df[df.Student_ID == "Unknown"].index, inplace=True)
    df.dropna(inplace=True)
    count = _to_sql(df)
    print(f"Pushed {count} appointments to server.")

def _generate_times(appts):
    for apt in appts:
        apt['datetime'] = _generate_time(apt)

def _generate_time(apt):
    if apt['date'] == None:
        return None
    else:
        date = datetime.strptime(apt['date'], "%Y-%m-%d")
        time = datetime.strptime(apt['time'], "%H:%M") - datetime.strptime("00:00", "%H:%M")
        combined = date + time
        return combined.strftime("%F %H:%M:%S")

def _generate_dates(appts, week=None):
    if week == None:
        start = datetime.today()
    else:
        start = datetime.strptime(week, "%Y-%m-%d")
    end = start + dt.timedelta(days=6) - dt.timedelta(days=start.weekday())
    
    print(f"Generating from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    for apt in appts:
        apt['date'] = _get_day(start, apt['day'])


def _to_sql(df):
    """ Pushes a pandas DataFrame to the SQL server specified by SQL_PATH. 
    Expected columns: Student_ID, Date_Time, Length """
    filepath = os.path.abspath(os.getenv('SQL_PATH'))
    assert os.path.exists(filepath), "The file doesn't exist"
    conn = sqlite3.connect(filepath)
    return df.to_sql("Sessions", conn, if_exists='append', index=False)

def _get_day(start, day):
    day_num = _day_num(day)
    time = start + dt.timedelta(days=day_num) - dt.timedelta(days=start.weekday())
    if time >= start:
        #print(f"time: {time}, day: {day}, num: {day_num}")
        return time.strftime("%Y-%m-%d")
    else:
        return None


def _day_num(day):
    if day == "Monday":
        return 0
    elif day == "Tuesday":
        return 1
    elif day == "Wednesday":
        return 2
    elif day == "Thursday":
        return 3
    elif day == "Friday":
        return 4
    elif day == "Saturday":
        return 5
    elif day == "Sunday":
        return 6
    else:
        raise ValueError(f"Bad Day String: {day}")
    
