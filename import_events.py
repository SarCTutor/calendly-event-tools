""" Provides functions for importing event data from Calendly and CSV.

Functions:
    read_event_csv(str) : list(dict)
    get_calendly_events(str, str) : list(dict)
"""
from calendly import Calendly
from datetime import datetime
from dateutil import tz
import csv

def read_event_csv(csvfile):
    """Reads a csv file into a list of dictionaries, one dict per row,
    where the keys are the csv file's column names.        

    Args:
        csvfile (str): The name of the csv file to read from.

    Returns:
        list(dict): A list of dictionaries containing the csv's data.
    """
    with open(csvfile, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_calendly_events(api_key, user_uri):
    """Gets all current (not-cancelled) appointments from calendly
    and returns them as a list of dicts containing the event files.

    Args:
        api_key (str): the personal api_key used to authenticate with Calendly
        user_uri (str): the uri of the Calendly user to get events for

    Returns:
        list(dict): a list of dicts representing one event each
    """
    # Open a connection to Calendly and get raw data 
    calendly = Calendly(api_key)
    current_time = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    raw_events = calendly.list_events(user=user_uri, min_start_time=current_time)

    # Generate a list of dicts
    # 1 dict represents 1 event
    # Dict keys: "uri", "type", "time"
    parsed_events = []
    for eventdict in raw_events["collection"]:
        if (eventdict["status"] == 'active'):
            parsed_dict = {}
            parsed_dict["uri"] = eventdict["uri"]
            parsed_dict["type"] = eventdict["name"]
            parsed_dict["time"] = eventdict["start_time"]
            parsed_events.append(parsed_dict)

    # Add "name" key to event dicts by requesting invitee info from Calendly
    for i in range(len(parsed_events)):
        uri = parsed_events[i]["uri"].split("/")[-1]
        invitees = calendly.list_event_invitees(uri)
        parsed_events[i]["name"] = invitees["collection"][0]["name"]

    # Split the time field into time, date, day
    parsed_events = _fix_times(parsed_events)

    # Correct durations to be integers
    parsed_events = _fix_lengths(parsed_events)

    return parsed_events   

def _fix_times(events):
    """ Splits "time" key entries in ISO-8601 T/Z format into more readable 
    "date", "day", and "time" fields.

    Args:
        events (list(dict)): a list of dicts representing one event each 

    Returns:
        list(dict): a list of dicts representing one event each with added time info
    """
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ" 
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Canada/Mountain')
    for event in events:
        raw_time = event['time']
        time = datetime.strptime(raw_time, date_format)
        time = time.replace(tzinfo=from_zone)
        time = time.astimezone(to_zone)
        event['time'] = time.strftime("%-I:%M %p") 
        event['date'] = time.strftime("%F")
        event['day'] = time.strftime("%A")
        event['datetime'] = time.strftime('%F %H:%M:%S')
    return events

def _fix_lengths(events):
    """ Fixes the lengths to be just numbers. """
    for event in events:
        event['length'] = event['type'][:2]
    return events

def _write_raw_to_dict(events):
    """[Currently unused] Write raw input [calendly.list_events()] to a CSV file.
    
    CSV Headers: 'start_time', 'uri', 'event_type', 'status', 'name'.
    All other fields ignored.

    Args:
        events (dict(dict)): the raw result from calling calendly.list_events()
    """
    event_fields = ['start_time', 'uri', 'event_type', 'status', 'name']
    eventfile = csv.DictWriter(open("events_raw.csv", "w"), event_fields, extrasaction='ignore')
    eventfile.writeheader()
    for eventdict in events["collection"]:
        eventfile.writerow(eventdict)