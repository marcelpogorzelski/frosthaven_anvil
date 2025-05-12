from ._anvil_designer import Character_oldTemplate
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
from anvil.js.window import window

class Character_old(Character_oldTemplate):
  def __init__(self, player, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.adjust_width()

    self.player_name = player
    self.item = app_tables.characters.get(Player=self.player_name)

    self.populate_class_drop_down()

  def adjust_width(self):
    if window.innerWidth >= 900:
      return
    column_width = (window.innerWidth / 3) - 10
    character_data_grid_columns = self.character_data_grid.columns
    for column in character_data_grid_columns:
      column['width'] = column_width
    self.character_data_grid.columns = character_data_grid_columns

    label_data_grid_columns = self.label_data_grid.columns
    label_data_grid_columns[0]['width'] = window.innerWidth - 30
    self.label_data_grid.columns = label_data_grid_columns
    

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
    Utilites.bounded_text_box(self.experience_text_box, 0, 500)
    Utilites.set_experience(self.item, self.experience_text_box.text or 0)
    self.refresh_data_bindings()

  def retire_button_click(self, **event_args):
    if len(self.item['Items']) > 0:
      alert("You have items left to sell")
      navigation.go_to_character_items(self.player_name)
      return
    if not confirm("Are you retiring?"):
      return
    
    Utilites.retire_character(self.item)
    navigation.go_to_character(self.player_name)

  def mastery_check_box_change(self, **event_args):
    mastery1 = self.mastery_check_box_1.checked
    mastery2 = self.mastery_check_box_2.checked
    Utilites.set_masteries(self.item, mastery1, mastery2)
    self.refresh_data_bindings()

  def check_marks_text_box_change(self, **event_args):
    Utilites.bounded_text_box(self.check_marks_text_box, 0, 18)
    Utilites.set_checkmarks(self.item, self.check_marks_text_box.text or 0)
    self.refresh_data_bindings()

  def text_box_change(self, **event_args):
    text_box = event_args['sender']
    Utilites.bounded_text_box(text_box, 0, 10000)
    self.item[text_box.tag] = text_box.text or 0
