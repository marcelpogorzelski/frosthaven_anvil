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
from .CharacterPerks import CharacterPerks
from ..Utilites import windowWidthWithMax


class Character(CharacterTemplate):
  def __init__(self, player_name, tab='CharacterSheet', **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.player_name = player_name

    self.tabs = {
      'CharacterSheet': {'OpenForm': self.open_sheet, 'Next': 'CharacterPerks', 'Current': 'CharacterSheet'},
      'CharacterPerks': {'OpenForm': self.open_perks, 'Next': 'CharacterItems', 'Current': 'CharacterPerks'},
      'CharacterItems': {'OpenForm': self.open_items, 'Next': 'CharacterCards', 'Current': 'CharacterItems'},
      'CharacterCards': {'OpenForm': self.open_cards, 'Next': 'CharacterDetails', 'Current': 'CharacterCards'},
      'CharacterDetails': {'OpenForm': self.open_details, 'Next': 'CharacterSheet', 'Current': 'CharacterDetails'},
    }
    self.current_tab = self.tabs[tab]
    
    self.setup_label()
    self.current_tab['OpenForm']()

  def set_tab(self, selected_link):
    for tab_link in self.tab_column_panel.get_components():
      tab_card = tab_link.get_components()[0]
      tab_card.background = ''
      tab_card.get_components()[0].foreground = ''

    selected_link.foreground = 'theme:Secondary Container'
    selected_link.parent.background = 'theme:Secondary'

  def open_next_tab(self):
    self.current_tab = self.tabs[self.current_tab['Next']]
    self.current_tab['OpenForm']()

  def open_tab(self, character_form, width=None):
    self.content_flow_panel.clear()
    if width:
      self.content_flow_panel.add_component(character_form, width=width)
    else:
      self.content_flow_panel.add_component(character_form)

  def open_sheet(self):
    self.set_tab(self.sheet_label)
    self.open_tab(CharacterSheet(self.player_name), 900)

  def open_perks(self):
    self.set_tab(self.perks_label)
    self.open_tab(CharacterPerks(self.player_name))

  def open_items(self):
    self.set_tab(self.items_label)
    self.open_tab(CharacterItems(self.player_name))

  def open_cards(self):
    self.set_tab(self.cards_label)
    self.open_tab(CharacterCards(self.player_name))

  def open_details(self):
    self.set_tab(self.details_label)
    self.open_tab(CharacterDetails(self.player_name))

  def tab_click(self, **event_args):
    tab = event_args['sender'].tag
    if self.current_tab['Current'] == tab:
      return
    self.current_tab = self.tabs[tab]
    self.current_tab['OpenForm']()

  def setup_label(self):
    name_label = Label(text=self.player_name, role='title', align='center')
    name_card = ColumnPanel(role='elevated-card', wrap_on='naver', spacing_above='none', spacing_below='none')
    name_card.add_component(name_label)
    self.label_flow_panel.add_component(name_card, width=900)

