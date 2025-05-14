from ._anvil_designer import BuildingOperationsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .MiningLoggingHunting import MiningLoggingHunting
from .... import Utilites


class BuildingOperations(BuildingOperationsTemplate):
  def __init__(self, gamestate, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.finish_phase_tag = Utilites.BUILDING_PHASE
    self.gamestate = gamestate

    self.finished = gamestate[self.finish_phase_tag]

    self.buildings = list()
    
    self.minig_logging_hunting = MiningLoggingHunting(self.gamestate, Utilites.BUILDING_MLH_PHASE)
    self.minig_logging_hunting.set_event_handler('x-building-finished', self.building_finished)
    self.buildings.append(self.minig_logging_hunting)
    self.building_operations_card.add_component(self.minig_logging_hunting)

  def disable_phase(self):
    self.building_operations_card.background = 'theme:Outline'

  def set_as_finished(self):
    self.disable_phase()
    self.gamestate[self.finish_phase_tag] = True
    self.raise_event('x-phase-finished')

  def building_finished(self, **event_args):
    for building in self.buildings:
      if not building.finished:
        return
    


    
