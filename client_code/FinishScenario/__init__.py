from ._anvil_designer import FinishScenarioTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
import math
from ..Resources import Resources
from ..Calendar import Calendar

def string_helper(player_resources, resource_list):
  resource_string_list = list()
  for resource in resource_list:
    if player_resources[resource]:
      resource_string_list.append(f"{resource}: {player_resources[resource] or 0}")

  if resource_list:
    return '  - ' + ', '.join(resource_string_list) + '\n'
  return ''

class FinishScenario(FinishScenarioTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = app_tables.frosthaven.search()[0]
    self.finish_scenario_repeating_panel.items = [
      {'Player': 'Håvard'},
      {'Player': 'John Magne'},
      {'Player': 'Kristian'},
      {'Player': 'Marcel'},
      {'Player': 'Frosthaven'},
    ]
    self.set_party_level()
    self.set_coin_value()
    self.set_bonus_experience()
    self.populate_scenario()
        
  def set_party_level(self):
    adjust_level = self.adjust_level_text_box.text or 0
    
    total_levels = 0
    for character in app_tables.characters.search():
      total_levels += character['Level']
    average_level = math.ceil(total_levels / 4 / 2) + adjust_level
    self.party_level_text_box.text = average_level

  def set_coin_value(self):
    gold_conversion = app_tables.scenario_info.get(Level=self.party_level_text_box.text)['Gold Conversion']
    self.coin_value_text_box.text = gold_conversion

  def set_bonus_experience(self):
    bonus_experience = app_tables.scenario_info.get(Level=self.party_level_text_box.text)['Bonus Experience']
    self.bonus_experience_text_box.text = bonus_experience
    
  def adjust_level_plus_button_click(self, **event_args):
    self.adjust_level_text_box.text = self.adjust_level_text_box.text + 1
    self.item['Adjust Level'] = self.adjust_level_text_box.text
    self.set_party_level()
    self.set_coin_value()
    
  def adjust_level_minus_button_click(self, **event_args):
    self.adjust_level_text_box.text = self.adjust_level_text_box.text - 1
    self.item['Adjust Level'] = self.adjust_level_text_box.text
    self.set_party_level()
    self.set_coin_value()
    
  def adjust_level_text_box_change(self, **event_args):
    self.set_party_level()
    self.set_coin_value()

  def get_gold(self, player_resources):
    gold = player_resources['Gold'] or 0
    gold_coin = player_resources['GoldCoins'] or 0
    return (gold_coin * self.coin_value_text_box.text) + gold

  def get_experience(self, player_resources):
    experience = self.bonus_experience + (player_resources['Experience'] or 0)
    return experience

  def get_player_string(self, player_name, player_resources):
    player_string = player_name + ':\n'

    if player_name != 'Frosthaven':
      experience = self.get_experience(player_resources)

      gold = self.get_gold(player_resources)

      other_resources = {'Experience': experience, 'Gold': gold, 'Check Marks': player_resources['CheckMarks']}
    
      player_string += string_helper(other_resources, ['Experience', 'Gold', 'Check Marks'])
      
    player_string += string_helper(player_resources, ['Lumber', 'Metal', 'Hide'])
    player_string += string_helper(player_resources, ['Arrowvine', 'Axenut', 'Corpsecap'])
    player_string += string_helper(player_resources, ['Flamefruit', 'Rockroot', 'Snowthistle'])

    player_string += '\n'
    return player_string    

  def finish_scenario_outlined_button_click(self, **event_args):

    if event_args['sender'].tag == 'Completed':
      self.bonus_experience = self.bonus_experience_text_box.text or 0
    elif event_args['sender'].tag == 'Lost':
      self.bonus_experience = 0

    #{'Player': 'Håvard', 'Experience': None, 'Gold': 1, 'GoldCoins': 3, 'Lumber': None, 'Metal': None, 'Hide': None, 'Arrowvine': None, 'Axenut': None, 'Corpsecap': None, 'Flamefruit': None, 'Rockroot': None, 'Snowthistle': None}
    total_string = 'Changed Values:\n'
    
    for player_input in self.finish_scenario_repeating_panel.get_components():
      player_name = player_input.item['Player']
      player_resources = player_input.item
      
      total_string += self.get_player_string(player_name, player_resources)
      total_string += '\n'

    if not confirm(content=total_string, large=True):
      return

    resource_names = ['Lumber', 'Metal', 'Hide', 'Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle']

    for player_input in self.finish_scenario_repeating_panel.get_components():
      player_name = player_input.item['Player']
      player_resources = player_input.item
      
      if player_name == 'Frosthaven':
        database_entry = app_tables.frosthaven.search()[0]
      else:
        database_entry = app_tables.characters.get(Player=player_name)
        
        experience = self.get_experience(player_resources)
        if experience > 0:
          database_entry['Experience'] += experience
          database_entry['Level'], database_entry['NextLevelExperience'] = Utilites.get_level(database_entry['Experience'])
  
        gold = self.get_gold(player_resources)
        if gold > 0:
          database_entry['Gold'] += gold

        if player_resources['CheckMarks']:
          checkmarks =  database_entry['CheckMarks'] + (player_resources['CheckMarks'] or 0)
          if checkmarks > 18:
            checkmarks = 18
          database_entry['CheckMarks'] = checkmarks
 
      for resource_name in resource_names:
        if not player_resources[resource_name]:
          continue
        database_entry[resource_name] += player_resources[resource_name] or 0
      database_entry.update()

    scenario = self.scenario_drop_down.selected_value
    if scenario:
      scenario.update(
        Chests=self.chests_text_box.text,
        Notes=self.notes_text_box.text,
        Status=self.status_drop_down.selected_value
      )

    main_form = get_open_form()
    main_form.navbar_link_select(main_form.calendar_link)
    main_form.change_form(Calendar())

  def populate_scenario(self):
    item_list = [('None', None)]
    for row in app_tables.scenarios.search(q.not_(Status='Undiscovered')):
      item_list.append((row['Number'], row))
    self.scenario_drop_down.items = item_list
    self.scenario_data_row_panel.item = app_tables.scenarios.search()[0]

  def scenario_drop_down_change(self, **event_args):
    scenario = event_args['sender'].selected_value
    if scenario:
      self.scenario_data_row_panel.item = scenario
      self.status_drop_down.selected_value = scenario['Status']
      self.name_label.text = scenario['Name']
      self.notes_text_box.text = scenario['Notes']
      self.chests_text_box.text = scenario['Chests']
      self.name_label.visible = True
      self.status_drop_down.visible = True
      self.notes_text_box.visible = True
      self.chests_text_box.visible = True
    else:
      self.scenario_data_row_panel.item = app_tables.scenarios.search()[0]
      self.name_label.visible = False
      self.status_drop_down.visible = False
      self.notes_text_box.visible = False
      self.chests_text_box.visible = False
