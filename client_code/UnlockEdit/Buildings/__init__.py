from ._anvil_designer import BuildingsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Buildings(BuildingsTemplate):
  def __init__(self, **properties):
    
    self.init_components(**properties)

    drop_down_items = list()
    for building in app_tables.available_buildings.search():
      if building['Available']:
        drop_down_text = f"{building['Number']} - {building['Name']}"
      else:
        drop_down_text = str(building['Number'])
      drop_down_items.append((drop_down_text, building))
    self.building_drop_down.items = drop_down_items
    self.change_building()

  def change_building(self):
    self.item = self.building_drop_down.selected_value
    self.level_drop_down.items = [
      (str(level), level) for level in range(self.item['MinLevel'] , self.item['MaxLevel'] + 1)
    ]
    self.refresh_data_bindings()

  def available_check_box_change(self, **event_args):
    self.item['Available'] = self.available_check_box.checked
    self.refresh_data_bindings()

  def building_drop_down_change(self, **event_args):
    self.change_building()

  def level_drop_down_change(self, **event_args):
    level = self.level_drop_down.selected_value
    self.item['CurrentBuilding'] = app_tables.buildings.get(Level=level, Number=self.item['Number'])
    self.refresh_data_bindings()
