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
      self.perk_rich_text.add_component(TwoChecks(), slot='two_check')
    elif self.item['count'] == 0.3:
      self.perk_rich_text.add_component(ThreeChecks(), slot='three_check')
    else:
      for index in range(self.item['count']):
        self.perk_rich_text.add_component(CheckBox(text=None), slot=f"check{index}")
    
    for slot in slots:
      self.perk_rich_text.add_component(PerkIcon(slot), slot=slot)
