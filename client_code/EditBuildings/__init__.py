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
    
    buildings = app_tables.buildings.search()
    building_list = {}
    for building in buildings:
      building_number = building['Number']
      building_name = building['Name']
      building_item = building_list.get(building_number, dict({'Number': building_number, 'Name': building_name, 'Level': 0, 'Count': 0}) )
      if building['Available']:
        building_item['Level'] = building['Level']
      building_item['Count'] += 1
      building_list[building_number] = building_item
    self.edit_buildings_repeating_panel.items = building_list.values()

    

    # Any code you write here will run before the form opens.
