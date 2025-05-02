from ._anvil_designer import SettingsTemplate
from anvil import *
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

    self.check_items()
    
  def test(self):
    pass

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

  def parse_scenario_errata(self, scenario_id, scenario_data):
    if not scenario_id.isdigit():
        return
      
    #number = 'S' + str(scenario_id)
    loot = scenario_data['loot']
    name = scenario_data['title']
    
    scenario = app_tables.scenarios.get(Name=name)

    scenario.update(Loot=loot)

  def parse_achievements(self, achievements):
    exclude = list()

    for achievement in achievements:
      if achievement['id'] in exclude:
        continue
      id = achievement.get('id')
      name = achievement.get('name')
      group = achievement.get('group')
      type = achievement.get('type')
      upgrades = achievement.get('upgrades', [])
      for upgrade in upgrades:
        exclude.append(upgrade)
      upgrades = len(upgrades)
      app_tables.achievements.add_row(Id=id, Name=name, Group=group, Type=type, Upgrades=upgrades)
    
  def import_file_loader_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    file_data = json.loads(file.get_bytes())
    self.parse_achievements(file_data)

  def change_password_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.change_password_with_form(require_old_password=False)
    #anvil.users.reset_password('aa_chill_meeting', 'Marcel_Frost')

  def action_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    for pet in pets:
      image_url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{pet['image']}"
      image_back_url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{pet['imageBack']}"
      app_tables.pets.add_row(
        Number=pet['id'],
        Name=pet['name'],
        ImageURL=image_url,
        ImageBackURL=image_back_url,
        Captured=False)




      
    
