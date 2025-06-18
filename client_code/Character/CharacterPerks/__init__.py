from ._anvil_designer import CharacterPerksTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CharacterPerks(CharacterPerksTemplate):
  def __init__(self, player_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.player_name = player_name
    self.character = app_tables.characters.get(Player=player_name)

    self.perks_info = self.character['PerksInfo']

    self.perks_repeating_panel.items = self.perks_info
    self.perks_repeating_panel.set_event_handler('x-checkbox-change', self.checkbox_change)

  def checkbox_change(self, **event_args):
    self.character['PerksInfo'] = self.perks_info
