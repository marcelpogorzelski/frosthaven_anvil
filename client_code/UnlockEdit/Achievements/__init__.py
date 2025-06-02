from ._anvil_designer import AchievementsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Utilites


class Achievements(AchievementsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.achievement_drop_down.items = [(achievement['Name'], achievement) for achievement in app_tables.achievements.search()]
    self.item = self.achievement_drop_down.selected_value

  def button_text(self):
    if self.item['Descriptor']:
      return f"Add new {self.item['Descriptor'][:-1]}"
    return ''

  def button_visible(self):
    if self.item['Upgrades'] == 0:
      return False
    if not self.item['Available']:
      return False
    if self.item['Upgrades'] == self.item['CurrentLevel']:
      return False
    return True
      
  def show_levels(self):
    if not self.item['Available']:
      return False
    if self.item['Upgrades']:
      return True
    return False

  def available_check_box_change(self, **event_args):
    if self.item['Connected'] and self.available_check_box.checked:
      self.item['Connected']['Available'] = False
    self.item['Available'] = self.available_check_box.checked
    if self.item['ScenarioCheck']:
      Utilites.set_scenario_available()
    self.achievement_image.visible = self.available_check_box.checked
    self.refresh_data_bindings()

  def achievement_drop_down_change(self, **event_args):
    self.item = self.achievement_drop_down.selected_value
    self.refresh_data_bindings()

  def upgrade_button_click(self, **event_args):
    self.item['CurrentLevel'] += 1
    self.refresh_data_bindings()
