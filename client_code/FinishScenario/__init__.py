from ._anvil_designer import FinishScenarioTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class FinishScenario(FinishScenarioTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.finish_scenario_repeating_panel.items = [
      {'Player': 'Håvard'},
      {'Player': 'John Magne'},
      {'Player': 'Kristian'},
      {'Player': 'Marcel'},
      {'Player': 'Frosthaven'},
    ]

  def finish_scenario_outlined_button_click(self, **event_args):
    for player in self.finish_scenario_repeating_panel.get_components():
      print(player.item['Player'])