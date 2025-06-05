import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from datetime import datetime

BACKUP_INFO_FILE = "backup_info.txt"


def table_to_dict(table):
  table_dict = dict()
  table_dict['ColumnInfo'] = table.list_columns()
  table_dict['Columns'] = list()

  link_single = list()
  link_multiple = list()
  media = list()

  for column in table.list_columns():
    if column['type'] == 'link_single':
      link_single.append(column['name'])
    if column['type'] == 'link_multiple':
      link_multiple.append(column['name'])
    if column['type'] == 'media':
      media.append(column['name'])

  for row in table.search():
    row_dict = dict(row)

    for column_name in media:
      if not row_dict[column_name]:
        continue
      row_dict[column_name] = None

    for column_name in link_single:
      if not row_dict[column_name]:
        continue
      row_dict[column_name] = row_dict[column_name].get_id()

    for column_name in link_multiple:
      if not row_dict[column_name]:
        continue
      row_dict[column_name] = [ value.get_id() for value in row_dict[column_name]]

    table_dict['Columns'].append(row_dict)

  return table_dict


def backup_table_to_drive(backup_folder, table, table_name):
  table_dict = table_to_dict(table)
  table_backup_filename = f'{table_name}.json'
  backup_blob = anvil.BlobMedia(content_type='application/json', content=json.dumps(table_dict, indent=4).encode('utf-8'), name=table_backup_filename)
  backup_folder.create_file(table_backup_filename, backup_blob)

def new_backup_folder(todays_date):
  new_backup_folder = app_files.backup.create_folder(todays_date)
  
  backup_info = app_files.backup.get(BACKUP_INFO_FILE)
  if backup_info:
    backup_info.trash()
    
  app_files.backup.create_file(BACKUP_INFO_FILE, todays_date)

  return new_backup_folder


def get_backup_folder():
  todays_date = datetime.now().strftime("%d-%m-%Y")

  todays_backup_folder = app_files.backup.get(todays_date)
  if not todays_backup_folder:
    todays_backup_folder = new_backup_folder(todays_date)

  backup_count = len(todays_backup_folder.folders)

  if backup_count >= 5:
    return False

  backup_folder = todays_backup_folder.create_folder(f"Backup {backup_count + 1}")

  return backup_folder


def backup_tables_to_drive():
  backup_folder = get_backup_folder()
  if not backup_folder:
    return False

  backup_table_to_drive(backup_folder, app_tables.achievements, 'Achievements')
  backup_table_to_drive(backup_folder, app_tables.available_buildings, 'AvailableBuildings')
  backup_table_to_drive(backup_folder, app_tables.buildings, 'Buildings')
  backup_table_to_drive(backup_folder, app_tables.calendar, 'Calendar')
  backup_table_to_drive(backup_folder, app_tables.characters, 'Characters')
  backup_table_to_drive(backup_folder, app_tables.classes, 'Classes')
  backup_table_to_drive(backup_folder, app_tables.events, 'Events')
  backup_table_to_drive(backup_folder, app_tables.frosthaven, 'Frosthaven')
  backup_table_to_drive(backup_folder, app_tables.gamestate, 'GameState')
  backup_table_to_drive(backup_folder, app_tables.items, 'Items')
  backup_table_to_drive(backup_folder, app_tables.pets, 'Pets')
  backup_table_to_drive(backup_folder, app_tables.retired_characters, 'RetiredCharacters')
  backup_table_to_drive(backup_folder, app_tables.scenario_info, 'ScenarioInfo')
  backup_table_to_drive(backup_folder, app_tables.scenarios, 'Scenarios')
  backup_table_to_drive(backup_folder, app_tables.treasures, 'Treasures')
  return True


def newest_backup_folder():
  backup_info = app_files.backup.get(BACKUP_INFO_FILE).get_bytes()
  if '05-06-2025' == backup_info:
    print('yea')
  
  
