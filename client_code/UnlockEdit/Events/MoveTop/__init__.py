from ._anvil_designer import MoveTopTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class MoveTop(MoveTopTemplate):
  def __init__(self, event_numbers, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    for event_number in event_numbers:
      event_button = Button(text=f'{event_number:02}', role='elevated-button', tag=event_number)
      event_button.set_event_handler('click', self.event_number_click)
      self.events_flow_panel.add_component(event_button)

  def event_number_click(self, **event_args):
    event_number = event_args['sender'].tag
    self.raise_event("x-close-alert", value=event_number)

    # Any code you write here will run before the form opens.
