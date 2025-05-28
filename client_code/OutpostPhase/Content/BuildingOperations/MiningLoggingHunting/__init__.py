from ._anvil_designer import MiningLoggingHuntingTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from itertools import cycle
from functools import reduce

class MiningLoggingHunting(MiningLoggingHuntingTemplate):
  def __init__(self, gamestate, finish_phase_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.finish_phase_tag = finish_phase_tag
    self.gamestate = gamestate

    self.finished = gamestate[finish_phase_tag]
    if self.finished:
      self.disable_phase()

    self.resource_repeating_panel.items = [
      {'Image': '_/theme/resource_images/fh-lumber-bw-icon.png', 'BuildingNumber': 17, 'Resource': 'Lumber'},
      {'Image': '_/theme/resource_images/fh-metal-bw-icon.png', 'BuildingNumber': 5, 'Resource': 'Metal'},
      {'Image': '_/theme/resource_images/fh-hide-bw-icon.png', 'BuildingNumber': 12, 'Resource': 'Hide'},
    ]
    self.resource_repeating_panel.set_event_handler('x-update-total-gold', self.update_total_gold)
    self.get_total_gold()
    
    self.characters = app_tables.characters.search(tables.order_by('Gold', ascending=False), tables.order_by('Player', ascending=False))
    self.find_initial_values()
    self.characters_repeating_panel.set_event_handler('x-funds-updated', self.funds_updated)

    self.check_funds()

  def disable_phase(self):
    self.building_operations_column_panel.background = 'theme:Outline'
    self.characters_repeating_panel.visible = False
    self.resource_repeating_panel.visible = False
    self.buy_flow_panel.visible = False
    self.name_label.text += " - Finished"

  def set_as_finished(self):
    self.disable_phase()
    self.finished = True
    self.gamestate[self.finish_phase_tag] = True
    self.raise_event('x-building-finished')

  def find_initial_values(self):
    self.character_items = [
      {'Character': character, 'Cost': 0, 'TotalGold': character['Gold']} for character in self.characters
    ]

    character_total = reduce(lambda sum, character: sum + character['TotalGold'], self.character_items, 0)
    character_total = int(character_total / 2) * 2
    
    total = min(self.total_gold, character_total)
    
    for character_item in cycle(self.character_items):
      if character_item['TotalGold'] <= 0:
        continue
      character_item['Cost'] += 1
      character_item['TotalGold'] -= 1
      total -= 1
      if total <= 0:
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
    frosthaven = app_tables.frosthaven.search()[0]
    resource_amounts = dict()
    for resource in self.resource_repeating_panel.items:
      resource_amounts[resource['Resource']] = resource['Amount']

    lumber = frosthaven['Lumber'] + resource_amounts['Lumber']
    metal = frosthaven['Metal'] + resource_amounts['Metal']
    hide = frosthaven['Hide'] + resource_amounts['Hide']

    frosthaven.update(
      Lumber=lumber,
      Metal=metal,
      Hide=hide
    )

    notification_text = "Added:"
    for resource, amount in resource_amounts.items():
      if not amount:
        continue
      notification_text += f"\n  {resource}: {amount}"

    notification_text += "\nPaying:"

    for character_item in self.character_items:
      cost = character_item['Cost']
      if not cost:
        continue
      character = character_item['Character']
      notification_text += f"\n  {character['Player']}: {cost} Gold"
      character['Gold'] -= character_item['Cost']

    Notification(notification_text, timeout=6).show()

    self.set_as_finished()




