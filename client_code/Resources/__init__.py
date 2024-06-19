from ._anvil_designer import ResourcesTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Resources(ResourcesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.item = app_tables.frosthaven.search()[0]
    self.character_repeating_panel.items = app_tables.characters.search(tables.order_by('Player'))
    self.total_data_row_panel.item = self.get_resources()

  def get_resources(self):
    total_resources = {'Name': 'Total', 'Gold': 0, 'Lumber': 0, 'Metal': 0, 'Hide': 0, 'Arrowvine': 0, 'Axenut': 0, 'Corpsecap': 0, 'Flamefruit': 0, 'Rockroot': 0, 'Snowthistle': 0}

    for character in self.character_repeating_panel.get_components():
      total_resources['Gold'] += character.player_gold_text_box.text
      total_resources['Lumber'] += character.player_lumber_text_box.text
      total_resources['Metal'] += character.player_metal_text_box.text
      total_resources['Hide'] += character.player_hide_text_box.text
      total_resources['Arrowvine'] += character.player_arrowvine_text_box.text
      total_resources['Axenut'] += character.player_axenut_text_box.text
      total_resources['Corpsecap'] += character.player_corpsecap_text_box.text
      total_resources['Flamefruit'] += character.player_flamefruit_text_box.text
      total_resources['Rockroot'] += character.player_rockroot_text_box.text
      total_resources['Snowthistle'] += character.player_snowthistle_text_box.text

    total_resources['Gold'] += self.frosthaven_gold_text_box.text
    total_resources['Lumber'] += self.frosthaven_lumber_text_box.text
    total_resources['Metal'] += self.frosthaven_metal_text_box.text
    total_resources['Hide'] += self.frosthaven_hide_text_box.text
    total_resources['Arrowvine'] += self.frosthaven_arrowvine_text_box.text
    total_resources['Axenut'] += self.frosthaven_axenut_text_box.text
    total_resources['Corpsecap'] += self.frosthaven_corpsecap_text_box.text
    total_resources['Flamefruit'] += self.frosthaven_flamefruit_text_box.text
    total_resources['Rockroot'] += self.frosthaven_rockroot_text_box.text
    total_resources['Snowthistle'] += self.frosthaven_snowthistle_text_box.text

    return total_resources
    
  def total_row_replace(self):
    self.data_grid_1.get_components()[-1].remove_from_parent()
    row = DataRowPanel(item=self.get_resources())
    self.data_grid_1.add_component(row)

  def text_box_change(self, **event_args):
    self.total_row_replace()
