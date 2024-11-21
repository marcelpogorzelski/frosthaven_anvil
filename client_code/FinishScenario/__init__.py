from ._anvil_designer import FinishScenarioTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
import math
from ..Resources import Resources
from ..Calendar import Calendar

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
    self.populate_scenario()
    for input_row in self.finish_scenario_repeating_panel.get_components():
      player = input_row.item['Player']
      if player == 'Frosthaven':
        input_row.gold_text_box.visible = False
        input_row.experience_text_box.visible = False
        input_row.gold_coin_text_box.visible = False
        
        
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
    
  def finish_scenario_outlined_button_click(self, **event_args):
    if not confirm("Do you want to update all values?"):
      return
    if event_args['sender'].tag == 'Completed':
      bonus_experience = self.bonus_experience_text_box.text or 0
    elif event_args['sender'].tag == 'Lost':
      bonus_experience = 0
      
    for input_row in self.finish_scenario_repeating_panel.get_components():
      player = input_row.item['Player']
      if player == 'Frosthaven':
        database_entry = app_tables.frosthaven.search()[0]
      else:
        database_entry = app_tables.characters.get(Player=player)
        database_entry['Experience'] += bonus_experience + (input_row.experience_text_box.text or 0)
        database_entry['Level'] = Utilites.get_level(database_entry['Experience'])

        gold = input_row.gold_text_box.text or 0
        gold_coin = input_row.gold_coin_text_box.text or 0
        total_gold = (gold_coin * self.coin_value_text_box.text) + gold
        database_entry['Gold'] += total_gold
      database_entry['Lumber'] += input_row.lumber_text_box.text or 0
      database_entry['Metal'] += input_row.metal_text_box.text or 0
      database_entry['Hide'] += input_row.hide_text_box.text or 0
      database_entry['Arrowvine'] += input_row.arrowvine_text_box.text or 0
      database_entry['Axenut'] += input_row.axenut_text_box.text or 0
      database_entry['Corpsecap'] += input_row.corpsecap_text_box.text or 0
      database_entry['Flamefruit'] += input_row.flamefruit_text_box.text or 0
      database_entry['Rockroot'] += input_row.rockroot_text_box.text or 0
      database_entry['Snowthistle'] += input_row.snowthistle_text_box.text or 0

    scenario = self.scenario_drop_down.selected_value
    if scenario:
      scenario.update(
        Chests=self.chests_text_box.text,
        Notes=self.notes_text_box.text,
        Status=self.status_drop_down.selected_value
      )

    main_form = self.parent.parent
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
