from ._anvil_designer import FinishScenarioTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
from .. import navigation


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
    self.recommended_scenario_difficulty = app_tables.scenario_info.get(Recommended=True)
    self.bonus_experience = 0
    #self.set_bonus_exp()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.item = app_tables.frosthaven.search()[0]

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
    challenges_experience = self.get_challenge_value() * 2

    self.bonus_experience = bonus_experience + (self.other_experience_text_box.text or 0) + challenges_experience
    self.refresh_data_bindings()

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
    #new_difficulty = app_tables.scenario_info.get(Recommended=True)
    self.set_scenario_difficulty(self.recommended_scenario_difficulty)

  def get_challenge_value(self):
    return int(self.challenge_0_radio_button.get_group_value() or 0)

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
      
    current_exp = player['Experience']
    
    next_level_exp = player['NextLevelExperience']
    new_exp = min(current_exp + experience, 500)

    if new_exp >=  next_level_exp:
       return player['Level'] + 1

    return False

  def check_if_perk_form_checks(self, player, checks):
    if checks == 0:
      return False

    current_perks = int(player['CheckMarks']/3)
    if current_perks == 6:
      return False
      
    new_perks = int((player['CheckMarks']+ checks)/3)

    if new_perks > current_perks:
      return True
    return False

  def check_if_town_guard_perk(self, challenge_value):
    frosthaven = app_tables.frosthaven.search()[0]

    if int((challenge_value+frosthaven['TownGuardCheckMarks'])/3) > int(frosthaven['TownGuardCheckMarks']/3):
      return True
    return False

  def get_town_guard_string(self):
    player_string = ''
    
    challenge_value = self.get_challenge_value()
    if challenge_value:
      player_string += f"  - Town Guard Check Marks: {challenge_value}"
      if self.check_if_town_guard_perk(challenge_value):
        player_string += "\n  - New Town Guard Perk!"
    
    return player_string
        
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

    if player_name == 'Frosthaven':
      player_string += self.get_town_guard_string()

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
        town_guard_checks = self.get_challenge_value()
        if town_guard_checks > 0:
          database_entry['TownGuardCheckMarks'] += town_guard_checks
      else:
        database_entry = app_tables.characters.get(Player=player_name)

        experience = self.get_experience(player_resources)
        
        Utilites.add_experience(database_entry, experience)
        
        gold = self.get_gold(player_resources)
        if gold > 0:
          database_entry["Gold"] += gold

        if player_resources["CheckMarks"]:
          Utilites.add_checkmarks(database_entry, player_resources["CheckMarks"] or 0)

      for resource_name in resource_names:
        if not player_resources[resource_name]:
          continue
        database_entry[resource_name] += player_resources[resource_name] or 0
      database_entry.update()

    recommended_scenario_difficulty = Utilites.update_recommended_party_level()
    if recommended_scenario_difficulty:
      alert(f"New recommended party level: {recommended_scenario_difficulty['Level']}")

    navigation.go_to_outpost()


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
      

