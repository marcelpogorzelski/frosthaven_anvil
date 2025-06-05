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
from ..Utilites import Backup
from .. import Frosthaven_info

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    Utilites.set_scenario_available()


    #self.test()

  def test(self):
    return

    
  def get_image(self, path):
    url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{path}"
    return URLMedia(url)

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

  def import_multi_file_loader_change(self, files, **event_args):
    self.layouts_upload(files, )

    
  def import_file_loader_change(self, file, **event_args):
    pass

  def layouts_upload(self, files):
    layouts_data = dict()
    for layout_file in files:
      _ , number, *rest = layout_file.name.split('-')

      s_number = 'S' + str(int(number))
  
      if s_number not in layouts_data:
        layouts_data[s_number] = {
          'loot': None,
          'layout': None,
          'key1': None,
          'key2': None
        }
  
      layout_data = layouts_data[s_number]
  
      if rest[-1] == 'loot.png':
        layout_data['loot'] = layout_file
      elif rest[-1] == 'layout.png':
        layout_data['layout'] = layout_file
      elif rest[-1] == 'b.png':
        layout_data['key2'] = layout_file
      else:
        layout_data['key1'] = layout_file

    for scenartio in app_tables.scenarios.search():
      layout_data = layouts_data[scenartio['Number']]
      
      scenartio.update(
        Loot=layout_data['loot'],
        Layout=layout_data['layout'],
        Key1=layout_data['key1'],
        Key2=layout_data['key2']
      )

  def events(self, files, event_type):
    event_prefix = 'fh-' + ''.join([word[0] for word in event_type.lower().split()]) + 'e-'
    event_folder = app_files.events.create_folder(event_type)
    for event_file in files:
      event_filename = event_file.name
      event_filename = event_filename.replace(event_prefix, '')
      event_filename = event_filename.replace('f.png', event_type + '-Front.png')
      event_filename = event_filename.replace('b.png', event_type + '-Back.png')
      print(f"Uploading: {event_filename}")
      event_folder.create_file(event_filename, event_file)

  def scenario_errata(self, file):
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
    if not confirm("Test?"):
      return
    events_backup = json.loads(Backup.get_backup_file('Events.json').get_bytes())

    for event in events_backup['Rows']:
      
      print(type(event['PreviousEvents']))
    

  def backup_button_click(self, **event_args):
    if not confirm("Sure?"):
      return
    notification_text = "Databases are all backed up!"
    if not Backup.backup_tables_to_drive():
      notification_text = "No backup. Reached the daily quota"
    Notification(notification_text, timeout=6).show()





      
    
