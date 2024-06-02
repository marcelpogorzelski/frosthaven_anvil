from ._anvil_designer import CharacterTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites


class Character(CharacterTemplate):
  def __init__(self, player,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.player = player
    self.item = app_tables.characters.get(Player=self.player)
  
    self.level_text_box.text = Utilites.get_level(self.item['Experience'])

    self.populate_class_drop_down()
    
  def populate_class_drop_down(self):
    item_list = []
    for row in app_tables.classes.search():
      item_list.append((row['Name'], row))
    self.class_drop_down.items = item_list

  def experience_text_box_change(self, **event_args):
    level = Utilites.get_level(self.experience_text_box.text)
    if level != self.item['Level']:
      self.item['Level'] = level
      #self.item.update()
      self.refresh_data_bindings()
    #self.level_text_box.text = Utilites.get_level(self.experience_text_box.text)



