from ._anvil_designer import BarracksTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .....Utilites import MATERIAL_RESOURCES, bounded_text_box
from ..CharacterPay import CharacterPay


class Barracks(BarracksTemplate):
  def __init__(self, gamestate, finish_phase_tag, **properties):
    self.phase_enabled = False
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.finish_phase_tag = finish_phase_tag
    self.gamestate = gamestate

    self.finished = gamestate[finish_phase_tag]
    if self.finished:
      self.disable_phase()

  def setup_barracks(self):
    self.barracks_level = app_tables.available_buildings.get(Number=98)['CurrentBuilding']['Level']
    self.guard_count = app_tables.frosthaven.search()[0]['Guards']

    self.max_guard_count = 2 + (self.barracks_level * 2)
    self.missing_quard_count = self.max_guard_count - self.guard_count

    if self.missing_quard_count == 0:
      self.set_as_finished()
    
    if self.missing_quard_count >= 2 and self.barracks_level >= 3:
      self.max_recruit = 2
    else:
      self.max_recruit = 1

    self.count_text_box.text = self.max_recruit
    
    self.missing_guard_label.text = f"Missing {self.missing_quard_count} guards"

    self.buy_count = int((self.barracks_level + 1) / 2)
    self.total_gold = self.buy_count * 3
    
    self.setup_material_resource( self.max_recruit)
    self.setup_character_pay()

    self.phase_enabled = True
    self.refresh_data_bindings()

  def setup_character_pay(self):
    self.character_pay_flow_panel.add_component(CharacterPay(self.total_gold), width=500)

  def setup_material_resource(self, max_recruit):
    self.frosthaven = app_tables.frosthaven.search()[0]

    resource_items = list()
    
    for resource in MATERIAL_RESOURCES:
      if self.frosthaven[resource] == 0:
        continue
      image = f"_/theme/resource_images/fh-{resource.lower()}-bw-icon.png"
      resource_item = {'Image': image, 'Resource': resource, 'Count': self.frosthaven[resource], 'MaxRecruit': max_recruit}
      resource_items.append(resource_item)
    
    self.meterial_repeating_panel.items = resource_items
    
  def disable_phase(self):
    self.barracks_column_panel.background = 'theme:Outline'
    self.phase_enabled = False
    self.refresh_data_bindings()

  def set_as_finished(self):
    self.disable_phase()
    #self.finished = True
    #self.gamestate[self.finish_phase_tag] = True
    #self.raise_event("x-building-finished")

  def start_button_click(self, **event_args):
    self.barracks_start_flow_panel.visible = False
    self.setup_barracks()

  def count_increase_button_click(self, **event_args):
    self.count_text_box.text += 1
    self.count_increase_button.enabled = self.count_text_box.text < self.max_recruit
    self.count_decrease_button.enabled = self.count_text_box.text > 0

  def count_decrease_button_click(self, **event_args):
    self.count_text_box.text -= 1
    self.count_increase_button.enabled = self.count_text_box.text < self.max_recruit
    self.count_decrease_button.enabled = self.count_text_box.text > 0

  def count_text_box_change(self, **event_args):
    bounded_text_box(self.count_text_box, 0, self.max_recruit)
    self.count_increase_button.enabled = self.count_text_box.text < self.max_recruit
    self.count_decrease_button.enabled = self.count_text_box.text > 0
    
    
