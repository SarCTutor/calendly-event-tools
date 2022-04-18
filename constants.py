from typing import Dict, List

""" Custom Defined Types

Event : Dict[str,str]
    Dictionary representing a single event.
    Required key(s): 'name'
    Created key(s): 'id'

Student : Dict[str,str]
    Dictionary representing a single student.
    All values are considered valid aliases for student.
    Required key(s): 'id'
"""
Event = Dict[str,str]
Student = Dict[str,str]

"""
Filenames
"""
REGULAR_EVENTS = "regular_events.csv"
LOOKUP_TABLE = "id_name.csv"