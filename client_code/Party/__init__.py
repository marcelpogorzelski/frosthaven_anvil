from ._anvil_designer import PartyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Party(PartyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.item = app_tables.characters.get(Player='Marcel')
    #self.repeating_panel_1.items = app_tables.characters.search()
    self.item = app_tables.frosthaven.search()[0]
    self.characters_repeating_panel.items = app_tables.characters.search()

  def get_party_level(self):
    total_levels = 0
    for character in self.characters_repeating_panel.items:
      total_levels += character['Level']
    average_level = total_levels / 4

  