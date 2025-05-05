from ._anvil_designer import ScenarioTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import navigation


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

    self.check_season()
    self.set_road_card()
    self.activate_buttons()
    self.set_complexity_image()
    self.get_images()
    self.set_treasures()
    self.set_scenario_difficulty_table()
    self.set_requirements()
    
  def check_season(self):
    week = len(app_tables.calendar.search(Finished=True))
    if ((week - 1) // 10 + 1) % 2:
      #summer
      self.season = 'Summer'
      self.season_background = '#FFFFAD'
    else:
      self.season = 'Winter'
      self.season_background = '#ADD8E6'

  def set_road_card(self):
    if self.item['Requirements'] and 'Boat' in self.item['Requirements']:
      event_text = "Draw a Boat Event Card"
      event_backgorund = 'theme:Primary Container'
    elif self.item['Location'] == 'FR':
      event_text = "Don't draw any Event Card!"
      event_backgorund = 'theme:Tertiary Container'
    else:
      event_text = f"Draw a {self.season} Road Event"
      event_backgorund = self.season_background
      
    self.event_card_label.text = event_text
    self.event_card_label.background = event_backgorund

    
  def set_requirements(self):
    if not self.item['Requirements']:
      return
      
    image_source = None
    if 'Climbing Gear' in self.item['Requirements']:
      image_source = '_/theme/outpost/climbing_gear.png'
    if 'Boat' in self.item['Requirements']:
      image_source = '_/theme/outpost/boat.png'
    if 'Sled' in self.item['Requirements']:
      image_source = '_/theme/outpost/sled.png'

    if image_source:
      self.req_image.source = image_source
      self.req_image.visible = True

    
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
    self.key_and_loot_card.visible = True
    self.map_layout_card.visible = True


  def set_complexity_image(self):
    complexity_images = {
      1: '_/theme/scenario/complexity1.png',
      2: '_/theme/scenario/complexity2.png',
      3: '_/theme/scenario/complexity3.png',
    }
    self.complexity_image.source = complexity_images[self.item['Complexity']]

  def get_images(self):
    if self.item['Number'][0:2] == 'So':
      self.scenario_image.source = None
      return
    name = self.item['Name'].lower().replace('\'', '').replace(' ', '-')
    number = int(self.item['Number'][1:])

    scenario_image_file = f"fh-{number:03d}-{name}.png"
    map_layout_image_file = f"fh-{number:03d}-{name}-map-layout.png"
    loot_image_file = f"fh-{number:03d}-{name}-loot.png"
    key_image_file = f"fh-{number:03d}-{name}-scenario-key.png"
    
    self.scenario_image.source = app_files.scenariostickers.get(scenario_image_file)
    self.map_layout_image.source = app_files.scenariolayout.get(map_layout_image_file)
    self.loot_image.source = app_files.scenariolayout.get(loot_image_file)
    self.key_image.source = app_files.scenariolayout.get(key_image_file)

  def set_scenario_difficulty_table(self):
    self.scenario_difficulty_repeating_panel.items = app_tables.scenario_info.search()

  def set_treasures(self):
    self.chests_repeating_panel.items = self.item['Treasures']
    self.chests_repeating_panel.set_event_handler('x-check-looted', self.check_looted)

  def check_looted(self, **event_args):
    if not self.item['Treasures']:
      self.item['Looted'] = True
      return
      
    if all(treasure['Looted'] for treasure in self.item['Treasures']):
      self.item['Looted'] = True
    else:
      self.item['Looted'] = False

  def start_scenario_button_click(self, **event_args):
    self.key_and_loot_card.visible = True
    self.map_layout_card.visible = True
    self.frosthaven['ActiveScenario'] = self.item
    main_form = get_open_form()
    main_form.setup_active_scenario()
    self.activate_buttons()

  def leave_scenario_button_click(self, **event_args):
    self.frosthaven['ActiveScenario'] = None
    main_form = get_open_form()
    main_form.setup_active_scenario()
    navigation.go_to_scenarios()

  def show_link(self, component, link):
    if component.visible:
      link.icon = 'fa:angle-double-down'
    else:
      link.icon = 'fa:angle-double-up'
    component.visible = not component.visible

  def notes_show_link_click(self, **event_args):
    self.show_link(self.notes_text_area, self.notes_show_link)

  def chests_link_click(self, **event_args):
    if not self.item['TreasuresSeen']:
      if not confirm("This is the first time opening Treasures. Are you sure?"):
        return
      self.item['TreasuresSeen'] = True
      self.item.update()
    self.check_looted()
    self.show_link(self.chests_repeating_panel, self.chests_link)

  def scenario_difficulty_link_click(self, **event_args):
    self.show_link(self.scenario_difficulty_data_grid, self.scenario_difficulty_link)

  def decrease_difficulty_link_click(self, **event_args):
    selected_difficulty = app_tables.scenario_info.get(Selected=True)
    if not selected_difficulty['Prev']:
      return
    new_difficulty = selected_difficulty['Prev']
    selected_difficulty['Selected'] = False
    new_difficulty['Selected'] = True

    self.set_scenario_difficulty_table()

  def reset_difficulty_link_click(self, **event_args):
    selected_difficulty = app_tables.scenario_info.get(Selected=True)
    recommended_difficulty = app_tables.scenario_info.get(Recommended=True)
    selected_difficulty['Selected'] = False
    recommended_difficulty['Selected'] = True
    self.set_scenario_difficulty_table()
    
  def increase_difficulty_link_click(self, **event_args):
    selected_difficulty = app_tables.scenario_info.get(Selected=True)
    if not selected_difficulty['Next']:
      return
    new_difficulty = selected_difficulty['Next']
    selected_difficulty['Selected'] = False
    new_difficulty['Selected'] = True

    self.set_scenario_difficulty_table()

  def finish_scenario(self, win):
    if win:
      self.item['Status'] = 'Finished'
    self.frosthaven['ActiveScenario'] = None
    navigation.go_to_finish_scenario(win=win)
    
  def win_scenario_button_click(self, **event_args):
    self.finish_scenario(win=True)

  def lose_scenario_button_click(self, **event_args):
    self.finish_scenario(win=False)
