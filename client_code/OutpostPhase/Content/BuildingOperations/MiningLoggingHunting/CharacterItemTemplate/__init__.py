from ._anvil_designer import CharacterItemTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ......Utilites import bounded_text_box


class CharacterItemTemplate(CharacterItemTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    #self.character = app_tables.characters.get(Player=self.item['Player'])
    self.max_amount = self.item['Character']['Gold']
    self.name_label.text = f"{self.item['Character']['Player']} ({self.max_amount})"
    self.gold_text_box.text = self.item['Cost']
    if self.gold_text_box.text == 0:
      self.decrease_button.enabled = False
    if self.gold_text_box.text == self.max_amount:
      self.increase_button.enabled = False


  def set_cost(self):
    bounded_text_box(self.gold_text_box, 0, self.max_amount)
    self.item['Cost'] = self.gold_text_box.text
    self.parent.raise_event('x-funds-updated')
    

  def decrease_button_click(self, **event_args):
    self.gold_text_box.text -= 1

    if self.gold_text_box.text == 0:
      self.decrease_button.enabled = False
    if self.gold_text_box.text < self.max_amount:
      self.increase_button.enabled = True

    self.set_cost()

  def increase_button_click(self, **event_args):
    self.gold_text_box.text += 1

    if self.gold_text_box.text == self.max_amount:
      self.increase_button.enabled = False
    if self.gold_text_box.text > 0:
      self.decrease_button.enabled = True

    self.set_cost()

  def gold_text_box_change(self, **event_args):
    self.set_cost()
