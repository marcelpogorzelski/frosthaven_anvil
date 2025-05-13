from ._anvil_designer import BuildingOperationsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .MiningLoggingHunting import MiningLoggingHunting


class BuildingOperations(BuildingOperationsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.building_operations_card.add_component(MiningLoggingHunting())

    
