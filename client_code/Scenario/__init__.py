from ._anvil_designer import ScenarioTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Loot import Loot


class Scenario(ScenarioTemplate):
  def __init__(self, scenario, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = scenario
    if self.item['Errata']:
      self.errata_card.visible = True
    # Any code you write here will run before the form opens.

    if self.item['Location'] == 'FR':
      self.road_card_card.visible = True
    self.set_complexity_image()
    self.get_scenario_image()


  def set_complexity_image(self):
    complexity_images = {
      1: '_/theme/complexity1.png',
      2: '_/theme/complexity2.png',
      3: '_/theme/complexity3.png',
    }
    self.complexity_image.source = complexity_images[self.item['Complexity']]

  def get_scenario_image(self):
    if self.item['Number'][0:1] == 'So':
      self.scenario_image.source = None
      return
    sticker_name = self.item['Name'].lower().replace(' ', '-')
    sticker_number = int(self.item['Number'][1:])
    sticker_media = URLMedia(f"https://github.com/any2cards/frosthaven/blob/master/images/art/frosthaven/stickers/individual/location-stickers/fh-{sticker_number:03d}-{sticker_name}.png?raw=true")
    self.scenario_image.source = sticker_media

  def loot_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(content=Loot(self.item['Loot']))
