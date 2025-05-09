from ._anvil_designer import CharacterCardsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import window
import json
from ... import Frosthaven_info
from .Card import Card

class CharacterCards(CharacterCardsTemplate):
  def __init__(self, player_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.character = app_tables.characters.get(Player=player_name)
    width = 300
    if window.innerWidth < 600:
      width = 180
    
    self.character_label.text = player_name

    class_id = self.character['Class']['Id']
    
    class_cards_info = sorted(Frosthaven_info.class_cards_info[class_id], key=lambda card: card['level'] )
    for class_card_info in class_cards_info:
      card = Card(class_card_info)
      self.cards_flow_panel.add_component(card, width=width)
