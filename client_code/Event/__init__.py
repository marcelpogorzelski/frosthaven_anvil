from ._anvil_designer import EventTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Event(EventTemplate):
  def __init__(self, event_type, event_number, event_side, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    event_filename = f"{event_number}-{event_type}-{event_side}.png"
    self.event_image.source = app_files.events.get(event_type).get(event_filename)

    
