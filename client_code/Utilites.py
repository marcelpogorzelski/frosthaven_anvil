import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import URLMedia
import json
from datetime import datetime
import math
from anvil.js.window import window

MATERIAL_AND_GOLD_RESOURCES = ['Gold', 'Lumber', 'Metal', 'Hide']
MATERIAL_RESOURCES = ['Lumber', 'Metal', 'Hide']
HERB_RESOURCES = ['Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle']
MATERIAL_AND_HERB_RESOURCES = ['Lumber', 'Metal', 'Hide', 'Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle']
ALL_RESOURCES = ['Gold', 'Lumber', 'Metal', 'Hide', 'Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle']

SCENARIO_FINISHED = 'Finished'
SCENARIO_AVAILABLE = 'Available'
SCENARIO_LOCKED = 'Locked'
SCENARIO_UNDISCOVERED = 'Undiscovered'
SCENARIO_UNFULFILLED = 'Unfulfilled Requirements'
SCENARIO_AVAILABLE_STATUSES = [SCENARIO_AVAILABLE, SCENARIO_FINISHED, SCENARIO_LOCKED, SCENARIO_UNDISCOVERED]
SCENARIO_UNFULFILLED_STATUSES = [SCENARIO_UNFULFILLED, SCENARIO_FINISHED, SCENARIO_LOCKED, SCENARIO_UNDISCOVERED]
SCENARIO_ACTIVE_STATUSES = [SCENARIO_AVAILABLE, SCENARIO_UNFULFILLED]
SCENARIO_NOT_AVAILABLE = [SCENARIO_LOCKED, SCENARIO_UNFULFILLED, SCENARIO_UNDISCOVERED]

TRANSPORTS = ['Sled', 'Boat', 'Climbing Gear']

OUTPOST_PHASE = 'Outpost Phase'
SCENARIO_PHASE = 'Scenario Phase'
ENDING_SCENARIO = 'Ending a Scenario'

PASSAGE_OF_TIME_PHASE = 'PassageOfTimeFinished'
OUTPOST_EVENT_PHASE = 'OutpostEventFinished'
BUILDING_PHASE = 'BuildingOperationsFinished'
BUILDING_MLH_PHASE = 'BuildingOperationMLHFinished'
BUILDING_GARDEN_PHASE = 'BuildingOperationGardenFinished'
BUILDING_BARRACKS_PHASE = 'BuildingOperationBarracksFinished'
DOWNTIME_PHASE = 'DowntimeFinished'
CONSTRUCTION_PHASE = 'ConstructionFinished'

OUTPOST_PHASES = [PASSAGE_OF_TIME_PHASE, OUTPOST_EVENT_PHASE, BUILDING_MLH_PHASE, BUILDING_GARDEN_PHASE, BUILDING_BARRACKS_PHASE]
PHASES = [PASSAGE_OF_TIME_PHASE, OUTPOST_EVENT_PHASE, BUILDING_MLH_PHASE, BUILDING_GARDEN_PHASE, BUILDING_BARRACKS_PHASE]


def check_scenario_available(requirement):
  achievement = app_tables.achievements.get(Name=requirement)
  if achievement:
    if achievement[SCENARIO_AVAILABLE]:
      return True
    else:
      return False
  if app_tables.achievements.get(Name='Coral Crown Shard')['CurrentLevel'] == 6:
    return True
  return False

def set_scenario_available():
  for scenario in app_tables.scenarios.search(Requirements=q.not_(None)):
    if scenario['Status'] not in SCENARIO_ACTIVE_STATUSES:
      continue
    for requirement in scenario['Requirements']:
      if requirement in TRANSPORTS:
        continue
      if check_scenario_available(requirement):
        scenario['Status'] = SCENARIO_AVAILABLE
      else:
        scenario['Status'] = SCENARIO_UNFULFILLED

def get_scenario_statuses(scenario):
  if not scenario['Requirements']:
    return SCENARIO_AVAILABLE_STATUSES
  for requirement in scenario['Requirements']:
    if requirement in TRANSPORTS:
      continue
    if check_scenario_available(requirement):
      return SCENARIO_AVAILABLE_STATUSES 
    else:
      return SCENARIO_UNFULFILLED_STATUSES
  return SCENARIO_AVAILABLE_STATUSES

def set_experience(character, experience):
  experience = max(min(experience, 500),0)
  level, next_level_exp = get_level(experience)

  level_diff = level - character['Level']
  perks = character['Perks'] + level_diff
  
  character.update(Experience=experience, Level=level, NextLevelExperience=next_level_exp, Perks=perks)
    
