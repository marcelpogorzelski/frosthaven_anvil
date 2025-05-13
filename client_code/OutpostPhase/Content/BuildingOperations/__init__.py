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

    self.max_amount = 1
    self.resource_repeating_panel.items = [
      {'Image': '_/theme/resource_images/fh-lumber-bw-icon.png', 'MaxAmount': self.max_amount},
      {'Image': '_/theme/resource_images/fh-metal-bw-icon.png', 'MaxAmount': self.max_amount},
      {'Image': '_/theme/resource_images/fh-hide-bw-icon.png', 'MaxAmount': self.max_amount},
    ]
    

    # Any code you write here will run before the form opens.
