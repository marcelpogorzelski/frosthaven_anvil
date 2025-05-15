from ._anvil_designer import PlantingTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....... import Utilites

import anvil.js

def scale_up_icon(component, scale=2):
  dom_node = anvil.js.get_dom_node(component)
  for icon in dom_node.querySelectorAll('i'):
    icon.style.fontSize = f'{scale}em'
    
class Planting(PlantingTemplate):
  def __init__(self, frosthaven, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    for herb in Utilites.HERB_RESOURCES:
      if frosthaven[herb] == 0:
        continue
      plant_button = Button(icon=f'_/theme/garden/{herb.lower()}-plot.png', role='elevated-button', tag=herb)
      plant_button.add_event_handler('click', self.plant)
      scale_up_icon(plant_button, 10)
      self.plant_flow_panel.add_component(plant_button)

  def plant(self, **event_args):
    self.raise_event("x-close-alert", value=event_args['sender'].tag)