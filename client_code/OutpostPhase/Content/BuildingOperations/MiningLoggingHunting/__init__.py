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

    self.characters_repeating_panel.items = [
      {'Player': 'Håvard'},
      {'Player': 'John Magne'},
      {'Player': 'Kristian'},
      {'Player': 'Marcel'},
    ]

  def get_total_gold(self):
    self.total_gold = 0
    for resource in self.resource_repeating_panel.items:
      self.total_gold += resource['Amount'] * 2
    self.total_gold_text_box.text = self.total_gold

  def update_total_gold(self, **event_args):
    self.get_total_gold()

