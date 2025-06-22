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
import re

from .Form1 import Form1
from ..Character.CharacterPerks import CharacterPerks


def extract_slots(text):
  matches = re.findall(r'\{([^}]*)\}', text)
  return matches

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    Utilites.set_scenario_available()

    self.rich_setup()


  def perks(self):
    characters = json.loads(app_tables.files.get(path='characters_frosthaven.json')['file'].get_bytes())

    for char_class in app_tables.classes.search():
      character = characters[char_class['Id']]
      char_class.update(Masteries=character['masteries'], Perks=character['perks'])
    
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
    self.layouts_upload(files)

    
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

  def fix_mastery(self, mastery):
    slots = extract_slots(mastery)
    for slot in slots:
      replace_text = '{' + slot + '}'
      output_text = slot
      if slot == 'again_2.png':
        output_text = 'again.png'
        
      if slot == 'curse_2.png':
        output_text = 'curse.png'
        
      if slot == 'damage_2.png':
        output_text = 'damage.png'
        
      if slot == 'minus_1_2.webp':
        output_text = 'minus_1.webp'
        
      if slot == 'minus_2_2.webp':
        output_text = 'minus_2.webp'

      if slot == 'muddle_2.png':
        output_text = 'muddle.png'

      if slot == 'plus_0_2.webp':
        output_text = 'plus_0.webp'

      if slot == 'plus_1_2.webp':
        output_text = 'plus_1.webp'

      if slot == 'range_2.png':
        output_text = 'range.png'

      if slot == 'resonance_icon_2.png':
        output_text = 'resonance_icon.png'
        
      width = 22
      height = 22
      if slot == 'heal.png':
        width = 17
      if slot == 'range.png':
        width = 30
      if slot == 'transfer_icon.png':
        width = 44
      if slot == 'time_icon.png':
        width = 17
      if slot == 'boneshaper.png':
        width = 20
      if slot == 'item_minus_1.webp':
        width = 26
      if slot == 'retaliate.png':
        width = 20
      if slot == 'shield.png':
        width = 20

      mastery = mastery.replace(replace_text, f'<img src="_/theme/perk_icons/{output_text}" width="{width}" height="{height}">')
    return mastery

    

  def action_button_click(self, **event_args):
    return
    for char_class in app_tables.classes.search():
      #<img src="_/theme/perk_icons/heal.png" width="14" height="20">
      masteries = char_class['MasteriesInfo']
      masteries[0] = self.fix_mastery(masteries[0])
      masteries[1] = self.fix_mastery(masteries[1])
      char_class['MasteriesInfo2'] = masteries

  def rich_setup(self):
    all_slots = set()
    for char_class in app_tables.classes.search():
      for perk_info in char_class['PerksInfo']:
        slots = extract_slots(perk_info['desc'])
        all_slots.update(slots)
    self.rich_drop_down.items = sorted(all_slots)
    self.set_rich_text()

  def set_rich_text(self):
    perk_image = self.rich_drop_down.selected_value
    width = self.width_text_box.text
    height = self.height_text_box.text
    perk_span = f'<img src="_/theme/perk_icons/{perk_image}" width="{width}" height="{height}">'
    self.rich_text_1.content = "abc " + perk_span + " 123 " + perk_image

  def rich_drop_down_change(self, **event_args):
    self.set_rich_text()

  def height_text_box_pressed_enter(self, **event_args):
    self.set_rich_text()
    
  def width_text_box_pressed_enter(self, **event_args):
    self.set_rich_text()


  

  

  def restore_events(self):
    if not confirm("Test?"):
      return
    events_backup = json.loads(Backup.get_backup_file('Events.json').get_bytes())

    for backup_event in events_backup['Rows']:
      current_event = app_tables.events.get(Type=backup_event['Type'])
      current_event.update(
        Count=backup_event['Count'],
        Active=backup_event['Active'],
        Inactive=backup_event['Inactive'],
        CurrentEvent=backup_event['CurrentEvent'],
        PreviousEvents=backup_event['PreviousEvents']
      )
      
      print(f"Restored: {backup_event['Type']}")


  def backup_button_click(self, **event_args):
    if not confirm("Sure?"):
      return
    notification_text = "Databases are all backed up!"
    if not Backup.backup_tables_to_drive():
      notification_text = "No backup. Reached the daily quota"
    Notification(notification_text, timeout=6).show()









      
    
