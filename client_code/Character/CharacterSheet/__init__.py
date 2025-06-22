from ._anvil_designer import CharacterSheetTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .SelectClass import SelectClass
from ... import Utilites
from ... import navigation
from anvil.js.window import window
import re
from ..CharacterPerks.PerksItemTemplate.PerkIcon import PerkIcon

def extract_slots(text):
  matches = re.findall(r'\{([^}]*)\}', text)
  return matches


class CharacterSheet(CharacterSheetTemplate):
  def __init__(self, player, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.adjust_width()

    self.player_name = player
    self.item = app_tables.characters.get(Player=self.player_name)

    self.display_class_image()
    self.set_mastery_rich_text()

  def adjust_width(self):
    width = 900
    if window.innerWidth < 900:
      width = window.innerWidth
    return width

  def display_class_image(self):######################
    self.class_image.source = f"_/theme/class_icons/{self.item['Class']['Nickname'].lower()}.png"

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
    if len(self.item["Items"]) > 0:
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
    text_box = event_args["sender"]
    Utilites.bounded_text_box(text_box, 0, 10000)
    self.item[text_box.tag] = text_box.text or 0

  def add_dropboxes(self, perks_info):
    for perk in perks_info:
      count = perk['count']
      if perk['count'] == 0.5:
        count = 2
      elif perk['count'] == 0.3:
        count = 3
      perk['dropboxes'] = [False] * count
      
  def change_class_button_click(self, **event_args):
    char_class = alert(SelectClass(), title="Select Class", dismissible=False, buttons=[('Cancel', None)])
    if not char_class:
      return

    self.item['Class'] = char_class
    self.display_class_image()
    perks_info = self.item['Class']['PerksInfo']
    self.add_dropboxes(perks_info)
    self.item['PerksInfo'] = perks_info

  def set_mastery_rich_text(self):
    self.mastery_rich_text_1.content =self.item['Class']['MasteriesInfo'][0]
    self.mastery_rich_text_2.content =self.item['Class']['MasteriesInfo'][1]
    #self.mastery_rich_text_1.content ='asdfa <img src="_/theme/perk_icons/item_minus_1.webp" width="35" height="27"> sasfd'
    return
    slots = extract_slots(self.item['Class']['MasteriesInfo'][0])
    self.mastery_rich_text_1.content = self.item['Class']['MasteriesInfo'][0]
    for slot in slots:
      self.mastery_rich_text_1.add_component(PerkIcon(slot), slot=slot)

    slots = extract_slots(self.item['Class']['MasteriesInfo'][1])
    self.mastery_rich_text_2.content = self.item['Class']['MasteriesInfo'][1]
    for slot in slots:
      self.mastery_rich_text_2.add_component(PerkIcon(slot), slot=slot)
    
