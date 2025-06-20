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
    self.get_used_perk_count()
    #self.perks_count_label.text = f"You have {count} out of {self.character['Perks']} Perks"
    total_perks = f"<span style=\"color:OliveDrab\">{self.character['Perks']}</span>"
    current_perks = f"<span style=\"color:OliveDrab\">{self.count}</span>"
    self.perks_rich_text.content =  f"You have selected {current_perks} out of {total_perks} Perks"

  

    self.perks_repeating_panel.items = self.perks_info
    self.perks_repeating_panel.set_event_handler('x-checkbox-change', self.checkbox_change)

  def get_used_perk_count(self):
    self.count = 0
    for perk_info in self.perks_info:
      self.count += sum(perk_info['dropboxes'])

  def checkbox_change(self, **event_args):
    self.character['PerksInfo'] = self.perks_info
    
