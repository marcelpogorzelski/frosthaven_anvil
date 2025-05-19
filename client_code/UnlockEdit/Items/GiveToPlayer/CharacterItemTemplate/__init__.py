from ._anvil_designer import CharacterItemTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CharacterItemTemplate(CharacterItemTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.give_button.text = self.item['Player']


  def give_button_click(self, **event_args):
    self.parent.parent.raise_event("x-close-alert", value=self.item)
