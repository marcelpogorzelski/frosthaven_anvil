from ._anvil_designer import ScenariosTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Scenarios(ScenariosTemplate):
  def __init__(self, **properties):
    self.available = False
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.scenario_drop_down.items = [(scenario['Number'], scenario) for scenario in app_tables.scenarios.search()]
    self.change_scenario(set_image=True)

  def change_scenario(self, set_image=False):
    self.item = self.scenario_drop_down.selected_value
    self.available = self.item['Status'] != 'Undiscovered'

    if set_image:
      self.set_scenario_image()
    
    self.refresh_data_bindings()

  def set_scenario_image(self):
    if self.item['Number'][0:2] == 'So':
      self.scenario_image.source = None
      return
      
    name = self.item['Name'].lower().replace('\'', '').replace(' ', '-')
    number = int(self.item['Number'][1:])
    
    sticker_media = URLMedia(
      f"https://github.com/any2cards/frosthaven/blob/master/images/art/frosthaven/stickers/individual/location-stickers/fh-{number:03d}-{name}.png?raw=true"
    )
    
    self.scenario_image.source = sticker_media

  def scenario_drop_down_change(self, **event_args):
    self.change_scenario(set_image=True)

  def status_drop_down_change(self, **event_args):
    self.item['Status'] = self.status_drop_down.selected_value
    self.change_scenario()