def add_experience(character, experience):
  if experience < 1:
    return
  set_experience(character, character['Experience'] + experience)

def set_masteries(character, mastery1, mastery2):
  mastery_count = int(mastery1) + int(mastery2)
  checkmarks = character['CheckMarks']
  retired_count = character['RetiredCount']
  level = character['Level'] - 1
  
  perks = retired_count + mastery_count + int(checkmarks/3) + level

  character.update(Perks=perks, Mastery1=mastery1, Mastery2=mastery2, MasteryCount=mastery_count)
  

  
def set_checkmarks(character, checkmarks):
  checkmarks = max(min(checkmarks, 18),0)

  retired_count = character['RetiredCount']
  mastery_count = character['MasteryCount']
  level = character['Level'] - 1

  perks = retired_count + mastery_count + int(checkmarks/3) + level
  
  character.update(CheckMarks=checkmarks, Perks=perks)

def add_checkmarks(character, checkmarks):
  if checkmarks < 1:
    return
  
  current_checkmarks = character['CheckMarks']
  if current_checkmarks == 18:
    return

  set_checkmarks(character, checkmarks + current_checkmarks)

def update_recommended_party_level():
  total_levels = sum(character["Level"] for character in app_tables.characters.search())

  recommended_level = math.ceil(total_levels / 4 / 2)
  
  new_recommended_scenario_difficulty = app_tables.scenario_info.get(Level=recommended_level)
  if new_recommended_scenario_difficulty['Recommended']:
    return False
    
  current_recommended_scenario_difficulty = app_tables.scenario_info.get(Recommended=True)
  
  current_recommended_scenario_difficulty['Recommended'] = False
  new_recommended_scenario_difficulty['Recommended'] = True

  return new_recommended_scenario_difficulty
  
def get_level(experience):
  experience_per_level = [0, 45, 95,150,210,275,345,420,500]
  for level, next_level_experience in zip(range(9), experience_per_level):
    if experience < next_level_experience:
      return level, next_level_experience

  return 9, 501

def get_experience(level):
  if level > 9:
    level = 9
  experience_per_level = [0, 45, 95,150,210,275,345,420,500]
  return experience_per_level[level-1]

def get_prosperity_level(prosperity):
  prosperity_per_level = [0, 6, 15, 27, 42, 60, 81, 105, 132]

  for level, required_prosperity in zip(range(9), prosperity_per_level):
    if prosperity < required_prosperity:
      return level, required_prosperity
  return 9, 133

def set_prosperity(frosthaven, prosperity):
  prosperity = max(min(prosperity, 132),0)
  level, next_level = get_prosperity_level(prosperity)
  frosthaven.update(Prosperity=prosperity, ProsperityLevel=level, ProsperityNextLevel=next_level)

def get_moral_defense(moral):
  moral_defense_break_points = [3, 5, 8, 11, 14]
  for moral_defense, required_moral in zip(range(-10, 15, 5), moral_defense_break_points):
    if moral < required_moral:
      return moral_defense
  return 15

def update_total_defense(frosthaven):
  frosthaven['TotalDefense'] = get_moral_defense(frosthaven['Moral']) + frosthaven['Defense']

def set_moral(frosthaven, moral):
  moral = max(min(moral, 20),0)
  
  frosthaven['Moral'] = moral
  update_total_defense(frosthaven)

def set_walls(frosthaven, walls):
  walls = max(min(walls, 5),0)
  
  frosthaven['Defense'] = walls * 5
  frosthaven['Walls'] = walls
  update_total_defense(frosthaven)

def database_to_dict(database, linked_columns=None):
  dict_list = list()
  for row in database:
    row_dict = dict(row)
    if linked_columns:
      for column in linked_columns:
        row_dict[column] = dict(row_dict[column])
    dict_list.append(row_dict)
  return dict_list

def bounded_text_box(text_box, min_value, max_value):
  if not text_box.text:
    return
    
  if text_box.text > max_value:
    text_box.text = max_value
    
  if text_box.text < min_value:
    text_box.text = min_value

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

def add_to_retired(character):
  player_name = character['Player']
  name = character['Name']
  experience = character['Experience']
  level = character['Level']
  character_class = character['Class']

  perks = character['Perks']
  master1 = character['Mastery1']
  master2 = character['Mastery2']

  app_tables.retired_characters.add_row(
    Player=player_name,
    Name=name,
    Experience=experience,
    Level=level,
    Class=character_class,
    Perks=perks,
    Mastery1=master1,
    Mastery2=master2,
  )

