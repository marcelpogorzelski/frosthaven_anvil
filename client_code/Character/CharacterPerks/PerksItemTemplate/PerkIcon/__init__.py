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
    #height = 22
    #if perk_file == 'heal.png':
      height = 20
    self.image_1.source = f"_/theme/perk_icons/{perk_file}"
    self.image_1.height = height
