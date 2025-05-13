from ._anvil_designer import PassageOfTimeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PassageOfTime(PassageOfTimeTemplate):
  def __init__(self, week, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.item = week
    self.sections_repeating_panel.items = [section for section in self.item['Sections'].replace(' ', '').split(',')]
