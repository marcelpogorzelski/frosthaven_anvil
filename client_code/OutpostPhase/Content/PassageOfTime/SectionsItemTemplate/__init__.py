from ._anvil_designer import SectionsItemTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator


class SectionsItemTemplate(SectionsItemTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
  def section_button_click(self, **event_args):
    navigator.clipboard.writeText(self.section_button.text)
    self.section_button.role = 'tonal-button'
    self.item['Clicked'] = True
    self.parent.raise_event('x-section-clicked')
