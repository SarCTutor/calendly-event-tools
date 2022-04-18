""" Provides functionality for converting student names to IDs.

Functions:
    resolve_names(str) : list[Event]
"""
import csv
from constants import List, Event, Student, LOOKUP_TABLE
from simple_term_menu import TerminalMenu
from import_events import read_event_csv

def resolve_names(csvfile: str) -> List[Event]:
    """ Resolves student names into their corresponding unique IDs.  

    First, checks a lookup table of known names/aliases.
    If no match is found, the user is given a menu to select a student.

    Args:
        csvfile : str
            The file containing the event data to process.

    Returns:
        List[Event] : A list of dictionaries representing the processed 
                      event data.
    """
    events = read_event_csv(csvfile)
    students = _read_ids()
    
    for i in range(len(events)):
       events[i] = _resolve(events[i], students)
    _print_fails(events)
    _write_ids(students)
    return events

def _read_ids() -> List[Student]:
    """ Reads student IDs and known names from file. 
    
    Returns:
        List[Student] : A list of dictionaries with IDs and student aliases.
    """
    with open(LOOKUP_TABLE, "r") as f:
        students = list(csv.DictReader(f))
        return students

def _write_ids(students : List[Student]) -> None:
    """ Writes student IDs and known names to file. 
    Important because new names might have been learned.
    
    Args:
        students : List[Student]
            A list of dictionaries with IDs and student aliases.
    """
    keys = ['id', 'name', 'alt1', 'alt2', 'alt3', 'alt4', 'alt5']
    with open(LOOKUP_TABLE, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(students)

        
def _resolve(event: Event, students: List[Student]) -> Event:
    """ Resolves one event's student Name into an ID. 
    event['id'] is set to either:
        A matched student ID 
        "Unknown", if no ID matches
    """
    name = event['name']
    
    for i in range(len(students)):
        if name in students[i].values():
            event['id'] = students[i]['id']
            return event

    event['id'] = "Unknown"
    return _ask_user(event, students)

def _ask_user(event: Event, students: List[Student]) -> Event:
    """ Asks the user to identify the student in the given event. 
    Assigns "Unknown" if no ID is matched.
    """
    menu_title = f"Who is: [{event['name']}]? (ESC if Not Found)"
    guide_text = f"Press <j/k>, <arrows> for selection and <enter> to accept"

    # Set the event ID to "Unknown" by default.
    event['id'] = "Unknown"

    # Generate list of 10-student chunks as formatted strings.
    choice_strings = []
    for i in range(0, len(students)):
        id = int(students[i]['id'])
        choice_strings.append(f"[{id:02d}] {students[i]['name']}")
    choices_list=[choice_strings[i:i + 10] \
        for i in range(0, len(choice_strings), 10)]
    
    # Display a page of 10 students and try to find a match.
    page = 0
    for choices in choices_list:
        menu = TerminalMenu(choices, title=menu_title, status_bar=guide_text)
        chosen = menu.show()
        if chosen != None: # Match found!
            event['id']=int(chosen)+1+(10*page)
            print(f"Assigning {event['id']} to {event['name']}")
            _remember_match(event['id'], event['name'], students)
            break
        page += 1

    # Return the event.
    return event

def _print_fails(events : List[Event]) -> None:
    """ Prints out students who could not be matched to an ID number. """
    fails = []
    for event in events:
        if event['id'] == "Unknown":
            fails.append(event['name'])
    if len(fails) > 0:
        print(f"Couldn't match:")
        for fail in fails:
            print(f" - {fail}")

def _remember_match(id : int, alias : str, students : List[Student]) -> None:
    student = students[id-1]
    for i in range(1,6): 
        if not student["alt"+str(i)]:
            student["alt"+str(i)] = alias 
            print(f"Remembering that \"{alias}\" is {student['name']}\n")
            return
    print(f"{student['name']} is out of alias space!")