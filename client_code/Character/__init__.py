from ._anvil_designer import CharacterTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
from anvil.js.window import window


class Character(CharacterTemplate):
  def __init__(self, player, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.adjust_width()
    
    self.player = player
    self.item = app_tables.characters.get(Player=self.player)
  
    self.set_experience()
    self.set_perks()

    self.populate_class_drop_down()

  def adjust_width(self):
    if window.innerWidth < 900:
      column_width = (window.innerWidth / 3) - 10
      data_grid_columns = self.data_grid_1.columns
      for column in data_grid_columns:
        column['width'] = column_width
      self.data_grid_1.columns = data_grid_columns
    
  def populate_class_drop_down(self):
    item_list = []
    for row in app_tables.classes.search():
      item_list.append((row['Name'], row))
    self.class_drop_down.items = item_list

  def set_experience(self):
    experience = self.experience_text_box.text or 0
    self.item['Level'] = Utilites.get_level(experience)
    self.level_text_box.text = self.item['Level']    

  def experience_text_box_change(self, **event_args):
    self.set_experience()

  def retire_button_click(self, **event_args):
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
    
    app_tables.retired_characters.add_row(Player=self.player,Name=name, Experience=experience, Level=level, Class=character_class, Perks=perks, Mastery1=master1, Mastery2=master2)

  def transfer_all_to_frosthaven(self): 
    frosthaven = app_tables.frosthaven.search()[0]
    frosthaven['Lumber'] += self.lumber_text_box.text
    frosthaven['Metal'] += self.metal_text_box.text
    frosthaven['Hide'] += self.hide_text_box.text
    frosthaven['Arrowvine'] += self.arrowvine_text_box.text
    frosthaven['Axenut'] += self.axenut_text_box.text
    frosthaven['Corpsecap'] += self.corpsecap_text_box.text
    frosthaven['Flamefruit'] += self.flamefruit_text_box.text
    frosthaven['Rockroot'] += self.rockroot_text_box.text
    frosthaven['Snowthistle'] += self.rockroot_text_box.text
    frosthaven['Prosperity'] += 2

  def reset_character(self):
    experience = 0
    level = Utilites.get_level(experience=experience)
    
    self.item.update(
      Name='',
      Experience=experience,
      Level=level,
      Gold=0,
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
      Perks=0,
      Mastery1=False,
      Mastery2=False,
      Notes=''
    )

    self.parent.parent.change_form(Character(self.player))

  def set_perks(self):
    check_marks = self.check_marks_text_box.text or 0
    perks = int(check_marks/3) + int(self.mastery_check_box_1.checked) + int(self.mastery_check_box_2.checked)
    self.item['Perks'] = perks
    self.perk_text_box.text = perks

  def perks_change(self, **event_args):
    self.set_perks()