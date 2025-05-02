from ._anvil_designer import UnlockEditTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from .. import Frosthaven_info
from .Scenario import Scenario


class UnlockEdit(UnlockEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.scenario_form = Scenario()
    self.edit_card.add_component(self.scenario_form)

  def radio_button_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    pass
    
    




