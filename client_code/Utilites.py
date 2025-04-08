import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import URLMedia
import json
from datetime import datetime

def get_level(experience):
  level = 0
  if experience < 45:
    level = 1
  elif experience < 95:
    level = 2
  elif experience < 150:
    level = 3
  elif experience < 210:
    level = 4
  elif experience < 275:
    level = 5
  elif experience < 345:
    level = 6
  elif experience < 420:
    level = 7
  elif experience < 500:
    level = 8
  elif experience >= 500:
    level = 9

  return level

def get_prosperity_level(prosperity):
  prosperity_level = 1
  if prosperity < 6:
    prosperity_level = 1
  elif prosperity < 15:
    prosperity_level = 2
  elif prosperity < 27:
    prosperity_level = 3
  elif prosperity < 42:
    prosperity_level = 4
  elif prosperity < 60:
    prosperity_level = 5
  elif prosperity < 81:
    prosperity_level = 6
  elif prosperity < 105:
    prosperity_level = 7
  elif prosperity < 132:
    prosperity_level = 8
  elif prosperity >= 132:
    prosperity_level = 9

  return prosperity_level


def get_total_defense(moral, defense):
  moral_defense = 0
  if moral < 3:
    moral_defense = -10
  if moral < 5:
    moral_defense = -5
  elif moral < 8:
    moral_defense = 0
  elif moral < 11:
    moral_defense = 5
  elif moral < 14:
    moral_defense = 10
  elif moral >= 14:
    moral_defense = 15
  
  return moral_defense + defense

def database_to_dict(database, linked_columns=None):
  dict_list = list()
  for row in database:
    row_dict = dict(row)
    if linked_columns:
      for column in linked_columns:
        row_dict[column] = dict(row_dict[column])
    dict_list.append(row_dict)
  return dict_list
    

def get_backup():
  backup = {}

  calendar_database = app_tables.calendar.search()
  backup['Calendar'] = database_to_dict(calendar_database)
  
  characters_database = app_tables.characters.search()
  backup['Characters'] = database_to_dict(characters_database, linked_columns=['Class'])

  classes_database = app_tables.classes.search()
  backup['Classes'] =  database_to_dict(classes_database)

  frosthaven_database = app_tables.frosthaven.search()
  backup['Frosthaven'] = database_to_dict(frosthaven_database)

  scenarios_database = app_tables.scenarios.search()
  backup['Scenarios'] = database_to_dict(scenarios_database)

  retired_characters_database = app_tables.retired_characters.search()
  backup['Retired Characters'] = database_to_dict(retired_characters_database, linked_columns=['Class'])

  now = datetime.now().strftime("%d-%m-%Y %H%M%S")
  backup_filename = f'Frosthaven_backup {now}.json'
  backup_blob = anvil.BlobMedia(content_type='application/json', content=json.dumps(backup, indent=4).encode('utf-8'), name=backup_filename)
  return backup_blob
  