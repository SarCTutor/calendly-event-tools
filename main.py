""" Main driver file for performing Calendly imports/exports. """
from dotenv import load_dotenv
from simple_term_menu import TerminalMenu
import import_events as importer
import export_events as exporter
import resolve_names as names
import regular_events as regulars
import os

def main():
    # Import the API key and URI.
    load_dotenv()
    api_key = os.getenv('CALENDLY_API_KEY')
    user_uri = os.getenv('CALENDLY_URI')

    # Ask the user for data source.
    title1 = "Please Select Operations to Perform"
    choices = ["Retrieve from Calendly", 
               "Process names to IDs", 
               "Push new event entries to SQL",
               "Generate regular appointment entries"]
    menu = TerminalMenu(choices, 
                                 title=title1,
                                 clear_screen=True,
                                 multi_select=True,
                                 show_multi_select_hint=True, 
                                 multi_select_select_on_accept=False)
    
    chosen_entries = menu.show()
    
    if 0 in chosen_entries:
        print(f"\nProcessing Calendly imports...")
        appts = importer.get_calendly_events(api_key, user_uri)
        count = exporter.dicts_to_csv(appts)
        print(f"Wrote [{count}] events to [events_parsed.csv].")

    if 1 in chosen_entries:
        print(f"\nResolving names...\n")
        appts = names.resolve_names("events_parsed.csv")
        count = exporter.dicts_to_csv(appts)
        print(f"Wrote [{count}] events to [events_parsed.csv].")

    if 2 in chosen_entries:
        print(f"\nPushing events from [events_parsed.csv] to SQL...")
        count = exporter.csv_to_sql("events_parsed.csv")
        print(f"Pushed [{count}] new events to SQL database.")

    if 3 in chosen_entries:
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        print(f"\nPushing events from [events_parsed.csv] to SQL...")
        count = regulars.import_week(date_entry)
        print(f"Pushed [{count}] recurring events to SQL database.")

if __name__ == "__main__":
    main()

