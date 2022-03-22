""" Provides functions for exporting event data to CSV and SQL.

Functions:
    csv_to_sql(str) : int
    df_to_sql(pandas.df) : int
    dicts_to_csv(list[Event]) : int
"""
import pandas, sqlite3, csv, os
from constants import List, Event

def csv_to_sql(csvfile: str) -> int:
    """ Exports a csvfile of events to the SQL database.

    Args:
        csvfile : str
            The filename of the CSV to read from.

    Returns:
        int : The number of entries written to SQL.
    """
    filepath = os.path.abspath(os.getenv('SQL_PATH'))
    assert os.path.exists(filepath), "File at SQL_PATH doesn't exist"
    conn = sqlite3.connect(filepath)
    df = pandas.read_csv(csvfile)
    df = df[["id", "datetime", "length"]]
    df.rename(columns={"id": "Student_ID", "datetime": "Date_Time",\
        "length": "Length"}, inplace=True)
    df.drop(df[df.Student_ID == "Unknown"].index, inplace=True)
    return df.to_sql("Sessions", conn, if_exists='append', index=False)

def df_to_sql(df: pandas.DataFrame) -> int:
    """ Pushes a pandas DataFrame of Sessions to the SQL server 
    specified by SQL_PATH. 

    Args:
        df : pandas.df
            Data frame representing sessions.  
            Expected columns:
                Student_ID
                Date_Time
                Length

    Returns:
        int: The number of entries written to SQL.
    """
    filepath = os.path.abspath(os.getenv('SQL_PATH'))
    assert os.path.exists(filepath), "The file doesn't exist"
    conn = sqlite3.connect(filepath)
    return df.to_sql("Sessions", conn, if_exists='append', index=False)

def dicts_to_csv(events: List[Event]) -> int:
    """Write a list of dictionaries containing events to a CSV file.

    CSV Headers: 
        'name', 'time', 'date', 'day', 'datetime', 
        'length', 'type', 'uri', 'id'
    Any other keys ignored.

    Args:
        events : List[Event]
            A list of dictionaries representing one event each.
    
    Returns:
        int : The number of entries written to the CSV file.
    """
    event_fields = ['name', 'time', 'date', 'day', 'datetime', \
                    'length', 'type', 'uri', 'id']
    eventfile = csv.DictWriter(open("events_parsed.csv", "w"), event_fields,\
                               extrasaction='ignore', restval="Unknown")
    eventfile.writeheader()
    for eventdict in events:
        eventfile.writerow(eventdict)
    return len(events)