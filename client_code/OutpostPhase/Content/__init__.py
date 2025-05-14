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

    self.gamestate = app_tables.gamestate.search()[0]
    self.week = app_tables.gamestate.search()[0]['Week']
    self.item = app_tables.calendar.get(Week=self.gamestate['Week'])


    self.passage_of_time = PassageOfTime(self.item, self.gamestate['PassageOfTimeFinished'], Utilites.PASSAGE_OF_TIME_PHASE)
    self.passage_of_time.set_event_handler('x-phase-finished', self.phase_finished)
    self.add_component(self.passage_of_time)

    self.outpost_event = OutpostEvent(self.gamestate['OutpostEventFinished'], Utilites.OUTPOST_EVENT_PHASE)
    self.outpost_event.set_event_handler('x-phase-finished', self.phase_finished)
    self.add_component(self.outpost_event)
    
    self.add_component(BuildingOperations())
    # Any code you write here will run before the form opens.

  def phase_finished(self, **event_args):
    self.gamestate[event_args['sender'].phase_name] = True
    