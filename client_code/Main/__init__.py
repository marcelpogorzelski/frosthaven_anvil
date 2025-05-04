from ._anvil_designer import MainTemplate
from anvil import *
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
from ..Achievements import Achievements

class Main(MainTemplate):
  def __init__(self, player_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.player_links = {}
    self.player_toggle_links = []
    #self.login_form = login_form

    self.setup_player('Håvard', self.havard_link, self.havard_sheet_link, self.havard_items_link, self.havard_cards_link, self.havard_details_link)
    self.setup_player('John Magne', self.john_magne_link, self.john_magne_sheet_link, self.john_magne_items_link, self.john_magne_cards_link, self.john_magne_details_link)
    self.setup_player('Kristian', self.kristian_link, self.kristian_sheet_link, self.kristian_items_link, self.kristian_cards_link, self.kristian_details_link)
    self.setup_player('Marcel', self.marcel_link, self.marcel_sheet_link, self.marcel_items_link, self.marcel_cards_link, self.marcel_details_link)
    
    self.setup_active_scenario()
    if player_name == 'Frosthaven':
      if self.scenario:
        self.open_scenario(self.scenario)
      else:
        self.change_form(Frosthaven(),self.frosthaven_link)
    else:
      link = self.player_links[player_name]['Links'][0]
      self.open_player_link(link.tag['Player'], link)

  def setup_active_scenario(self):
    self.scenario = app_tables.frosthaven.search()[0]['ActiveScenario']
    if not self.scenario:
      self.scenario_link.visible = False
      self.scenario_link.text = ''
      return
    self.scenario_link.visible = True
    self.scenario_link.text = self.scenario['Number']
    

  def setup_player(self, player, player_link, sheet_link, items_link, cards_link, details_link):
    player_link.tag = player
    sheet_link.tag = {'Player': player, 'Next': items_link, 'Form': Character}
    items_link.tag = {'Player': player, 'Next': cards_link, 'Form': CharacterItems}
    cards_link.tag = {'Player': player, 'Next': details_link, 'Form': CharacterCards}
    details_link.tag = {'Player': player, 'Next': sheet_link, 'Form': CharacterDetails}

    invisible_links = [sheet_link, items_link, cards_link, details_link]
    for link in invisible_links:
      self.player_toggle_links.append(link)
    
    self.player_links[player] = {'Player Link': player_link, 'Links': invisible_links, 'Sheet Link': sheet_link, 'Items Link': items_link}
 
  def change_form(self, form, link=None):
    if link:
      self.navbar_link_select(link)
    self.content_panel.clear()
    self.content_panel.add_component(form, full_width_row=True)

  def reset_links(self, **event_args):
    for comp in self.navbar_column_panel.get_components():
      if type(comp) is Spacer:
        continue
      if comp.role == 'selected':
        comp.role = ''
    self.appeear_links_toggle(self.player_toggle_links, False)

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

  def appeear_links_toggle(self, toggle_link_list, toggle):
    for toggle_link in toggle_link_list:
      toggle_link.visible = toggle

  def open_player_link(self, player, link):
    self.navbar_link_select(link)
    self.appeear_links_toggle(self.player_links[player]['Links'], True)
    self.player_links[player]['Player Link'].role = 'selected'
    self.change_form(link.tag['Form'](player))

  def player_link_click(self, **event_args):
    player = event_args['sender'].tag
    for player_link in self.player_links[player]['Links']:
      if player_link.role == 'selected':
        self.open_player_link(player_link.tag['Player'], player_link.tag['Next'])
        return
    link = self.player_links[player]['Links'][0]
    self.open_player_link(link.tag['Player'], link)
    
  def player_sublink_click(self, **event_args):
    link = event_args['sender']
    self.open_player_link(link.tag['Player'], link)

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
    self.open_scenario(self.scenario)

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

