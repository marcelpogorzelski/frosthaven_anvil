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
    Utilites.set_scenario_available()
    
  def test(self):
    return
      
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
    return
    for file in files:
      app_files.achievements.create_file(file.name, file)
    

  def change_password_button_click(self, **event_args):
    return
    anvil.users.change_password_with_form(require_old_password=False)
    #anvil.users.reset_password('aa_chill_meeting', 'Marcel_Frost')

  def action_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def backup_button_click(self, **event_args):
    notification_text = "Databases are all backed up!"
    if not Utilites.backup_tables_to_drive():
      notification_text = "No backup. Reached the daily quota"
    Notification(notification_text, timeout=6).show()




      
    
