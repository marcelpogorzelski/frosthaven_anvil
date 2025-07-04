from ._anvil_designer import ScenariosTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Scenarios(ScenariosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #self.scenario_repeating_panel.items = app_tables.scenarios.search(q.not_(Status='Undiscovered'))
    self.available_filter_button.role = 'filled-button'
    self.filter_on_status()

  def filter_on_status(self):
    status_filter_list = list()
    for filter_button in self.filter_flow_panel.get_components():
      if filter_button.role == 'filled-button':
        status_filter_list.append(filter_button.text)
    if not status_filter_list:
      self.scenario_repeating_panel.items = app_tables.scenarios.search(q.not_(Status='Undiscovered'))
    else:
      self.scenario_repeating_panel.items = app_tables.scenarios.search(Status=q.any_of(*status_filter_list))

  def status_button_click(self, **event_args):
    if event_args['sender'].role == 'filled-button':
      event_args['sender'].role = 'elevated-button'
    else:
      event_args['sender'].role = 'filled-button'
    self.filter_on_status()

  def foregroud_color(self, hex):
    red, green, blue = tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
    
    cieY = (((red/255.0) ** 2) *  0.2126 ) + (((green/255.0) ** 2) *  0.7152) + (((blue/255.0) ** 2) *  0.0722)
    if cieY < 0.36:
      return "#ffffff"
    else:
      return "#000000"
    
