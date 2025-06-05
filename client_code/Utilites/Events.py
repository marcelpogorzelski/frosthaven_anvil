import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def get_next_event(event_type):
  event_entry = app_tables.events.get(Type=event_type)

  if event_entry['CurrentEvent']:
    return event_entry['CurrentEvent']

  active_list = event_entry['Active']
  current_event = active_list.pop(0)
  event_entry.update(Active=active_list, CurrentEvent=current_event)
  return current_event

def return_current_event(event_type):
  event_entry = app_tables.events.get(Type=event_type)

  current_event = event_entry['CurrentEvent']
  if not current_event:
    return

  active_list = event_entry['Active']
  active_list.append(current_event)

  previous_events = event_entry['PreviousEvents'] or list()
  previous_events.insert(0, current_event)

  event_entry.update(
    Active=active_list,
    CurrentEvent=None,
    PreviousEvents=previous_events
  )

def remove_current_event(event_type):
  event_entry = app_tables.events.get(Type=event_type)

  current_event = event_entry['CurrentEvent']
  if not event_entry['CurrentEvent']:
    return

  inactive_list = event_entry['Inactive']
  inactive_list.append(current_event)
  inactive_list.sort()

  previous_events = event_entry['PreviousEvents'] or list()
  previous_events.insert(0, current_event)

  event_entry.update(
    Inactive=inactive_list,
    CurrentEvent=None,
    PreviousEvents=previous_events
  )
