from ._anvil_designer import OutpostPhaseTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .BuldingOperations import BuldingOperations
from .PassageOfTime import PassageOfTime
from ..Utilites import windowWidthWithMax


class OutpostPhase(OutpostPhaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    width, remaingingWidth = windowWidthWithMax()
    self.content_flow_panel.add_component(PassageOfTime(), width=width)

    self.content_flow_panel.add_component(Spacer(height=0), width=remaingingWidth)
    self.content_flow_panel.add_component(BuldingOperations(), width=width)
    # Any code you write here will run before the form opens.
