from ._anvil_designer import PartyTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

class Party(PartyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = app_tables.frosthaven.search()[0]
    self.characters_repeating_panel.items = app_tables.characters.search(tables.order_by('Player'))
    self.scenario_info_repeating_panel.items = app_tables.scenario_info.search()
    self.set_party_level()
    self.scenario_info_repeating_panel.raise_event_on_children("x-hightlight-level", scenario_level=self.party_level_text_box.text)

  def set_party_level(self):
    adjust_level = self.adjust_level_text_box.text or 0
    
    total_levels = 0
    for character in self.characters_repeating_panel.items:
      total_levels += character['Level']
    average_level = math.ceil(total_levels / 4 / 2) + adjust_level
    self.party_level_text_box.text = average_level

  def adjust_level_text_box_change(self, **event_args):
    self.set_party_level()
    self.scenario_info_repeating_panel.raise_event_on_children("x-hightlight-level", scenario_level=self.party_level_text_box.text)

  def adjust_level_plus_button_click(self, **event_args):
    self.adjust_level_text_box.text = self.adjust_level_text_box.text + 1
    self.set_party_level()
    self.item['Adjust Level'] = self.adjust_level_text_box.text
    self.scenario_info_repeating_panel.raise_event_on_children("x-hightlight-level", scenario_level=self.party_level_text_box.text)
    
  def adjust_level_minus_button_click(self, **event_args):
    self.adjust_level_text_box.text = self.adjust_level_text_box.text - 1
    self.set_party_level()
    self.item['Adjust Level'] = self.adjust_level_text_box.text
    self.scenario_info_repeating_panel.raise_event_on_children("x-hightlight-level", scenario_level=self.party_level_text_box.text)
  