def transfer_all_to_frosthaven(character):
  frosthaven = app_tables.frosthaven.search()[0]
  for resource in MATERIAL_RESOURCES + HERB_RESOURCES:
    frosthaven[resource] += character[resource]

  prosperity = frosthaven['Prosperity'] + 2
  set_prosperity(frosthaven, prosperity)

def reset_character(character):
  prosperity_level = app_tables.frosthaven.search()[0]["ProsperityLevel"]

  starting_gold = (10 * prosperity_level) + 20
  starintg_level = math.ceil(prosperity_level / 2)

  starting_experience = get_experience(starintg_level)
  next_level_experience = get_experience(starintg_level + 1)

  retired_count = character['RetiredCount'] + 1
  starting_perks = starintg_level - 1 + retired_count
  
  character.update(
    Name='',
    Experience=starting_experience,
    NextLevelExperience=next_level_experience,
    Level=starintg_level,
    Gold=starting_gold,
    Lumber=0,
    Metal=0,
    Hide=0,
    Arrowvine=0,
    Axenut=0,
    Corpsecap=0,
    Flamefruit=0,
    Rockroot=0,
    Snowthistle=0,
    CheckMarks=0,
    MasteryCount=0,
    Perks=starting_perks,
    Mastery1=False,
    Mastery2=False,
    RetiredCount=retired_count,
    Notes='',
  )

def retire_character(character):
  add_to_retired(character)
  transfer_all_to_frosthaven(character)
  reset_character(character)

def remove_item(character, removed_item):
  if removed_item not in character['Items']:
    return
  
  character['Items'] = [character_item for character_item in character['Items'] if character_item != removed_item]
  removed_item['AvailableCount'] += 1

def add_item(character, added_item):
  if added_item in character['Items']:
    return
    
  character_items = [character_item for character_item in character['Items']]
  character_items.append(added_item)
  character_items.sort(key=lambda item: item['Number'])
  character['Items'] = character_items
  added_item['AvailableCount'] -= 1

def windowWidthWithMax(maxWidth=900):
  if window.innerWidth < maxWidth:
    maxWidth = window.innerWidth
  remainingWidth = window.innerWidth - maxWidth
  return maxWidth, remainingWidth

def is_summer():
  week = len(app_tables.calendar.search(Finished=True))
  if ((week - 1) // 10 + 1) % 2:
    return True
  return False

def is_winter():
  week = len(app_tables.calendar.search(Finished=True))
  if ((week - 1) // 10 + 1) % 2:
    return False
  return True

def next_phase():
  state = app_tables.gamestate.search()[0]
  #state['Phase']
  index = PHASES.index(state['Phase'])
  index += 1
  if index == len(PHASES):
    index = 0
    
  state['Phase'] = PHASES[index]

def outpost_phase_finished(phase):
  current_phase = app_tables.gamestate.search()[0]['Phase']

  phase_index = OUTPOST_PHASES.index(phase)
  current_phase_index = OUTPOST_PHASES.index(current_phase)
  if current_phase_index > phase_index:
    return True
  return False

def get_next_event(event_type):
  event_entry = app_tables.events.get(Type=event_type)

  if event_entry['CurrentEvent']:
    return event_entry['CurrentEvent']
  
  active_list = event_entry['Active']
  current_event = active_list.pop(0)
  event_entry.update(Active=active_list, CurrentEvent=current_event)
  return current_event

def return_current_event(event_type):
  event_entry = app_tables.events.get(Type=event_type)
  
  current_event = event_entry['CurrentEvent']
  if not current_event:
    return

  active_list = event_entry['Active']
  active_list.append(current_event)

  previous_events = event_entry['PreviousEvents'] or list()
  previous_events.insert(0, current_event)
  
  event_entry.update(
    Active=active_list,
    CurrentEvent=None,
    PreviousEvents=previous_events
  )
  
def remove_current_event(event_type):
  event_entry = app_tables.events.get(Type=event_type)
  
  current_event = event_entry['CurrentEvent']
  if not event_entry['CurrentEvent']:
    return
    
  inactive_list = event_entry['Inactive']
  inactive_list.append(current_event)
  inactive_list.sort()

  previous_events = event_entry['PreviousEvents'] or list()
  previous_events.insert(0, current_event)

  event_entry.update(
    Inactive=inactive_list,
    CurrentEvent=None,
    PreviousEvents=previous_events
  )
  
  
  
  
  