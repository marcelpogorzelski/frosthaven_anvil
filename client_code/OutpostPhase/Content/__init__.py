from ._anvil_designer import ContentTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .PassageOfTime import PassageOfTime
from .OutpostEvent import OutpostEvent
from .BuildingOperations import BuildingOperations
from ... import Utilites


class Content(ContentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.item = app_tables.calendar.search(tables.order_by("Week", ascending=True),Finished=False)[0]
    passage_enabled = False
    if app_tables.gamestate.search()[0]['Phase'] == Utilites.PASSAGE_PHASE:
      passage_enabled = True
    
    passage = PassageOfTime(self.item, passage_enabled)
    passage.set_event_handler('x-phase-finished', self.phase_finished)
    
    self.add_component(passage)
    self.add_component(OutpostEvent())
    self.add_component(BuildingOperations())
    # Any code you write here will run before the form opens.

  def phase_finished(self, **event_args):
    pass