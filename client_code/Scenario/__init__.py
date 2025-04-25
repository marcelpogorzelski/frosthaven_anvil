from ._anvil_designer import ScenarioTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import navigation


class Scenario(ScenarioTemplate):
  def __init__(self, scenario=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.frosthaven = app_tables.frosthaven.search()[0]
    
    if scenario:
      self.item = scenario
    else:
      self.item = self.frosthaven['ActiveScenario']
      
    if self.item['Errata']:
      self.errata_card.visible = True
    # Any code you write here will run before the form opens.

    if self.item['Location'] == 'FR':
      self.road_card_card.visible = True
      
    self.activate_buttons()
    self.set_complexity_image()
    self.get_images()
    self.set_chests()
    self.set_scenario_difficulty_table()
    

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

  def set_scenario_difficulty_table(self):
    self.scenario_difficulty_repeating_panel.items = app_tables.scenario_info.search()

  def set_chests(self):
    self.chests_repeating_panel.items = self.item['Treasures']

  def start_scenario_button_click(self, **event_args):
    self.frosthaven['ActiveScenario'] = self.item
    main_form = get_open_form()
    main_form.setup_active_scenario()
    self.activate_buttons()

  def leave_scenario_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.frosthaven['ActiveScenario'] = None
    main_form = get_open_form()
    main_form.setup_active_scenario()
    navigation.go_to_scenarios()
    #self.activate_buttons()

  def show_link(self, component, link):
    if component.visible:
      link.icon = 'fa:angle-double-down'
    else:
      link.icon = 'fa:angle-double-up'
    component.visible = not component.visible

  def notes_show_link_click(self, **event_args):
    self.show_link(self.notes_text_area, self.notes_show_link)

  def chests_link_click(self, **event_args):
    self.show_link(self.chests_repeating_panel, self.chests_link)

  def scenario_difficulty_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.show_link(self.scenario_difficulty_data_grid, self.scenario_difficulty_link)

  def decrease_difficulty_link_click(self, **event_args):
    scenario_difficulty = app_tables.scenario_info.get(Selected=True)
    if scenario_difficulty['Level'] == 0:
      return
    new_difficulty = scenario_difficulty['Level'] - 1
    new_scenario_difficulty = app_tables.scenario_info.get(Level=new_difficulty)
    scenario_difficulty['Selected'] = False
    new_scenario_difficulty['Selected'] = True
    self.set_scenario_difficulty_table()

  def reset_difficulty_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def increase_difficulty_link_click(self, **event_args):
    scenario_difficulty = app_tables.scenario_info.get(Selected=True)
    if scenario_difficulty['Level'] == 7:
      return
    new_difficulty = scenario_difficulty['Level'] + 1
    new_scenario_difficulty = app_tables.scenario_info.get(Level=new_difficulty)
    scenario_difficulty['Selected'] = False
    new_scenario_difficulty['Selected'] = True
    self.set_scenario_difficulty_table()
