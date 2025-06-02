from ._anvil_designer import ScenarioTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator
from ... import navigation
from ... import Utilites
from .Pets import Pets
from .ChooseEventType import ChooseEventType
from ...Event import Event


class Scenario(ScenarioTemplate):
  def __init__(self, scenario=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #self.frosthaven = app_tables.frosthaven.search()[0]
    self.gamestate = app_tables.gamestate.search()[0]
    
    if scenario:
      self.item = scenario
    else:
      self.item = self.gamestate['ActiveScenario']
      
    if self.item['Errata']:
      self.errata_card.visible = True
    # Any code you write here will run before the form opens.

    self.event_backgrounds = {
      'Summer Road': '#FFFFAD',
      'Winter Road': '#ADD8E6',
      'Boat': 'theme:Primary Container'
    }

    self.get_event_type()
    if self.event_type:
      self.draw_event_button.text = f"Draw {self.event_type} Event"
    self.check_road_event()

    if not self.item['Key2']:
      self.key2_image.remove_from_parent()

    self.activate_buttons()
    self.set_complexity_image()
    self.get_images()
    self.set_treasures()
    self.set_scenario_difficulty_table()
    self.set_requirements()

    self.check_pets()

  def check_pets(self):
    if self.gamestate['PetCaught']:
      self.set_pet_caught()
      return

    if not self.item['Pets']:
      return
      
    self.capturable_pets = list()
    for pet in self.item['Pets']:
      if not pet['Captured']:
        self.capturable_pets.append(pet)

    self.setup_pets()

  def setup_pets(self):
    if not self.capturable_pets:
      return
      
    self.pets_button.visible = True
    self.pets_button.enabled = True
    self.pets_form = Pets(self.capturable_pets, self.gamestate, self.pets_button)

  def set_pet_caught(self):
    self.pets_button.visible = True
    self.pets_button.enabled = False
    self.pets_button.text = 'Already caught'
    self.gamestate.update(PetCaught=True)
    
  def get_event_type(self):
    if self.item['Location'] == 'FR':
      self.event_type = None
      self.event_card_flow_panel.visible = False
      self.event_button_flow_panel.visible = False
      self.no_event_label.visible = True
      return
    if self.item['Requirements'] and 'Boat' in self.item['Requirements']:
      self.event_type = 'Boat'
      return
    elif Utilites.is_summer():
      self.event_type = 'Summer Road'
    else:
      self.event_type = 'Winter Road'

  def enable_event_card(self):
    self.event_button_flow_panel.visible = False
    self.draw_event_button.enabled = False
    self.draw_event_button.visible = False
    self.wrong_event_button.enabled = False
    self.wrong_event_button.visible = False
    self.event_card.visible = True
    self.event_card_label.text = self.current_road_event['Label']
    self.event_card.background = self.current_road_event['Background']
    self.event_number_button.text = self.current_road_event['Text']
    if self.current_road_event['Resolved']:
      self.return_event_button.enabled = False
      self.return_event_button.visible = False
      self.remove_event_button.enabled = False
      self.remove_event_button.visible = False

  def check_road_event(self):
    self.current_road_event = self.gamestate['CurrentRoadEvent']
    if self.current_road_event:
      self.enable_event_card()
    
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
    if self.gamestate['ActiveScenario'] != self.item:
      self.start_scenario_button.visible = True
      return
    self.win_scenario_button.visible = True
    self.lose_scenario_button.visible = True
    self.leave_scenario_button.visible = True
    self.key_and_loot_card.visible = True
    self.map_layout_card.visible = True
    self.event_column_panel.visible = True


  def set_complexity_image(self):
    complexity_images = {
      1: '_/theme/scenario/complexity1.png',
      2: '_/theme/scenario/complexity2.png',
      3: '_/theme/scenario/complexity3.png',
    }
    self.complexity_image.source = complexity_images[self.item['Complexity']]

  def get_images(self):
    return
    self.loot_image.source = self.item['Loot']
    self.key_image.source = self.item['Key1']
    self.map_layout_image.source = self.item['Layout']
    
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
    self.gamestate.update(ActiveScenario=self.item, Phase=Utilites.SCENARIO_PHASE)
    navigation.setup_active_scenario()
    self.activate_buttons()

  def leave_scenario_button_click(self, **event_args):
    self.gamestate.update(ActiveScenario=None, Phase=Utilites.CHOOSE_SCENARIO_PHASE)
    navigation.setup_active_scenario()
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

  def reset_gamestate(self, last_scenario_won):
    self.gamestate.update(Phase=Utilites.ENDING_SCENARIO_PHASE, CurrentRoadEvent=None, LastScenarioWon=True, ActiveScenario=None, PetCaught=False)
    
  def win_scenario_button_click(self, **event_args):
    self.reset_gamestate(True)
    self.item['Status'] = Utilites.SCENARIO_FINISHED
    navigation.go_to_finish_scenario(win=True)

  def lose_scenario_button_click(self, **event_args):
    self.reset_gamestate(False)
    navigation.go_to_finish_scenario(win=False)

  def event_number_button_click(self, **event_args):
    event_number = self.event_number_button.text
    forteller_search_value = f"{self.event_card_label.text} Event {event_number:02}"
    navigator.clipboard.writeText(forteller_search_value)
    Notification("Event copied to clipboard. Go to forteller.gg", timeout=6).show()

  def return_event_button_click(self, **event_args):
    if not confirm(f"Do you want to return {self.current_road_event['Label']} Event {self.current_road_event['Text']} to the bottom of the deck?"):
      return
    Utilites.return_current_event(self.current_road_event['Label'])
    self.current_road_event['Resolved'] = True
    self.gamestate['CurrentRoadEvent'] = self.current_road_event
    self.enable_event_card()

  def remove_event_button_click(self, **event_args):
    if not confirm(f"Do you want to remove {self.current_road_event['Label']} Event {self.current_road_event['Text']}?"):
      return
    Utilites.remove_current_event(self.current_road_event['Label'])
    self.current_road_event['Resolved'] = True
    self.gamestate['CurrentRoadEvent'] = self.current_road_event
    self.enable_event_card()

  def get_outpost_event(self, event_type):
    event_number = Utilites.get_next_event(event_type)
    self.current_road_event = dict()
    self.current_road_event['Label'] = event_type
    self.current_road_event['Background'] = self.event_backgrounds[event_type]
    self.current_road_event['Number'] = event_number
    self.current_road_event['Text'] = f"{event_number:02}"
    self.current_road_event['Resolved'] = False
    self.gamestate['CurrentRoadEvent'] = self.current_road_event
    self.enable_event_card()

  def draw_event_button_click(self, **event_args):
    self.get_outpost_event(self.event_type)

  def wrong_event_button_click(self, **event_args):
    event_type = alert(content=ChooseEventType(), title='Choose Event Type', dismissible=False, buttons=[('Cancel', None)])
    if not event_type:
      Notification("Canceled").show()
    self.get_outpost_event(event_type)

  def show_outpost_event_button_click(self, **event_args):
    event_type = self.gamestate['CurrentRoadEvent']['Label']
    event_number = self.gamestate['CurrentRoadEvent']['Text']
    event_side = event_args['sender'].tag
    alert(Event(event_type, event_number, event_side), large=True)

  def pets_button_click(self, **event_args):
    pet = alert(self.pets_form, buttons=[('Cancel', None)], dismissible=True)
    if not pet:
      return
    self.set_pet_caught()