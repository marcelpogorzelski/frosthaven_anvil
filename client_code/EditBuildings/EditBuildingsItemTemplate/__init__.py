from ._anvil_designer import EditBuildingsItemTemplateTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EditBuildingsItemTemplate(EditBuildingsItemTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.building_number_drop_down.items = [(str(i), (str(i), self.item['Name'])) for i in range(self.item['Count'] + 1)]
    self.building_number_drop_down.selected_value = (str(self.item['Level']), self.item['Name'])
    self.name_text_box.text = self.item['Name']

    # Any code you write here will run before the form opens.

  def building_number_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    building_name = event_args['sender'].selected_value[1]
    building_level = event_args['sender'].selected_value[0]
    print(building_name,building_level)
    for building in app_tables.buildings.search(Name=building_name):
      Available = False
      if str(building['Level']) == building_level:
        Available = True
      building.update(Available=Available)
