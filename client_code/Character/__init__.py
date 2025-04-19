from ._anvil_designer import CharacterTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
from anvil.js.window import window
from math import ceil

class Character(CharacterTemplate):
  def __init__(self, player, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.adjust_width()

    self.player_name = player
    self.item = app_tables.characters.get(Player=self.player_name)

    self.set_experience()
    self.set_perks()

    self.populate_class_drop_down()

  def adjust_width(self):
    if window.innerWidth < 900:
      column_width = (window.innerWidth / 3) - 10
      data_grid_columns = self.data_grid_1.columns
      for column in data_grid_columns:
        column["width"] = column_width
      self.data_grid_1.columns = data_grid_columns

  def populate_class_drop_down(self):
    item_list = []
    for row in app_tables.classes.search():
      item_list.append((row["Name"], row))
    self.class_drop_down.items = item_list

  def set_experience(self):
    experience = self.experience_text_box.text or 0
    level, next_level_experience = Utilites.get_level(experience)
    if self.level_text_box.text != level:
      self.item["Level"] = level
      self.level_text_box.text = level
      self.item["NextLevelExperience"] = next_level_experience
      self.next_level_text_box.text = next_level_experience
      self.set_perks()

  def experience_text_box_change(self, **event_args):
    self.set_experience()

  def go_to_character_items(self):
    main_form = get_open_form()

    items_link = main_form.player_links[self.player_name]['Items Link']
    main_form.open_player_link(self.player_name, items_link)

  def retire_button_click(self, **event_args):
    if self.player_name == 'Håvard':
      item_list = app_tables.items.search(Available=True, Håvard=True)
      
    if self.player_name == 'Marcel':
      item_list = app_tables.items.search(Available=True, Marcel=True)
      
    if self.player_name == 'Kristian':
      item_list = app_tables.items.search(Available=True, Kristian=True)
      
    if self.player_name == 'John Magne':
      item_list = app_tables.items.search(Available=True, John_Magne=True)

    if len(item_list) > 0:
      alert("You have items left to sell")
      self.go_to_character_items()
      return
      
    if not confirm("Are you retiring?"):
      return

    self.retire_character()
    self.transfer_all_to_frosthaven()
    self.reset_character()

  def retire_character(self):
    name = self.name_text_box.text
    experience = self.experience_text_box.text
    level = self.level_text_box.text
    character_class = self.class_drop_down.selected_value

    perks = self.perk_text_box.text
    master1 = self.mastery_check_box_1.checked
    master2 = self.mastery_check_box_2.checked

    app_tables.retired_characters.add_row(
      Player=self.player_name,
      Name=name,
      Experience=experience,
      Level=level,
      Class=character_class,
      Perks=perks,
      Mastery1=master1,
      Mastery2=master2,
    )

  def transfer_all_to_frosthaven(self):
    frosthaven = app_tables.frosthaven.search()[0]
    frosthaven["Lumber"] += self.lumber_text_box.text
    frosthaven["Metal"] += self.metal_text_box.text
    frosthaven["Hide"] += self.hide_text_box.text
    frosthaven["Arrowvine"] += self.arrowvine_text_box.text
    frosthaven["Axenut"] += self.axenut_text_box.text
    frosthaven["Corpsecap"] += self.corpsecap_text_box.text
    frosthaven["Flamefruit"] += self.flamefruit_text_box.text
    frosthaven["Rockroot"] += self.rockroot_text_box.text
    frosthaven["Snowthistle"] += self.rockroot_text_box.text
    frosthaven["Prosperity"] += 2

  def reset_character(self):
    prosperity_level = Utilites.get_prosperity_level(app_tables.frosthaven.search()[0]["Prosperity"])

    starting_gold = (10 * prosperity_level) + 20
    starintg_level = ceil(prosperity_level / 2)

    starting_experience = Utilites.get_experience(starintg_level)
    next_level_experience = Utilites.get_experience(starintg_level + 1)

    retired_count = self.item['RetiredCount'] + 1
    starting_perks = starintg_level - 1 + retired_count

    self.item.update(
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

    self.parent.parent.change_form(Character(self.player_name))

  def set_perks(self):
    check_marks = self.check_marks_text_box.text or 0
    retired_count = self.item['RetiredCount']
    mastery_count = self.item['MasteryCount']
    level = self.item['Level'] - 1
    perks = int(check_marks / 3) + retired_count + mastery_count + level
    self.item["Perks"] = perks
    self.perk_text_box.text = perks

  def mastery_check_box_change(self, **event_args):
    mastery_perks_count = int(self.mastery_check_box_1.checked) + int(self.mastery_check_box_2.checked)
    self.item['MasteryCount'] = mastery_perks_count
    self.set_perks()

  def check_marks_text_box_change(self, **event_args):
    if self.check_marks_text_box.text > 18:
      self.check_marks_text_box.text = 18
    self.set_perks()
