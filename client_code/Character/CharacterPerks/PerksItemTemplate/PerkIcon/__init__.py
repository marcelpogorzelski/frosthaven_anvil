from ._anvil_designer import PerkIconTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PerkIcon(PerkIconTemplate):
  def __init__(self, perk_file, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    width = 22
    height = 22
    if perk_file == 'heal.png':
      width = 16
      height = 16
    if perk_file == 'item_minus_1.webp':
      width = 30
      height = 30

    perk_image = Image(source=f"_/theme/perk_icons/{perk_file}", height=height, display_mode='fill_width')
    self.flow_panel_1.add_component(perk_image, width=width)
    
