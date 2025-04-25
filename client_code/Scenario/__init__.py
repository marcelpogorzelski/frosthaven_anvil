from ._anvil_designer import ScenarioTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Scenario(ScenarioTemplate):
  def __init__(self, scenario, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = scenario
    self.frosthaven = next(iter(app_tables.frosthaven.search()))
    if self.item['Errata']:
      self.errata_card.visible = True
    # Any code you write here will run before the form opens.

    if self.item['Location'] == 'FR':
      self.road_card_card.visible = True
      
    self.activate_buttons()
    self.set_complexity_image()
    self.get_images()

  def reset_buttons(self):
    self.start_scenario_button.visible = False
    self.win_scenario_button.visible = False
    self.lose_scenario_button.visible = False
    self.leave_scenario_button.visible = False

  def activate_buttons(self):
    self.reset_buttons()
    if self.frosthaven['ActiveScenario'] != self.item:
      self.start_scenario_button.visible = True
      return
    self.win_scenario_button.visible = True
    self.lose_scenario_button.visible = True
    self.leave_scenario_button.visible = True


  def set_complexity_image(self):
    complexity_images = {
      1: '_/theme/complexity1.png',
      2: '_/theme/complexity2.png',
      3: '_/theme/complexity3.png',
    }
    self.complexity_image.source = complexity_images[self.item['Complexity']]

  def get_images(self):
    if self.item['Number'][0:1] == 'So':
      self.scenario_image.source = None
      return
    name = self.item['Name'].lower().replace('\'', '').replace(' ', '-')
    number = int(self.item['Number'][1:])
    
    scenario_image_media = URLMedia(f"https://github.com/any2cards/frosthaven/blob/master/images/art/frosthaven/stickers/individual/location-stickers/fh-{number:03d}-{name}.png?raw=true")
    map_layout_image_media = URLMedia(f"https://github.com/any2cards/frosthaven/blob/master/images/art/frosthaven/scenario-layout/fh-{number:03d}-{name}-map-layout.png?raw=true")
    loot_image_media = URLMedia(f"https://github.com/any2cards/frosthaven/blob/master/images/art/frosthaven/scenario-layout/fh-{number:03d}-{name}-loot.png?raw=true")
    key_image_media = URLMedia(f"https://github.com/any2cards/frosthaven/blob/master/images/art/frosthaven/scenario-layout/fh-{number:03d}-{name}-scenario-key.png?raw=true")
    
    self.scenario_image.source = scenario_image_media
    self.map_layout_image.source = map_layout_image_media
    self.loot_image.source = loot_image_media
    self.key_image.source = key_image_media

  def start_scenario_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.frosthaven['ActiveScenario'] = self.item
    self.activate_buttons()

  def leave_scenario_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.frosthaven['ActiveScenario'] = None
    self.activate_buttons()

  def notes_show_link_click(self, **event_args):
    if self.notes_text_area.visible:
      self.notes_show_link.icon = 'fa:angle-double-down'
    else:
      self.notes_show_link.icon = 'fa:angle-double-up'
    self.notes_text_area.visible = not self.notes_text_area.visible