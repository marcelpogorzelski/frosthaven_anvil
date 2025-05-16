from ._anvil_designer import OutpostEventTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator
from .... import Utilites


class OutpostEvent(OutpostEventTemplate):
  def __init__(self, gamestate, finish_phase_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #
    self.finish_phase_tag = finish_phase_tag
    self.gamestate = gamestate

    self.finished = gamestate[finish_phase_tag]

    self.season_backgrounds = {
      'Summer': '#FFFFAD',
      'Winter': '#ADD8E6'
    }
    self.check_season()
    self.draw_event_button.text = f"Draw {self.season} Outpost Event"
    
    self.check_outpost_event()

    if self.finished:
      self.disable_phase()

  def check_season(self):
    if Utilites.is_summer():
      self.season = 'Summer'
      self.wrong_season = 'Winter'
    else:
      self.season = 'Winter'
      self.wrong_season = 'Summer'

  def enable_event_card(self):
    self.button_flow_panel.visible = False
    self.draw_event_button.enabled = False
    self.draw_event_button.visible = False
    self.wrong_season_button.enabled = False
    self.wrong_season_button.visible = False
    self.card_label.text = self.current_outpost_event['Label']
    self.card_card.background = self.current_outpost_event['Background']
    self.event_number_button.text = self.current_outpost_event['Text']
    self.card_card.visible = True

  def check_outpost_event(self):
    self.current_outpost_event = self.gamestate['CurrentOutpostEvent']
    if self.current_outpost_event:
      self.enable_event_card()

  def disable_phase(self):
    self.outpost_event_card.background = 'theme:Outline'
    self.remove_button.enabled = False
    self.remove_button.visible = False
    self.return_button.enabled = False
    self.return_button.visible = False
    self.draw_event_button.enabled = False
    self.draw_event_button.visible = False
    self.wrong_season_button.enabled = False
    self.wrong_season_button.visible = False

  def set_as_finished(self):
    self.disable_phase()
    self.finished = True
    self.gamestate[self.finish_phase_tag] = True
    self.raise_event('x-phase-finished')

  def event_number_button_click(self, **event_args):
    event_number = self.event_number_button.text
    forteller_search_value = f"{self.card_label.text} Event {event_number:02}"
    navigator.clipboard.writeText(forteller_search_value)
    Notification("Event copied to clipboard. Go to forteller.gg", timeout=6).show()

  def get_outpost_event(self, season):
    event_number = Utilites.get_next_event(f"{season} Outpost")
    self.current_outpost_event = dict()
    self.current_outpost_event['Label'] = f"{season} Outpost"
    self.current_outpost_event['Background'] = self.season_backgrounds[season]
    self.current_outpost_event['Number'] = event_number
    self.current_outpost_event['Text'] = f"{event_number:02}"
    self.gamestate['CurrentOutpostEvent'] = self.current_outpost_event
    self.enable_event_card()

  def draw_event_button_click(self, **event_args):
    self.get_outpost_event(self.season)
    

  def wrong_season_button_click(self, **event_args):
    if not confirm(f"Draw {self.wrong_season} Outpost Event instead?"):
      return
    self.get_outpost_event(self.wrong_season)

  def return_button_click(self, **event_args):
    if not confirm(f"Do you want to return {self.current_outpost_event['Label']} Event {self.current_outpost_event['Text']} to the bottom of the deck?"):
      return
    Utilites.return_current_event(self.current_outpost_event['Label'])
    self.set_as_finished()

  def remove_button_click(self, **event_args):
    if not confirm(f"Do you want to remove {self.current_outpost_event['Label']} Event {self.current_outpost_event['Text']}?"):
      return
    Utilites.remove_current_event(self.current_outpost_event['Label'])
    self.set_as_finished()
    
