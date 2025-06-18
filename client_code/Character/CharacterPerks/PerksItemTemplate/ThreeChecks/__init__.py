from ._anvil_designer import ThreeChecksTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ThreeChecks(ThreeChecksTemplate):
  def __init__(self, perk_info, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.perk_info = perk_info
    self.check_box_1.checked = perk_info['dropboxes'][0]
    self.check_box_2.checked = perk_info['dropboxes'][1]
    self.check_box_3.checked = perk_info['dropboxes'][2]

  def check_box_1_change(self, **event_args):
    self.perk_info['dropboxes'][0] = self.check_box_1.checked
    self.raise_event('x-multi-checkbox-change')

  def check_box_2_change(self, **event_args):
    self.perk_info['dropboxes'][1] = self.check_box_2.checked
    self.raise_event('x-multi-checkbox-change')

  def check_box_3_change(self, **event_args):
    self.perk_info['dropboxes'][2] = self.check_box_3.checked
    self.raise_event('x-multi-checkbox-change')