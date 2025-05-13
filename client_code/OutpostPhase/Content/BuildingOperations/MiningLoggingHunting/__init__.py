from ._anvil_designer import MiningLoggingHuntingTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class MiningLoggingHunting(MiningLoggingHuntingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.resource_repeating_panel.items = [
      {'Image': '_/theme/resource_images/fh-lumber-bw-icon.png', 'BuildingNumber': 17},
      {'Image': '_/theme/resource_images/fh-metal-bw-icon.png', 'BuildingNumber': 5},
      {'Image': '_/theme/resource_images/fh-hide-bw-icon.png', 'BuildingNumber': 12},
    ]
    self.resource_repeating_panel.set_event_handler('x-update-value', self.update_total_gold)
    self.get_total_gold()
    
    self.characters = app_tables.characters.search(tables.order_by('Gold', ascending=False), tables.order_by('Player', ascending=False))
    self.find_initial_values()
    self.characters_repeating_panel.items = sorted(self.character_items, key=lambda x: x['Character']['Player'])
    

  def find_initial_values(self):
    initialValue = int(self.total_gold / 4)
    remainder = self.total_gold % 4
    self.character_items = [
      {'Character': character, 'InitialValue': 0, 'TotalGold': character['Gold'], 'TempTotalGold': character['Gold']} for character in self.characters
    ]

    total = self.total_gold
    while total > 0:
      temp_total = total
      for character_item in self.character_items:
        if character_item['TempTotalGold'] == 0:
          continue
        character_item['InitialValue'] += 1
        character_item['TempTotalGold'] -= 1
        total -= 1
        if total == 0:
          break
      if temp_total == total:
        break
    
  def get_total_gold(self):
    self.total_gold = 0
    for resource in self.resource_repeating_panel.items:
      self.total_gold += resource['Amount'] * 2
    self.total_gold_text_box.text = self.total_gold

  def update_total_gold(self, **event_args):
    self.get_total_gold()

  def buy_button_click(self, **event_args):
    pass

