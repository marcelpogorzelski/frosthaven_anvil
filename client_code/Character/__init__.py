from ._anvil_designer import CharacterTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
from ..RetirePrompt import RetirePrompt
from anvil.js.window import window


class Character(CharacterTemplate):
  def __init__(self, player, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.adjust_width()
    
    self.player = player
    self.item = app_tables.characters.get(Player=self.player)
  
    self.level_text_box.text = Utilites.get_level(self.item['Experience'])

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

  def experience_text_box_change(self, **event_args):
    experience = self.experience_text_box.text or 0
    self.item['Level'] = Utilites.get_level(experience)
    self.level_text_box.text = self.item['Level']

  def retire_button_click(self, **event_args):
    if not confirm("Are you retiring?"):
      return
    
    self.retire_character()
    self.transfer_all_to_frosthaven()
    self.reset_character()

  def retire_character(self):
    retire_prompt = RetirePrompt()
    alert(content=retire_prompt)
    
    name = self.name_text_box.text
    experience = self.experience_text_box.text
    level = self.level_text_box.text
    character_class = self.class_drop_down.selected_value

    perks = retire_prompt.perk_checks_text_box.text
    master1 = retire_prompt.m1_check_box.checked
    master2 = retire_prompt.m2_check_box.checked
    
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
    self.item['Experience'] = 0
    self.item['Name'] = ''
    self.item['Level'] = Utilites.get_level(experience=self.item['Experience'])
    self.item['Gold'] = 0
    self.item['Lumber'] = 0
    self.item['Metal'] = 0
    self.item['Hide'] = 0
    self.item['Arrowvine'] = 0
    self.item['Axenut'] = 0
    self.item['Corpsecap'] = 0
    self.item['Flamefruit'] = 0
    self.item['Rockroot'] = 0
    self.item['Snowthistle'] = 0
    self.item['Notes'] = ''
    self.item.update()

    self.parent.parent.change_form(Character(self.player))
    