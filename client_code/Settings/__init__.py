from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import json
from anvil.tables import app_tables
from .. import Utilites


pets = [
    {
      'id': 1,
      'name': "Piranha Pig",
      'game': "fh",
      'image': "pets/frosthaven/fh-01-piranha-pig.jpeg",
      'imageBack': "pets/frosthaven/fh-01-piranha-pig-back.jpeg",
    },
    {
      'id': 2,
      'name': "Hound",
      'game': "fh",
      'image': "pets/frosthaven/fh-02-hound.jpeg",
      'imageBack': "pets/frosthaven/fh-02-hound-back.jpeg",
    },
    {
      'id': 3,
      'name': "Spitting Drake",
      'game': "fh",
      'image': "pets/frosthaven/fh-03-spitting-drake.jpeg",
      'imageBack': "pets/frosthaven/fh-03-spitting-drake-back.jpeg",
    },
    {
      'id': 4,
      'name': "Rending Drake",
      'game': "fh",
      'image': "pets/frosthaven/fh-04-rending-drake.jpeg",
      'imageBack': "pets/frosthaven/fh-04-rending-drake-back.jpeg",
    },
    {
      'id': 5,
      'name': "Black Imp",
      'game': "fh",
      'image': "pets/frosthaven/fh-05-black-imp.jpeg",
      'imageBack': "pets/frosthaven/fh-05-black-imp-back.jpeg",
    },
    {
      'id': 6,
      'name': "Forest Imp",
      'game': "fh",
      'image': "pets/frosthaven/fh-06-forest-imp.jpeg",
      'imageBack': "pets/frosthaven/fh-06-forest-imp-back.jpeg",
    },
    {
      'id': 7,
      'name': "Snow Imp",
      'game': "fh",
      'image': "pets/frosthaven/fh-07-snow-imp.jpeg",
      'imageBack': "pets/frosthaven/fh-07-snow-imp-back.jpeg",
    },
    {
      'id': 8,
      'name': "Ooze",
      'game': "fh",
      'image': "pets/frosthaven/fh-08-ooze.jpeg",
      'imageBack': "pets/frosthaven/fh-08-ooze-back.jpeg",
    },
    {
      'id': 9,
      'name': "Ruined Machine",
      'game': "fh",
      'image': "pets/frosthaven/fh-09-ruined-machine.jpeg",
      'imageBack': "pets/frosthaven/fh-09-ruined-machine-back.jpeg",
    },
    {
      'id': 10,
      'name': "Lightning Eel",
      'game': "fh",
      'image': "pets/frosthaven/fh-10-lightning-eel.jpeg",
      'imageBack': "pets/frosthaven/fh-10-lightning-eel-back.jpeg",
    },
    {
      'id': 11,
      'name': "Heroics",
      'game': "fh",
      'image': "pets/frosthaven/fh-11-heroics.jpeg",
      'imageBack': "pets/frosthaven/fh-11-heroics-back.jpeg",
    },
    {
      'id': 12,
      'name': "Brummix",
      'game': "fh",
      'image': "pets/frosthaven/fh-12-brummix.jpeg",
      'imageBack': "pets/frosthaven/fh-12-brummix-back.jpeg",
    },
  ]

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
    
    
  def import_file_loader_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    file_data = json.loads(file.get_bytes())

    for scenario_id, scenario_data in file_data.items():
      break
      #self.parse_scenario_errata(scenario_id, scenario_data)

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




      
    
