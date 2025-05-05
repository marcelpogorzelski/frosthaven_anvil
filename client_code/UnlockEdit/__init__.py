from ._anvil_designer import UnlockEditTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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
from .Achievements import Achievements

class UnlockEdit(UnlockEditTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.setup_forms()
    self.forms['Scenarios']['instance'] = self.forms['Scenarios']['form']()
    self.current_form = self.forms['Scenarios']['instance']
    self.form_flow_panel.add_component(self.forms['Scenarios']['instance'])

  def setup_form(self, name, form, radio_button):
    self.forms[name] = {'form': form, 'instance': None}
    radio_button.tag = name

  def setup_forms(self):
    self.forms = dict()
    self.setup_form('Scenarios', Scenarios, self.scenario_radio_button)
    self.setup_form('Items', Items, self.item_radio_button)
    self.setup_form('Buildings', Buildings, self.building_radio_button)
    self.setup_form('Classes', Classes, self.class_radio_button)
    self.setup_form('Achievements', Achievements, self.achievement_radio_button)
    self.setup_form('Pets', Pets, self.pet_radio_button)

  def reset_forms(self):
    self.scenarios_form.visible = False
    self.items_form.visible = False
    self.buildings_form.visible = False
    self.classes_from.visible = False
    self.pets_form.visible = False
    self.achievements_form.visible = False

  def change_form(self, name):
    if not self.forms[name]['instance']:
      self.forms[name]['instance'] = self.forms[name]['form']()
      self.form_flow_panel.add_component(self.forms[name]['instance'])
    self.current_form.visible = False
    self.current_form = self.forms[name]['instance']
    self.current_form.visible = True

  def radio_button_clicked(self, **event_args):
    self.change_form(event_args['sender'].tag)
    
    




