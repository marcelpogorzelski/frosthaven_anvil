from ._anvil_designer import Character_oldTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites

class Character_old(Character_oldTemplate):
  def __init__(self, player, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.player = player
    self.character = app_tables.characters.get(Player=self.player)
    #self.character = anvil.server.call('get_character_by_player', player)
    self.experience_text_box.text = self.character['Experience']
    self.level_text_box.text = Utilites.get_level(self.character['Experience'])
    self.name_text_box.text = self.character['Name']
    self.notes_text_area.text = self.character['Notes']
    self.populate_class_drop_down()
    self.populate_resource_panel()

  def populate_resource_panel(self):
    self.gold_text_box.text = self.character['Gold']
    self.lumber_text_box.text = self.character['Lumber']
    self.metal_text_box.text = self.character['Metal']
    self.hide_text_box.text = self.character['Hide']
    self.arrowvine_text_box.text = self.character['Arrowvine']
    self.axenut_text_box.text = self.character['Axenut']
    self.corpsecap_text_box.text = self.character['Corpsecap']
    self.flamefruit_text_box.text = self.character['Flamefruit']
    self.rockroot_text_box.text = self.character['Rockroot']
    self.snowthistle_text_box.text = self.character['Snowthistle']
    
  def populate_class_drop_down(self):
    #item_list = anvil.server.call('get_classes')
    item_list = []
    for row in app_tables.classes.search():
      item_list.append((row['Name'], row['Name']))
    self.class_drop_down.items = item_list
    self.class_drop_down.selected_value = self.character['Class']
    # Any code you write here will run before the form opens.

  def change_character_value(self, new_value, key):
    self.character[key] = new_value
    self.character.update()
    if key == 'Experience':
      self.level_text_box.text = Utilites.get_level(self.character[key])

  def inc_button_click(self, **event_args):
    new_value = event_args['sender'].tag.text + 1
    event_args['sender'].tag.text = new_value
    self.change_character_value(new_value, event_args['sender'].tag.tag)


  def dec_button_click(self, **event_args):
    new_value = event_args['sender'].tag.text - 1
    event_args['sender'].tag.text = new_value
    self.change_character_value(new_value, event_args['sender'].tag.tag)

  def class_drop_down_change(self, **event_args):
    self.change_character_value(event_args['sender'].selected_value, 'Class')

  def text_box_pressed_enter(self, **event_args):
    self.change_character_value(event_args['sender'].text, event_args['sender'].tag)

  def text_box_change(self, **event_args):
    self.change_character_value(event_args['sender'].text, event_args['sender'].tag)
