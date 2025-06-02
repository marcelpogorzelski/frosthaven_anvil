from ._anvil_designer import ScenariosTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Utilites

class Scenarios(ScenariosTemplate):
  def __init__(self, **properties):
    self.available = False
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.scenario_drop_down.items = [(scenario['Number'], scenario) for scenario in app_tables.scenarios.search()]
    self.change_scenario(change=True)

  def get_scenario_statuses(self):
    self.status_drop_down.items = Utilites.get_scenario_statuses(self.item)

  def change_scenario(self, change=False):
    self.item = self.scenario_drop_down.selected_value
    self.available = self.item['Status'] != 'Undiscovered'

    if change:
      self.get_scenario_statuses()
    
    self.refresh_data_bindings()

  def scenario_drop_down_change(self, **event_args):
    self.change_scenario(change=True)

  def status_drop_down_change(self, **event_args):
    self.item['Status'] = self.status_drop_down.selected_value
    self.change_scenario()
