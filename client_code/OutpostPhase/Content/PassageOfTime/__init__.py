from ._anvil_designer import PassageOfTimeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PassageOfTime(PassageOfTimeTemplate):
  def __init__(self, gamestate, finish_phase_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.finish_phase_tag = finish_phase_tag

    self.gamestate = gamestate
    self.item = gamestate['Week']
    self.finished = gamestate[finish_phase_tag]
    
    if self.finished:
      self.disable_phase()
      
    self.setup_section()

  def setup_section(self):
    if self.item['Sections'].strip():
      self.sections_repeating_panel.items = [{'Section': section, 'Clicked': False} for section in self.item['Sections'].replace(' ', '').split(',')]
      self.sections_repeating_panel.set_event_handler('x-section-clicked', self.section_clicked)
      self.sections_finished = False
    else:
      self.sections_repeating_panel.visible = False
      self.sections_label.text = 'No Sections this week'
      self.sections_finished = True

  def disable_phase(self):
    self.week_passed_check_box.enabled = False
    self.passage_card.background = 'theme:Outline'

  def set_as_finished(self):
    self.disable_phase()
    self.gamestate[self.finish_phase_tag] = True
    self.raise_event('x-phase-finished')

  def section_clicked(self, **event_args):
    if self.finished:
      return
      
    for item in  self.sections_repeating_panel.items:
      if not item['Clicked']:
        return
    self.sections_finished = True
    
    if self.item['Finished']:
      self.set_as_finished()
      
  def week_passed_check_box_change(self, **event_args):
    self.week_passed_check_box.enabled = False
    if self.sections_finished:
      self.set_as_finished()
