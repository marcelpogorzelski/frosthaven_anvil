from ._anvil_designer import OutpostEventTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class OutpostEvent(OutpostEventTemplate):
  def __init__(self, finished, phase_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.phase_name = phase_name
    self.finished = finished
    if self.finished:
      self.disable_phase()
      
  def disable_phase(self):
    self.outpost_event_card.background = 'theme:Outline'

  def set_as_finished(self):
    self.disable_phase()
    if not self.finished:
      self.raise_event('x-phase-finished')
    
