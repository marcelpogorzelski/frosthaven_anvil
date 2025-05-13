from ._anvil_designer import BuildingOperationsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class BuildingOperations(BuildingOperationsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    max_amount = 3
    self.total_gold = max_amount * 2 * 3
    self.total_gold_text_box.text = self.total_gold
    self.resource_repeating_panel.items = [
      {'Image': '_/theme/resource_images/fh-lumber-bw-icon.png', 'MaxAmount': max_amount, 'Amount': max_amount},
      {'Image': '_/theme/resource_images/fh-metal-bw-icon.png', 'MaxAmount': max_amount, 'Amount': max_amount},
      {'Image': '_/theme/resource_images/fh-hide-bw-icon.png', 'MaxAmount': max_amount, 'Amount': max_amount},
    ]
    self.resource_repeating_panel.set_event_handler('x-update-value', self.update_total_gold)

  def update_total_gold(self, **event_args):
    self.total_gold = 0
    for resource in self.resource_repeating_panel.items:
      self.total_gold += resource['Amount'] * 2
    self.total_gold_text_box.text = self.total_gold

