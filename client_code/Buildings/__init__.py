from ._anvil_designer import BuildingsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Buildings(BuildingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    for available_building in app_tables.available_buildings.search(Available=True):
      building = app_tables.buildings.get(Name=available_building['Name'], Level=available_building['CurrentLevel'])
      tag = (building['Card Front'], building['Card Back'])
      building_image = Image(source=building['Card Front'], display_mode='original_size', tag=tag)
      building_image.add_event_handler('mouse_down', self.change_building_side)
      self.buildings_flow_panel.add_component(building_image)
    #Image(source=self.buildings_list[0]["Card Front"])

  def change_building_side(self, **event_args):
    if event_args['button'] != 1:
      return
    building_image = event_args['sender']
    building_image.tag = tuple(reversed(building_image.tag))
    building_image.source = building_image.tag[0]

