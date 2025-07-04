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
  def __init__(self, total_gold, event_handler=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.characters = app_tables.characters.search(tables.order_by('Gold', ascending=False), tables.order_by('Player', ascending=False))
    
    item_template = 'OutpostPhase.Content.BuildingOperations.CharacterPay.CharacterItemTemplate'
    self.character_pay_repeating_panel = RepeatingPanel(item_template=item_template)
    self.character_pay_repeating_panel.set_event_handler('x-update-gold', self.update_gold)
    self.add_component(self.character_pay_repeating_panel)
    self.event_handler = event_handler
    
    self.total_gold = total_gold
    self.setup_character_gold_pay()
    self.check_gold()

  def setup_character_gold_pay(self):
    self.character_items = [
      {'Character': character, 'Payment': 0, 'TotalGold': character['Gold'], 'Cost': self.total_gold} for character in self.characters
    ]

    character_total = reduce(lambda sum, character: sum + character['TotalGold'], self.character_items, 0)

    total = min(self.total_gold, character_total)

    for character_item in cycle(self.character_items):
      if total <= 0:
        break
      if character_item['TotalGold'] <= 0:
        continue
      character_item['Payment'] += 1
      character_item['TotalGold'] -= 1
      total -= 1

    self.character_pay_repeating_panel.items = sorted(self.character_items, key=lambda x: x['Character']['Player'])

  def update_total_gold(self, total_gold):
    self.total_gold = total_gold
    self.setup_character_gold_pay()
    self.check_gold()

  def check_gold(self):
    self.sum_gold = sum(gold_item['Payment'] for gold_item in self.character_pay_repeating_panel.items)
    
  def update_gold(self, **event_args):
    self.check_gold()
    if not self.event_handler:
      return
    self.raise_event(self.event_handler)

  def pay(self):
    for character_item in self.character_items:
      cost = character_item['Payment']
      if not cost:
        continue
      character = character_item['Character']
      character['Gold'] -= character_item['Payment']
    
