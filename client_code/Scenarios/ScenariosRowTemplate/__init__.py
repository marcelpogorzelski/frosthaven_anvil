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
    self.status_drop_down.items = Utilites.get_scenario_statuses(self.item)

  def check_name_link(self):
    if self.item['Status'] == Utilites:
      pass
    
  def foregroud_color(self, hex):
    red, green, blue = tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
    
    cieY = (((red/255.0) ** 2) *  0.2126 ) + (((green/255.0) ** 2) *  0.7152) + (((blue/255.0) ** 2) *  0.0722)
    if cieY < 0.36:
      return "#ffffff"
    else:
      return "#000000"

  def name_link_click(self, **event_args):
    navigation.go_to_scenario(self.item)
