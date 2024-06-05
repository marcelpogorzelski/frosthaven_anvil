from ._anvil_designer import Character2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Character2(Character2Template):
  def __init__(self, player, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.player = player
    self.item = app_tables.characters.get(Player=self.player)
    # Any code you write here will run before the form opens.
