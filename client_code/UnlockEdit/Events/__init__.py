from ._anvil_designer import EventsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random
from .MoveTop import MoveTop


class Events(EventsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.events = {event_entry['Type']: {'event_entry': event_entry} for event_entry in app_tables.events.search()}

    self.setup_event_buttons()
    self.change_event_type('Summer Road')

  def change_event_type(self, event_type):
    self.event_entry = self.events[event_type]['event_entry']
    self.event_type = event_type
    self.add_label.text = f"Add {self.event_type} Event"
    self.remove_label.text = f"Remove {self.event_type} Event"
    self.inactive_flow_panel.clear()
    self.active_flow_panel.clear()
    self.populate_inactive()
    self.populate_active()

  def populate_inactive(self):
    for button in self.events[self.event_type]['inactive_buttons']:
      self.inactive_flow_panel.add_component(button)

  def populate_active(self):
    for button in self.events[self.event_type]['active_buttons']:
      self.active_flow_panel.add_component(button)

  def get_buttons(self, event_list, event_handler):
    button_list = list()
    for event_number in event_list:
      event_button = Button(text=f'{event_number:02}', role='elevated-button', tag=event_number)
      event_button.set_event_handler('click', event_handler)
      button_list.append(event_button)
    return button_list

  def setup_event_buttons(self):
    for event_type, event_info in self.events.items():
      event_entry = event_info['event_entry']
      inactive_buttons = self.get_buttons(event_entry['Inactive'], self.add_event)
      event_info['inactive_buttons'] = inactive_buttons

      active_buttons = self.get_buttons(sorted(event_entry['Active']), self.remove_event)
      event_info['active_buttons'] = active_buttons


  def add_event(self, **event_args):
    event_button = event_args['sender']
    event_number = event_button.tag

    if not confirm(f"Do you want to add {self.event_entry['Type']} Event {event_number:02}?"):
      return
    
    active_list = self.event_entry['Active']
    inactive_list = self.event_entry['Inactive']

    inactive_list.remove(event_number)
    active_list.append(event_number)
    random.shuffle(active_list)
    self.event_entry.update(Active=active_list, Inactive=inactive_list)

    active_button_list = self.events[self.event_type]['active_buttons']
    inactive_button_list = self.events[self.event_type]['inactive_buttons']

    inactive_button_list.remove(event_button)
    active_button_list.append(event_button)
    active_button_list.sort(key=lambda button: button.tag)

    self.change_event_type(self.event_type)

  def remove_event(self, **event_args):
    event_button = event_args['sender']
    event_number = event_button.tag

    if not confirm(f"Do you want to remove {self.event_entry['Type']} Event {event_number:02}?"):
      return

    active_list = self.event_entry['Active']
    inactive_list = self.event_entry['Inactive']

    active_list.remove(event_number)
    inactive_list.append(event_number)
    inactive_list.sort()
    self.event_entry.update(Active=active_list, Inactive=inactive_list)

    active_button_list = self.events[self.event_type]['active_buttons']
    inactive_button_list = self.events[self.event_type]['inactive_buttons']

    active_button_list.remove(event_button)
    inactive_button_list.append(event_button)
    inactive_button_list.sort(key=lambda button: button.tag)

    self.change_event_type(self.event_type)

  def event_radio_button_clicked(self, **event_args):
    self.change_event_type(event_args['sender'].text)

  def shuffle_button_click(self, **event_args):
    if not confirm(f"Do you want to shuffle {self.event_entry['Type']} Events Deck?"):
      return
    active_list = self.event_entry['Active']
    random.shuffle(active_list)
    self.event_entry['Active'] = active_list
    
    Notification(f"{self.event_entry['Type']} Event Deck is shuffled", timeout=6).show()


  def front_button_click(self, **event_args):
    active_list = self.event_entry['Active']
    event_number = alert(MoveTop(active_list), buttons=[("Cancel", None)])
    
    if not event_number:
      return
      
    active_list.remove(event_number)
    active_list.insert(0, event_number)

    self.event_entry['Active'] = active_list
    
    Notification(f"{self.event_entry['Type']} Event {event_number:02} is put on top of the Deck ", timeout=6).show()

    
    
