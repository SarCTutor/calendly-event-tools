""" Main driver file for performing Calendly imports/exports. """
from dotenv import load_dotenv
import import_events as importer
import export_events as exporter
import resolve_names as names
import os

# Import the API key and URI.
load_dotenv()
api_key = os.getenv('CALENDLY_API_KEY')
user_uri = os.getenv('CALENDLY_URI')

# Flags for choosing what actions to perform. 
IMPORTING_CALENDLY = False 
IMPORTING_FILE = True
FIXING_NAMES = True
WRITING = True

if IMPORTING_CALENDLY:
    appts = importer.get_calendly_events(api_key, user_uri)
elif IMPORTING_FILE:
    appts = importer.read_event_csv("events_parsed.csv")

if WRITING:
    exporter.dicts_to_csv(appts)

if FIXING_NAMES:
    appts = names.resolve_names("events_parsed.csv")

if WRITING:
    exporter.dicts_to_csv(appts)

#exporter.csv_to_sql("events_parsed.csv")