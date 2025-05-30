from ._anvil_designer import EventTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from itertools import cycle

class Event(EventTemplate):
  def __init__(self, event_type, event_number, event_side, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.event_folder = app_files.events.get(event_type)

    event_card = self.get_event_card(f"{event_number}-{event_type}-{event_side}.png")
    
    other_side = "FrontBack".replace(event_side, '')
    other_event_card = self.get_event_card(f"{event_number}-{event_type}-{other_side}.png")
    
    self.event_card_name = cycle([event_card, other_event_card])
    self.next_event_card()

  def get_event_card(self, event_filename):
    return self.event_folder.get(event_filename)

  def next_event_card(self):
    self.event_image.source = next(self.event_card_name)

  def flip_button_click(self, **event_args):
    self.next_event_card()

    
