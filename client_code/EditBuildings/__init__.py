from ._anvil_designer import EditBuildingsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EditBuildings(EditBuildingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    all_building_numbers = (5, 12,17,21,24,34,35,37,39,42,44,65,67,72,74,81,83,84,90,98)
    items = 
    for building_number in all_building_numbers:
      building = app_tables.buildings.search(Number=building_number, Available=True)
      level = 0
      if len(building) > 0:
        level = building[0]['Level']
      print(f"Building {building_number} has level {level}")

    

    # Any code you write here will run before the form opens.
