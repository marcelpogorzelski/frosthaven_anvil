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
    current_events = {
      'Summer Outpost': [5,31,58,22,13,20,6,21,53,64,30,32,63,4,28,57,33,18,14,52,1,34,29,26,25,24,17,15,27,61],
      'Summer Road': [14,31,4,33,10,20,24,21,27,26,23,29,9,22,8,30,38,45,25,1,28,6,17,32,16,11,2,46,42,12],
      'Winter Outpost': [34,28,46,47,43,44,21,36,37,38,14,31,40,10,41,18,42,81,30,11,22,32,13,23,33,24,9,20,1,25,5,8,26,80,12,62,27,39,45,35,29,19],
      'Winter Road': [11,10,7,23,38,14,2,30,15,21,22,20,41,78,18,6,5,16,13,8,26,27,28,29,24,44,25,17,42],
      'Boat': [5,15,9,3,7,6,2,10,12,11,1,13],
    }
    for event in app_tables.events.search():
      active = current_events[event['Type']]
      cards = list()
      for card_number in range(1, event['Count']+1):
        if card_number in active:
          continue
        cards.append(card_number)
      event.update(
        Inactive=cards,
        Active=active,
        CurrentEvent=None
      )
        
      
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




      
    
