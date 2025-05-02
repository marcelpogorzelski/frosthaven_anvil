from ._anvil_designer import UnlockEditTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from .. import Frosthaven_info
from .Scenarios import Scenarios
from .Items import Items
from .Buildings import Buildings
from .Classes import Classes
from .Pets import Pets

class UnlockEdit(UnlockEditTemplate):
  def __init__(self, **properties):
    
    self.scenarios_form = Scenarios()
    self.items_form = Items()
    self.buildings_form = Buildings()
    self.classes_from = Classes()
    self.pets_form = Pets()
    
    self.init_components(**properties)

    self.change_form(self.scenarios_form)
    
    self.flow_panel_2.add_component(self.scenarios_form)
    self.flow_panel_2.add_component(self.items_form)
    self.flow_panel_2.add_component(self.buildings_form)
    self.flow_panel_2.add_component(self.classes_from)
    self.flow_panel_2.add_component(self.pets_form)
    

  def reset_forms(self):
    self.scenarios_form.visible = False
    self.items_form.visible = False
    self.buildings_form.visible = False
    self.classes_from.visible = False
    self.pets_form.visible = False

  def change_form(self, form):
    self.reset_forms()
    form.visible = True

  def radio_button_clicked(self, **event_args):
    self.change_form(event_args['sender'].tag)
    
    




