from ._anvil_designer import ScenariosTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Scenarios(ScenariosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #self.scenario_repeating_panel.items = app_tables.scenarios.search(q.not_(Status='Undiscovered'))
    self.scenario_repeating_panel.items = app_tables.scenarios.search(Status=q.any_of('Available', 'Finished', 'Locked'))
    self.populate_unlock_scenario_drop_down()

  def populate_unlock_scenario_drop_down(self):
    item_list = []
    for row in app_tables.scenarios.search(Status='Undiscovered'):
      item_list.append((row['Number'], row))
    self.unlock_scenario_drop_down.items = item_list

  def add_scenario_button_click(self, **event_args):
    scenario = self.unlock_scenario_drop_down.selected_value
    if not confirm(f"Do you want to add scenario {scenario['Number']}?"):
      return
    scenario['Status'] = 'Available'
    scenario.update()
    self.scenario_repeating_panel.items = app_tables.scenarios.search(q.not_(Status='Undiscovered'))
    self.populate_unlock_scenario_drop_down()

  def status_button_click(self, **event_args):
    if event_args['sender'].role == 'filled-button':
      event_args['sender'].role = 'elevated-button'
    else:
      event_args['sender'].role = 'filled-button'
      self.add_status_filter(event_args['sender'].text)