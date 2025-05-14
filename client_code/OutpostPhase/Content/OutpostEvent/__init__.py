from ._anvil_designer import OutpostEventTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class OutpostEvent(OutpostEventTemplate):
  def __init__(self, gamestate, finish_phase_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.finish_phase_tag = finish_phase_tag
    self.gamestate = gamestate

    self.finished = gamestate[finish_phase_tag]

    self.finished = True

    if self.finished:
      self.disable_phase()
      
  def disable_phase(self):
    self.outpost_event_card.background = 'theme:Outline'

  def set_as_finished(self):
    self.disable_phase()
    self.gamestate[self.finish_phase_tag] = True
    self.raise_event('x-phase-finished')
    
