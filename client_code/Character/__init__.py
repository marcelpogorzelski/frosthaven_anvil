from ._anvil_designer import CharacterTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .CharacterSheet import CharacterSheet
from .CharacterItems import CharacterItems
from .CharacterCards import CharacterCards
from .CharacterDetails import CharacterDetails
from ..Utilites import windowWidthWithMax
from itertools import cycle, islice


class Character(CharacterTemplate):
  def __init__(self, player_name, tab='CharacterSheet', **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.player_name = player_name

    #tabs = ['CharacterItems', 'CharacterItems', 'CharacterCards', 'CharacterDetails']
    #tab = islice(cycle(tabs),tab,None)

    if tab == 'CharacterItems':
      self.open_items()
    elif tab == 'CharacterCards':
      self.open_cards()
    elif tab == 'CharacterDetails':
      self.open_details()
    else:
      self.open_sheet()

  def set_tab(self, selected_link):
    for tab_card in self.tab_column_panel.get_components():
      tab_card.background = ''
      tab_card.get_components()[0].foreground = ''

    selected_link.foreground = 'theme:Secondary Container'
    selected_link.parent.background = 'theme:Secondary'

  def open_tab(self, character_form, width=None):
    self.content_flow_panel.clear()
    if width:
      self.content_flow_panel.add_component(character_form, width=width)
    else:
      self.content_flow_panel.add_component(character_form)

  def open_sheet(self):
    self.set_tab(self.sheet_link)
    self.open_tab(CharacterSheet(self.player_name), 900)

  def open_items(self):
    self.set_tab(self.items_link)
    self.open_tab(CharacterItems(self.player_name))

  def open_cards(self):
    self.set_tab(self.cards_link)
    self.open_tab(CharacterCards(self.player_name))

  def open_details(self):
    self.set_tab(self.details_link)
    self.open_tab(CharacterDetails(self.player_name))
    
  def sheet_link_click(self, **event_args):
    self.open_sheet()

  def items_link_click(self, **event_args):
    self.open_items()

  def cards_link_click(self, **event_args):
    self.open_cards()

  def details_link_click(self, **event_args):
    self.open_details()
