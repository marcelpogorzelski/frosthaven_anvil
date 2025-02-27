from ._anvil_designer import CardsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator
import json

class Cards(CardsTemplate):
  def __init__(self, player_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.character = app_tables.characters.get(Player=player_name)

    self.display_mode = 'original_size'
    if navigator.userAgentData.mobile:
      self.display_mode = 'shrink_to_fit'
    
    self.character_label.text = player_name

    #https://github.com/cmlenius/gloomhaven-card-browser/blob/main/data/character-ability-cards.ts
    cards_json = URLMedia("https://raw.githubusercontent.com/any2cards/frosthaven/refs/heads/master/data/character-ability-cards.js")
    all_cards = json.loads(cards_json.get_bytes())

    class_name = self.character['Class']['xws']
    cards_path = list(filter(lambda card: card['character-xws'] == class_name and card['cardno'] != '-', all_cards))[0]['image'][:37]
    cards_url = f'https://api.github.com/repos/any2cards/frosthaven/contents/images/{cards_path}'
    card_media = URLMedia(cards_url)
    card_paths =  json.loads(card_media.get_bytes())
    for card_path in card_paths:
      self.add_card_image(card_path['path'])

  def add_card_image(self, card_path):
    card_url = f"https://github.com/any2cards/frosthaven/blob/master/{card_path}?raw=true"
    card_media = URLMedia(card_url)
    card_image = Image(source=card_media, display_mode=self.display_mode)
    self.cards_flow_panel.add_component(card_image)
