""" Main driver file for performing Calendly imports/exports. """
from dotenv import load_dotenv
import import_events as importer
import export_events as exporter
import resolve_names as names
import regular_events as regulars
import os

# Import the API key and URI.
load_dotenv()
api_key = os.getenv('CALENDLY_API_KEY')
user_uri = os.getenv('CALENDLY_URI')

# Flags for choosing what actions to perform. 
IMPORTING_CALENDLY = False 
FIXING_NAMES = False
UPDATE_DB = False
REGULAR_IMPORTS = False
REGULAR_DATE = "2022-03-28"

if IMPORTING_CALENDLY:
    appts = importer.get_calendly_events(api_key, user_uri)
    exporter.dicts_to_csv(appts)
else:
    appts = importer.read_event_csv("events_parsed.csv")

if FIXING_NAMES:
    appts = names.resolve_names("events_parsed.csv")
    exporter.dicts_to_csv(appts)

if UPDATE_DB:
    exporter.csv_to_sql("events_parsed.csv")

if REGULAR_IMPORTS:
    regulars.import_week(REGULAR_DATE)