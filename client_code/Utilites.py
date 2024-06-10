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



def get_backup():
  characters = app_tables.characters.search()
  backup = {}
  backup['Characters'] = list()
  for character in characters:
    character_dict = dict(character)
    character_dict['Class'] = dict(character_dict['Class'])
    backup['Characters'].append(character_dict)

  frosthaven = app_tables.frosthaven.search()[0]
  frosthaven_dict = dict(frosthaven)
  backup['Frosthaven'] = frosthaven_dict

  classes = app_tables.classes.search()
  backup['Classes'] = list()
  for character_class in classes:
    character_class_dict = dict(character_class)
    backup['Classes'].append(character_class_dict)

  calendar = app_tables.calendar.search()
  backup['Calendar'] = list()
  for week in calendar:
    week_dict = dict(week)
    backup['Calendar'].append(week_dict)

  now = datetime.now().strftime("%d-%m-%Y %H%M%S")
  backup_filename = f'Frosthaven_backup {now}.json'
  backup_blob = anvil.BlobMedia(content_type='application/json', content=json.dumps(backup).encode('utf-8'), name=backup_filename)
  return backup_blob
