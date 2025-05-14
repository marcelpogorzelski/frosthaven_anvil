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
    self.resource_repeating_panel.set_event_handler('x-update-total-gold', self.update_total_gold)
    self.get_total_gold()
    
    self.characters = app_tables.characters.search(tables.order_by('Gold', ascending=False), tables.order_by('Player', ascending=False))
    self.find_initial_values()
    #self.characters_repeating_panel.items = sorted(self.character_items, key=lambda x: x['Character']['Player'])
    self.characters_repeating_panel.set_event_handler('x-funds-updated', self.funds_updated)

    self.check_funds()
    

  def find_initial_values(self):
    self.character_items = [
      {'Character': character, 'Cost': 0, 'TotalGold': character['Gold']} for character in self.characters
    ]

    total = self.total_gold
    while total > 0:
      temp_total = total
      for character_item in self.character_items:
        if character_item['TotalGold'] == 0:
          continue
        character_item['Cost'] += 1
        character_item['TotalGold'] -= 1
        total -= 1
        if total == 0:
          break
      if temp_total == total:
        break

    self.characters_repeating_panel.items = sorted(self.character_items, key=lambda x: x['Character']['Player'])
    
  def get_total_gold(self):
    self.total_gold = 0
    for resource in self.resource_repeating_panel.items:
      self.total_gold += resource['Amount'] * 2
    self.total_gold_text_box.text = self.total_gold

  def update_total_gold(self, **event_args):
    self.get_total_gold()
    self.find_initial_values()
    self.check_funds()

  def check_funds(self):
    total_funds = 0
    for character_item in self.character_items:
      total_funds += character_item['Cost']
      
    if total_funds != self.total_gold:
      self.buy_button.enabled = False
    else:
      self.buy_button.enabled = True

  def funds_updated(self, **event_args):
    self.check_funds()

  def buy_button_click(self, **event_args):
    pass

