from ._anvil_designer import FrosthavenTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Content import Content
from ..Utilites import windowWidthWithMax


class Frosthaven(FrosthavenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    width, _ = windowWidthWithMax()
      
    self.content_flow_panel.add_component(Content(), width=width)
