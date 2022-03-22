""" File for adding recurring appointments to the SQL database.  
Uses a CSV file to read in the regular event days and times.

Unrelated to Calendly, but useful for a setup in which
regular standing appointments exist in addition to Calendly. """

import pandas
import resolve_names as names
import export_events as exporter
import datetime as dt
from constants import List, Event, REGULAR_EVENTS

def import_week(week: str) -> int:
    """Generates a week of recurring events and starting at 
    the specified date, and pushes them to the SQL database.

    Args:
        week : str
            String for start date (inclusive) "YYYY-MM-DD" format

    Returns:
        int: Number of entries written to the SQL server.
    """
    appts = names.resolve_names(REGULAR_EVENTS)
    _generate_dates(appts, week)
    _generate_datetimes(appts)
    
    # Convert to df and fix formatting for SQL
    df = pandas.DataFrame(appts)
    df = df[["id", "datetime", "length"]]
    df.rename(columns={"id": "Student_ID", 
                 "datetime": "Date_Time", 
                   "length": "Length"}, inplace=True)
    df.drop(df[df.Student_ID == "Unknown"].index, inplace=True)
    df.dropna(inplace=True)

    # Push to SQL
    return exporter.df_to_sql(df)

def _generate_datetimes(appts: List[Event]) -> None:
    """ Generate 'datetime' entries in form "YYYY-MM-DD HH:MM" 
    Requires 'date' to already be filled (run _generate_dates()) """
    for apt in appts:
        apt['datetime'] = _generate_datetime(apt)

def _generate_datetime(apt: Event) -> str:
    """ Generate 'datetime' entry for a single appointment. 
    Returns None if 'date' is not set. """
    if apt['date'] == None:
        return None
    else:
        date = dt.datetime.strptime(apt['date'], "%Y-%m-%d")
        time = dt.datetime.strptime(apt['time'], "%H:%M") \
                - dt.datetime.strptime("00:00", "%H:%M")
        combined = date + time
        return combined.strftime("%F %H:%M:%S")

def _generate_dates(appts: List[Event], start: str) -> None:
    """ Generate 'date' entry for all appointments starting
    with on the specified start date ("YYYY-MM-DD"). """
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = start + dt.timedelta(days=6) - dt.timedelta(days=start.weekday())
    
    print(f"Generating events from {start.strftime('%Y-%m-%d')} \
            to {end.strftime('%Y-%m-%d')}")
    for apt in appts:
        apt['date'] = _get_day(start, apt['day'])

def _get_day(start_date: dt.datetime, day: str) -> str:
    """ Find the next weekday 'day' from date 'start'. 
    
    Returns:
        str : the YYYY-MM-DD string representing the day's date
    """
    day_num = _day_num(day)
    time = start_date + dt.timedelta(days=day_num) \
            - dt.timedelta(days=start_date.weekday())
    if time >= start_date:
        return time.strftime("%Y-%m-%d")
    else:
        return None

def _day_num(day: str) -> int:
    """ Convert weekday string to int (0:Monday ... 6:Sunday) """
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
