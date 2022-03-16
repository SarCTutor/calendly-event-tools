""" Provides functions for exporting event data to CSV and SQL.

Functions:
    csv_to_sql(str) : None
    get_calendly_events(str, str) : list(dict)
"""
import pandas, sqlite3, csv, os

def csv_to_sql(csvfile):
    """Exports a csvfile of events to the SQL database.

    Args:
        csvfile (str): the filename of the CSV to read from
    """
    filepath = os.path.abspath(os.getenv('SQL_PATH'))
    assert os.path.exists(filepath), "The file doesn't exist"
    conn = sqlite3.connect(filepath)
    df = pandas.read_csv(csvfile)
    df = df[["id", "datetime", "length"]]
    df.rename(columns={"id": "Student_ID", "datetime": "Date_Time", "length": "Length"}, inplace=True)
    df.drop(df[df.Student_ID == "Unknown"].index, inplace=True)
    return df.to_sql("Sessions", conn, if_exists='append', index=False)

def dicts_to_csv(events):
    """Write a list of dictionaries containing events to a CSV file.

    CSV Headers: 'name', 'time', 'date', 'day', 'datetime', 'length', 'type', 'uri', 'id'
    All other fields ignored.

    Args:
        events (list(dict)): a list of dicts representing one event each
    """
    event_fields = ['name', 'time', 'date', 'day', 'datetime', 'length', 'type', 'uri', 'id']
    eventfile = csv.DictWriter(open("events_parsed.csv", "w"), event_fields, extrasaction='ignore', restval="Unknown")
    eventfile.writeheader()
    for eventdict in events:
        eventfile.writerow(eventdict)
    return len(events)