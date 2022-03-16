""" Provides functionality for converting student names to IDs.
See resolve_names() for more info.
"""
import csv
from import_events import read_event_csv

LOOKUP_TABLE = "id_name.csv"

def resolve_names(csvfile):
    """ Resolves student names into their corresponding unique IDs.  

    First, checks a lookup table of known names/aliases.
    If no match is found, the user is given a menu to select a student.

    Args:
        csvfile (str): The file containing the event data to process.

    Returns:
        list(dict): A list of dictionaries representing the processed event data.
    """
    events = read_event_csv(csvfile)
    students = _read_ids()
    
    for i in range(len(events)):
       events[i] = _resolve(events[i], students)
    _print_fails(events)
    return events

def _read_ids():
    """ Reads student IDs and known names from file. """
    with open(LOOKUP_TABLE, "r") as f:
        students = list(csv.DictReader(f))
        return students
        
def _resolve(event, students):
    """ Resolves one event's student Name into an ID. """
    name = event['name']
    
    for i in range(len(students)):
        if name in students[i].values():
            event['id'] = students[i]['id']
            return event

    event['id'] = "Unknown"
    return _ask_user(event, students)

def _ask_user(event, students):
    """ Asks the user to identify the student in the given event. """
    print("----------------")
    print(f"Who is: [{event['name']}] ?")
    for i in range(1,(len(students)//10 + 2)):
        stop = min((i*10)+1, len(students))
        _print_menu(students, i)
        response = input(f"Choice [{(i-1)*10+1}-{i*10}] >")
        if response == "n":
            continue
        elif int(response) in range((i-1)*10+1,stop):
            event['id']=int(response)
            break
    return event

def _print_menu(data, pagination=1):
    """ Prints a menu containing potential student names. """
    start = (10*(pagination-1))
    end = min(start + 10, len(data))
    print("----------------")
    for i in range(start, end):
        print(f"[{data[i]['id']}] {data[i]['name']}")
    print(f"\n[n] Next")
    print("----------------")

def _print_fails(events):
    """ Prints out a list of students who could not be matched to an ID number. """
    fails = []
    for event in events:
        if event['id'] == "Unknown":
            fails.append(event['name'])
    if len(fails) > 0:
        print(f"Couldn't match:")
        for fail in fails:
            print(f" - {fail}")