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
    self.name_label.text = f"{self.item['Character']['Player']} ({self.item['Character']['Gold']})"

    self.gold_text_box.text = self.item['Payment']
    self.max_amount = min(self.item['Character']['Gold'], self.item['Cost'])
    self.set_buttons()

  def set_cost(self):
    bounded_text_box(self.gold_text_box, 0, self.max_amount)
    self.item['Payment'] = self.gold_text_box.text
    self.set_buttons()
    self.parent.raise_event('x-update-gold')

  def set_buttons(self):
    self.decrease_button.enabled = self.gold_text_box.text > 0
    self.increase_button.enabled = self.gold_text_box.text < self.max_amount

  def decrease_button_click(self, **event_args):
    self.gold_text_box.text -= 1
    self.set_cost()

  def increase_button_click(self, **event_args):
    self.gold_text_box.text += 1
    self.set_cost()

  def gold_text_box_change(self, **event_args):
    self.set_cost()
