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
    
    self.item = self.gamestate['Week']

    self.phases = list()
    self.finish = False

    self.passage_of_time = PassageOfTime(self.gamestate, Utilites.PASSAGE_OF_TIME_PHASE)
    self.passage_of_time.set_event_handler('x-phase-finished', self.phase_finished)
    self.phases.append(self.passage_of_time)
    self.add_component(self.passage_of_time)

    self.outpost_event = OutpostEvent(self.gamestate, Utilites.OUTPOST_EVENT_PHASE)
    self.outpost_event.set_event_handler('x-phase-finished', self.phase_finished)
    self.phases.append(self.outpost_event)
    self.add_component(self.outpost_event)

    self.building_operations = BuildingOperations(self.gamestate)
    self.building_operations.set_event_handler('x-phase-finished', self.phase_finished)
    self.phases.append(self.building_operations)
    self.add_component(self.building_operations)

    self.finish_week_button = Button(text='Go on an adventure!', role='filled-button')
    self.finish_week_button.set_event_handler('click', self.finish_week)

    self.finish_card = ColumnPanel(role='elevated-card')
    self.finish_card.add_component(self.finish_week_button)
    self.add_component(self.finish_card)


  def phase_finished(self, **event_args):
    for phase in self.phases:
      if not phase.finished:
        return
    self.disable_phase()

  def disable_phase(self):
    self.week_card.background = 'theme:Outline'
    self.finish = True

  def finish_week(self, **event_args):
    if not self.finish:
      if not confirm("All Outpost Phases are not finished. Do you still want to leave?"):
        return
    