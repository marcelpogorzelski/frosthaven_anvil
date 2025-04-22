from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import json
from anvil.tables import app_tables
from .. import Utilites

def parse_int_price(price):
  if price:
    return int(price)
  return 0


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def test_treasures(self):
    return
    scenario = app_tables.scenarios.get(Number='S2')
    treasure = app_tables.treasures.get(Number=5)
    print(treasure)
    if treasure not in scenario['Treasures']:
      scenario['Treasures'] += [treasure]
    print(len(scenario['Treasures']))

    # Any code you write here will run before the form opens.
  def export_button_click(self, **event_args):
    backup_blob = Utilites.get_backup()
    download(backup_blob)

  def parse_scenario(self, scenario_data):
    if 'treasures' not in scenario_data:
        return
    scenario_id = 'S' + str(scenario_data['id'])

    scenario = app_tables.scenarios.get(Number=scenario_id)
    
    treasures = list()

    for treasure_id in scenario_data['treasures']:
      treasure = app_tables.treasures.get(Number=treasure_id)
      treasures.append(treasure)
    scenario['Treasures'] = treasures

  def parse_scenario_errata(self, scenario_id, scenario_data):
    if not scenario_id.isdigit():
        return
      
    #number = 'S' + str(scenario_id)
    complition = scenario_data.get('completion', {'section': ''})['section']
    has_random_item = bool(scenario_data['loot']['Item'])
    errata = scenario_data['errata']
    page = int(scenario_data['page'])
    location = scenario_data.get('location', '')
    tiles = scenario_data['tiles']
    complexity = scenario_data.get('difficulty', 1)

    name = scenario_data['title']
    
    scenario = app_tables.scenarios.get(Name=name)

    #scenario.update()
    
    
  def import_file_loader_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    file_data = json.loads(file.get_bytes())

    for scenario_id, scenario_data in file_data.items():
      self.parse_scenario_errata(scenario_id, scenario_data)
      

  def change_password_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.change_password_with_form(require_old_password=False)
    #anvil.users.reset_password('aa_chill_meeting', 'Marcel_Frost')



      
    
