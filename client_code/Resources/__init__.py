from ._anvil_designer import ResourcesTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites


class Resources(ResourcesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.total_resources = {resource: 0 for resource in Utilites.ALL_RESOURCES}
    self.party_level = app_tables.scenario_info.get(Recommended=True)
    self.init_components(**properties)

    self.item = app_tables.frosthaven.search()[0]
    self.character_repeating_panel.items = app_tables.characters.search(tables.order_by('Player'))
    self.character_repeating_panel.set_event_handler('x-update-value', self.update_value)
    
    self.setup_tags()
    self.set_total_resources()
    self.refresh_data_bindings()

  def setup_tags(self):
    self.frosthaven_lumber_text_box.tag = 'Lumber'
    self.frosthaven_metal_text_box.tag = 'Metal'
    self.frosthaven_hide_text_box.tag = 'Hide'
    
    self.frosthaven_arrowvine_text_box.tag = 'Arrowvine'
    self.frosthaven_axenut_text_box.tag = 'Axenut'
    self.frosthaven_corpsecap_text_box.tag = 'Corpsecap'
    self.frosthaven_flamefruit_text_box.tag = 'Flamefruit'
    self.frosthaven_rockroot_text_box.tag = 'Rockroot'
    self.frosthaven_snowthistle_text_box.tag = 'Snowthistle'

  def update_value(self, **event_args):
    self.set_total_resources()
    self.refresh_data_bindings()
    

  def set_total_resources(self):
    self.total_resources = {resource: 0 for resource in Utilites.ALL_RESOURCES}

    for character in self.character_repeating_panel.get_components():
      for resource in Utilites.ALL_RESOURCES:
        self.total_resources[resource] += character.item[resource] or 0

    for resource in Utilites.MATERIAL_RESOURCES + Utilites.HERB_RESOURCES:
      self.total_resources[resource] += self.item[resource] or 0

  def text_box_change(self, **event_args):
    text_box = event_args['sender']
    Utilites.bounded_text_box(text_box, 0, 10000)
    self.item[text_box.tag] = text_box.text or 0
    self.set_total_resources()
    self.refresh_data_bindings()

    
