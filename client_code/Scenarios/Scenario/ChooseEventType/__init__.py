from ._anvil_designer import ChooseEventTypeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ChooseEventType(ChooseEventTypeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def choose_event_button_click(self, **event_args):
    event_type = event_args['sender'].text
    self.raise_event("x-close-alert", value=event_type)
