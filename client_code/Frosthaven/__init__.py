from ._anvil_designer import FrosthavenTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import window
from .Content import Content


class Frosthaven(FrosthavenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    width = 900
    if window.innerWidth < 900:
      width = window.innerWidth
      
    self.content_flow_panel.add_component(Content(), width=width)
