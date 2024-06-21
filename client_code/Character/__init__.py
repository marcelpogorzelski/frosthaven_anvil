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
    level = Utilites.get_level(self.experience_text_box.text)
    if level != self.item['Level']:
      self.item['Level'] = level
      self.item.update()
      self.level_text_box.text = level
    # Any code you write here will run before the form opens.

  def retire_button_click(self, **event_args):
    if not confirm("Are you retiring?"):
      return
    retire_prompt = RetirePrompt()
    alert(content=retire_prompt)
    
    name = self.name_text_box.text
    experience = self.experience_text_box.text
    level = self.level_text_box.text
    character_class = self.class_drop_down.selected_value

    perks = retire_prompt.perks_text_box.text
    
    app_tables.retired_characters.add_row(Player=self.player,Name=name, Experience=experience, Level=level, Class=character_class, Perks=perks, Mastery1=None, Mastery2=None)
