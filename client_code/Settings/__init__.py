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


    
  def import_file_loader_change(self, file, **event_args):
    scenarios = json.loads(file.get_bytes())

    pets = {pet['Name']: pet for pet in app_tables.pets.search()}
    scenario_rows = {scenario_row['Name']:scenario_row for scenario_row in app_tables.scenarios.search()}

    for scenario_id, scenario in scenarios.items():
      if not scenario_id.isdigit():
        continue
      monsters = scenario.get('monsters', list())
      if not monsters:
        monsters.extend(scenarios[f"{scenario_id}A"]['monsters'])
        monsters.extend(scenarios[f"{scenario_id}B"]['monsters'])
    
      monsters_names = [ monster['name'] for monster in monsters]
      pets_in_scenario = list()
      for pet_name, pet in pets.items():
        if pet_name not in monsters_names:
          continue
        pets_in_scenario.append(pet)
      if not pets_in_scenario:
        continue
        
      scenario_rows[scenario['title']].update(Pets=pets_in_scenario)

    

  def change_password_button_click(self, **event_args):
    return
    anvil.users.change_password_with_form(require_old_password=False)
    #anvil.users.reset_password('aa_chill_meeting', 'Marcel_Frost')

  def action_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def backup_button_click(self, **event_args):
    if not confirm("Sure?"):
      return
    notification_text = "Databases are all backed up!"
    if not Utilites.backup_tables_to_drive():
      notification_text = "No backup. Reached the daily quota"
    Notification(notification_text, timeout=6).show()




      
    
