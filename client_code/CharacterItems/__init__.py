from ._anvil_designer import CharacterItemsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CharacterItems(CharacterItemsTemplate):
  def __init__(self, player,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_1.text = f"Items for {player}"

    # Any code you write here will run before the form opens.
