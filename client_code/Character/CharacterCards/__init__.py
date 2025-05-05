from ._anvil_designer import CharacterCardsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator
import json
from ... import Frosthaven_info

class CharacterCards(CharacterCardsTemplate):
  def __init__(self, player_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.character = app_tables.characters.get(Player=player_name)

    self.display_mode = 'original_size'
    if navigator.userAgentData.mobile:
      self.display_mode = 'shrink_to_fit'
    
    self.character_label.text = player_name

    class_id = self.character['Class']['Id']
    
    class_cards_info = sorted(Frosthaven_info.class_cards_info[class_id], key=lambda card: card['level'] )
    for class_card_info in class_cards_info:
      self.add_card_image(class_card_info['image'])

  def add_card_image(self, card_path):
    card_url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{card_path}"
    card_media = URLMedia(card_url)
    card_image = Image(source=card_media, display_mode=self.display_mode)
    self.cards_flow_panel.add_component(card_image)
