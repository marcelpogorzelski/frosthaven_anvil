from ._anvil_designer import BarracksTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


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

    self.phase_enabled = True
    self.refresh_data_bindings()
    
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
    if self.count_text_box.text == self.max_recruit:
      self.count_increase_button.enabled = False
    self.count_decrease_button.enabled = True

  def count_decrease_button_click(self, **event_args):
    self.count_text_box.text -= 1
    if self.count_text_box.text == 0:
      self.count_decrease_button.enabled = False
    self.count_increase_button.enabled = True
    
