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
    self.perk_rich_text.content = "{check1}" + "{check2}" + "{check3}" + self.item['desc']
    #self.perk_rich_text.add_component(ThreeChecks(), slot='drop')
    self.perk_rich_text.add_component(CheckBox(text=None), slot='check1')
    self.perk_rich_text.add_component(CheckBox(text=None), slot='check2')
    self.perk_rich_text.add_component(CheckBox(text=None), slot='check3')
    for slot in slots:
      self.perk_rich_text.add_component(PerkIcon(slot), slot=slot)
