from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import json
from anvil.tables import app_tables
from .. import Utilites

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.test()
    
    
  def test(self):
    unmet_reqs = dict()
    if not app_tables.achievements.get(Name='Into the Forest')['Available']:
      unmet_reqs['Into the Forest'] = 'Unfulfilled Requirements'
    if not app_tables.achievements.get(Name='Shard Seeker')['Available']:
      unmet_reqs['Shard Seeker'] = 'Unfulfilled Requirements'
    unmet_reqs['6Shards']  = 'Unfulfilled Requirements'

    transport = ['Sled', 'Boat', 'Climbing Gear']

    for scenario in app_tables.scenarios.search():
      if scenario['Status'] != 'Available':
        continue
      if not scenario['Requirements']:
        continue
      for requirement in scenario['Requirements']:
        if requirement in transport:
          continue
        if requirement in unmet_reqs:
          print('Test')

  def check_items(self):
    character_items = dict()
    for character in app_tables.characters.search():
      for character_item in character['Items']:
        if character_item['Number'] not in character_items:
          character_items[character_item['Number']] = 1
        else:
          character_items[character_item['Number']] += 1
      
    for item in app_tables.items.search():
      count = character_items.get(item['Number'], 0)
      available_count = item['TotalCount'] - count
      if available_count != item['AvailableCount']:
        print('New: ', item['Number'])

      

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

  def parse_scenario_errata(self, scenarios_data):
    for scenario_id, scenario_data in scenarios_data.items():
      print(scenario_id)
      if not scenario_id.isdigit():
          continue
        
      #number = 'S' + str(scenario_id)
      requirements = scenario_data['requirements']
      name = scenario_data['title']
      
      scenario = app_tables.scenarios.get(Name=name)
      if requirements[0] == "":
        requirements = None
  
      scenario.update(Requirements=requirements)
    
  def import_file_loader_change(self, files, **event_args):
    for file in files:
      app_files.achievements.create_file(file.name, file)
    

  def change_password_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.change_password_with_form(require_old_password=False)
    #anvil.users.reset_password('aa_chill_meeting', 'Marcel_Frost')

  def action_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass




      
    
