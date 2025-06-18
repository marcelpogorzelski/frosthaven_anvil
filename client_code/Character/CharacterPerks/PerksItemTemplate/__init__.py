from ._anvil_designer import PerksItemTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .PerkIcon import PerkIcon
from .TwoChecks import TwoChecks
from .ThreeChecks import ThreeChecks

import re

def extract_slots(text):
  matches = re.findall(r'\{([^}]*)\}', text)
  return matches

class PerksItemTemplate(PerksItemTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    slots = extract_slots(self.item['desc'])
    self.perk_rich_text.content = "{check0}" + "{check1}" + "{check2}" + "{two_check}" + "{three_check}" + self.item['desc']
    if self.item['count'] == 0.5:
      two_checks = TwoChecks(self.item)
      two_checks.set_event_handler('x-multi-checkbox-change', self.multi_checkbox_changed)
      self.perk_rich_text.add_component(two_checks, slot='two_check')
    elif self.item['count'] == 0.3:
      three_checks = ThreeChecks(self.item)
      three_checks.set_event_handler('x-multi-checkbox-change', self.multi_checkbox_changed)
      self.perk_rich_text.add_component(three_checks, slot='three_check')
    else:
      for index in range(self.item['count']):
        perk_checkbox = CheckBox(text=None, checked=self.item['dropboxes'][index], tag=index)
        perk_checkbox.set_event_handler('change', self.checkbox_changed)
        self.perk_rich_text.add_component(perk_checkbox, slot=f"check{index}")
        
    for slot in slots:
      self.perk_rich_text.add_component(PerkIcon(slot), slot=slot)

  def checkbox_changed(self, **event_args):
    perk_drop = event_args['sender']
    self.item['dropboxes'][perk_drop.tag] = perk_drop.checked
    self.parent.raise_event('x-checkbox-change')

  def multi_checkbox_changed(self, **event_args):
    self.parent.raise_event('x-checkbox-change')
