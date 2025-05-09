from ._anvil_designer import ScenariosRowTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import navigation
from ... import Utilites

class ScenariosRowTemplate(ScenariosRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.check_name_link_availability()
    self.status_drop_down.items = Utilites.get_scenario_statuses(self.item)

  def check_name_link_availability(self):
    if self.item['Status'] not in Utilites.SCENARIO_NOT_AVAILABLE:
      self.name_button.enabled = True
      return
    self.name_button.enabled = False
    
  def foregroud_color(self, hex):
    red, green, blue = tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
    
    cieY = (((red/255.0) ** 2) *  0.2126 ) + (((green/255.0) ** 2) *  0.7152) + (((blue/255.0) ** 2) *  0.0722)
    if cieY < 0.36:
      return "#ffffff"
    else:
      return "#000000"

  def name_button_click(self, **event_args):
    navigation.go_to_scenario(self.item)

  def status_drop_down_change(self, **event_args):
    self.item['Status'] = self.status_drop_down.selected_value
    self.check_name_link_availability()
