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

  if resource_string_list:
    return "  - " + ", ".join(resource_string_list) + "\n"
  return ""


class FinishScenario(FinishScenarioTemplate):
  def __init__(self, win=False, **properties):
    self.scenario_difficulty = app_tables.scenario_info.get(Selected=True)
    self.bonus_experience = 0
    #self.set_bonus_exp()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = app_tables.frosthaven.search()[0]

    if app_tables.available_buildings.get(Number=90)['CurrentLevel'] == 3:
      self.challenge_2_radio_button.visible = True
    
    
    self.finish_scenario_repeating_panel.items = [
      {"Player": "Håvard"},
      {"Player": "John Magne"},
      {"Player": "Kristian"},
      {"Player": "Marcel"},
      {"Player": "Frosthaven"},
    ]
    
    if win:
      self.win_radio_button.selected = True

    self.set_bonus_exp()

  def set_bonus_exp(self):
    bonus_experience = 0
    if self.win_radio_button.selected:
      bonus_experience = self.scenario_difficulty['Bonus Experience']
    challenges_experience = int(self.challenge_0_radio_button.get_group_value() or 0) * 2

    self.bonus_experience = bonus_experience + (self.other_experience_text_box.text or 0) + challenges_experience
    self.refresh_data_bindings()

  def set_party_level_old(self):
    adjust_level = self.adjust_level_text_box.text or 0

    total_levels = 0
    for character in app_tables.characters.search():
      total_levels += character["Level"]
    average_level = math.ceil(total_levels / 4 / 2) + adjust_level
    self.party_level_text_box.text = average_level

  def set_scenario_difficulty(self, new_difficulty):
    self.scenario_difficulty['Selected'] = False
    new_difficulty['Selected'] = True
    self.scenario_difficulty = new_difficulty
    self.refresh_data_bindings()
    self.set_bonus_exp()

  def adjust_level_plus_button_click(self, **event_args):
    if not self.scenario_difficulty['Next']:
      return
    new_difficulty = self.scenario_difficulty['Next']
    self.set_scenario_difficulty(new_difficulty)
    
  def adjust_level_minus_button_click(self, **event_args):
    if not self.scenario_difficulty['Prev']:
      return
    new_difficulty = self.scenario_difficulty['Prev']
    self.set_scenario_difficulty(new_difficulty)

  def recommended_party_level_button_click(self, **event_args):
    new_difficulty = app_tables.scenario_info.get(Recommended=True)
    self.set_scenario_difficulty(new_difficulty)

  def get_gold(self, player_resources):
    gold = player_resources["Gold"] or 0
    gold_coin = player_resources["GoldCoins"] or 0
    return (gold_coin * self.scenario_difficulty['Gold Conversion']) + gold

  def get_experience(self, player_resources):
    experience = self.bonus_experience + (player_resources["Experience"] or 0)
    return experience

  def check_if_level_up(self, player, experience):
    if experience == 0:
      return False
      
    current_level = player['Level']
    current_exp = player['Experience']
    new_exp = current_exp + experience

    new_level, _ = Utilites.get_level(new_exp)
    if new_level > current_level:
      return new_level
    return False

  def check_if_perk_form_checks(self, player, checks):
    if checks == 0:
      return False

    current_perks = int(player['CheckMarks']/3)
    new_perks = int((player['CheckMarks']+ checks)/3)

    if new_perks > current_perks:
      return True
    return False
  

  def get_player_string(self, player_name, player_resources):
    player_string = player_name + ":\n"

    new_level = None
    new_perk = None
    if player_name != "Frosthaven":
      player = app_tables.characters.get(Player=player_name)

      experience = self.get_experience(player_resources)

      new_level = self.check_if_level_up(player, experience)
      new_perk = self.check_if_perk_form_checks(player, player_resources["CheckMarks"] or 0)

      gold = self.get_gold(player_resources)

      other_resources = {
        "Experience": experience,
        "Gold": gold,
        "Check Marks": player_resources["CheckMarks"],
      }

      player_string += string_helper(
        other_resources, ["Experience", "Gold", "Check Marks"]
      )

    player_string += string_helper(player_resources, ["Lumber", "Metal", "Hide"])
    player_string += string_helper(
      player_resources, ["Arrowvine", "Axenut", "Corpsecap"]
    )
    player_string += string_helper(
      player_resources, ["Flamefruit", "Rockroot", "Snowthistle"]
    )

    if new_level:
      player_string += f"  - Leveled up to level {new_level}!"
    if new_perk:
      player_string += "  - New Perk from check marks!"

    player_string += "\n"
    return player_string

  def finish_scenario_button_click(self, **event_args):
    # {'Player': 'Håvard', 'Experience': None, 'Gold': 1, 'GoldCoins': 3, 'Lumber': None, 'Metal': None, 'Hide': None, 'Arrowvine': None, 'Axenut': None, 'Corpsecap': None, 'Flamefruit': None, 'Rockroot': None, 'Snowthistle': None}
    total_string = "Changed Values:\n"

    for player_input in self.finish_scenario_repeating_panel.get_components():
      player_name = player_input.item["Player"]
      player_resources = player_input.item

      total_string += self.get_player_string(player_name, player_resources)
      total_string += "\n"

    if not confirm(content=total_string, large=True):
      return
    
    resource_names = [
      "Lumber",
      "Metal",
      "Hide",
      "Arrowvine",
      "Axenut",
      "Corpsecap",
      "Flamefruit",
      "Rockroot",
      "Snowthistle",
    ]

    for player_input in self.finish_scenario_repeating_panel.get_components():
      player_name = player_input.item["Player"]
      player_resources = player_input.item

      if player_name == "Frosthaven":
        database_entry = app_tables.frosthaven.search()[0]
      else:
        database_entry = app_tables.characters.get(Player=player_name)

        experience = self.get_experience(player_resources)
        if experience > 0:
          database_entry["Experience"] += experience
          database_entry["Level"], database_entry["NextLevelExperience"] = (
            Utilites.get_level(database_entry["Experience"])
          )

        gold = self.get_gold(player_resources)
        if gold > 0:
          database_entry["Gold"] += gold

        if player_resources["CheckMarks"]:
          checkmarks = database_entry["CheckMarks"] + (
            player_resources["CheckMarks"] or 0
          )
          if checkmarks > 18:
            checkmarks = 18
          database_entry["CheckMarks"] = checkmarks

      for resource_name in resource_names:
        if not player_resources[resource_name]:
          continue
        database_entry[resource_name] += player_resources[resource_name] or 0
      database_entry.update()

    main_form = get_open_form()
    main_form.navbar_link_select(main_form.calendar_link)
    main_form.change_form(Calendar())


  def gold_conversion_background(self):
    if self.scenario_difficulty['NextGold']:
      return 'theme:Primary Container'
    return None

  def other_experience_text_box_change(self, **event_args):
    self.set_bonus_exp()

  def outcome_radio_button_change(self, **event_args):
    self.set_bonus_exp()

  def challenge_radio_button_change(self, **event_args):
    self.set_bonus_exp()
      

