from ._anvil_designer import RetiredCharactersTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RetiredCharacters(RetiredCharactersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.retired_characters_repeating_panel.items = app_tables.retired_characters.search()
    # Any code you write here will run before the form opens.
