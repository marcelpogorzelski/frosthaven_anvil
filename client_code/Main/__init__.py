from ._anvil_designer import MainTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..UnlockEdit import UnlockEdit
from ..Character import Character
from ..Frosthaven import Frosthaven
from ..Resources import Resources
from ..Settings import Settings
from ..Calendar import Calendar
from ..Scenarios import Scenarios
from ..RetiredCharacters import RetiredCharacters
from ..FinishScenario import FinishScenario
from ..Buildings import Buildings
from ..Items import Items
from ..Character.CharacterCards import CharacterCards
from ..Character.CharacterDetails import CharacterDetails
from ..Character.CharacterItems import CharacterItems
from ..Scenarios.Scenario import Scenario
from ..Pets import Pets
from ..OutpostPhase import OutpostPhase
from ..Achievements import Achievements
from .. import Utilites


class Main(MainTemplate):
  def __init__(self, player_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.current_link = None
    self.player_links = {
      'Håvard': self.havard_link,
      'John Magne': self.john_magne_link,
      'Kristian': self.kristian_link,
      'Marcel': self.marcel_link,
    }

    self.setup_active_scenario()
    if player_name == 'Frosthaven':
      self.open_game_flow()
    else:
      self.open_character(player_name)

  def open_game_flow(self):
    gamestate = app_tables.gamestate.search()[0]
    phase = gamestate['Phase']
    if phase == Utilites.OUTPOST_PHASE:
      self.open_outpost()
    elif phase == Utilites.CHOOSE_SCENARIO_PHASE:
      self.open_scenarios()
    elif phase == Utilites.SCENARIO_PHASE:
      if self.scenario:
        self.open_scenario(self.scenario)
      else:
        self.open_scenarios()
    elif phase == Utilites.ENDING_SCENARIO_PHASE:
      self.open_finish_scenario(win=gamestate['LastScenarioWon'])

  def setup_active_scenario(self):
    self.scenario = app_tables.gamestate.search()[0]['ActiveScenario']
    if not self.scenario:
      self.scenario_link.text = 'Choose Scenario'
      return
    self.scenario_link.text = self.scenario['Number']
 
  def change_form(self, form, link=None):
    if link:
      self.navbar_link_select(link)
      self.current_link = link
    self.content_panel.clear()
    self.content_panel.add_component(form, full_width_row=True)

  def reset_links(self, **event_args):
    for comp in self.navbar_column_panel.get_components():
      if type(comp) is Spacer:
        continue
      if comp.role == 'selected':
        comp.role = ''

  def navbar_link_select(self, link):
    self.reset_links()
    link.role = 'selected'

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')

  def frosthaven_link_click(self, **event_args):
    self.change_form(Frosthaven(), event_args['sender'])

  def resources_link_click(self, **event_args):
    self.change_form(Resources(), event_args['sender'])

  def open_character(self, player_name, tab='CharacterSheet'):
    player_link = self.player_links[player_name]
    if self.current_link == player_link:
      self.selected_character.open_next_tab()
    else:
      self.selected_character = Character(player_name, tab)
      self.change_form(self.selected_character, player_link)

  def player_link_click(self, **event_args):
    player_name = event_args['sender'].tag
    self.open_character(player_name)

  def settings_link_click(self, **event_args):
    self.change_form(Settings(), event_args['sender'])

  def open_calendar(self):
    self.change_form(Calendar(), self.calendar_link)

  def calendar_link_click(self, **event_args):
    self.open_calendar()

  def open_scenarios(self):
    self.change_form(Scenarios(), self.scenarios_link)    

  def scenarios_link_click(self, **event_args):
    self.open_scenarios()

  def open_scenario(self, scenario):
    self.change_form(Scenario(scenario), self.scenario_link)    

  def scenario_link_click(self, **event_args):
    self.setup_active_scenario()
    if self.scenario:
      self.open_scenario(self.scenario)
    else:
      self.open_scenarios()

  def retired_characters_link_click(self, **event_args):
    self.change_form(RetiredCharacters(), event_args['sender'])

  def open_finish_scenario(self, win=False):
    self.change_form(FinishScenario(win), self.finish_scenario_link)

  def finish_scenario_link_click(self, **event_args):
    self.open_finish_scenario()

  def unlock_edit_link_click(self, **event_args):
    self.change_form(UnlockEdit(), event_args['sender'])

  def buildings_link_click(self, **event_args):
    self.change_form(Buildings(), event_args['sender'])

  def items_link_click(self, **event_args):
    self.change_form(Items(), event_args['sender'])

  def pets_link_click(self, **event_args):
    self.change_form(Pets(), event_args['sender'])

  def achievements_link_click(self, **event_args):
    self.change_form(Achievements(), event_args['sender'])

  def open_outpost(self):
    self.change_form(OutpostPhase(), self.outpost_link)

  def outpost_link_click(self, **event_args):
    self.open_outpost()

  def go_to_currect_phase(self):
    game_state = app_tables.gamestate.search()[0]['Phase']
               
    if game_state == Utilites.OUTPOST_PHASE:
      self.open_outpost()
    elif game_state == Utilites.SCENARIO_PHASE:
      if self.scenario:
        self.open_scenario(self.scenario)
      else:
        self.open_scenarios()
        
    

