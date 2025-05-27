from ._anvil_designer import CharacterPayTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from itertools import cycle
from functools import reduce

class CharacterPay(CharacterPayTemplate):
  def __init__(self, total_gold, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.characters = app_tables.characters.search(tables.order_by('Gold', ascending=False), tables.order_by('Player', ascending=False))
    
    item_template = 'OutpostPhase.Content.BuildingOperations.CharacterPay.CharacterItemTemplate'
    self.character_pay_repeating_panel = RepeatingPanel(item_template=item_template)
    self.add_component(self.character_pay_repeating_panel)
    
    self.total_gold = total_gold
    self.setup_character_gold_pay()


  def setup_character_gold_pay(self):
    self.character_items = [
      {'Character': character, 'Payment': 0, 'TotalGold': character['Gold'], 'Cost': self.total_gold} for character in self.characters
    ]

    character_total = reduce(lambda sum, character: sum + character['TotalGold'], self.character_items, 0)
    #character_total = int(character_total / 2) * 2

    total = min(self.total_gold, character_total)

    for character_item in cycle(self.character_items):
      if character_item['TotalGold'] <= 0:
        continue
      character_item['Payment'] += 1
      character_item['TotalGold'] -= 1
      total -= 1
      if total <= 0:
        break

    self.character_pay_repeating_panel.items = sorted(self.character_items, key=lambda x: x['Character']['Player'])
