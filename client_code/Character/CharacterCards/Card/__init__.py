from ._anvil_designer import CardTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Card(CardTemplate):
  def __init__(self, card, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.add_card_image(card['image'])


  def add_card_image(self, card_path):
    card_url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{card_path}"
    card_media = URLMedia(card_url)
    self.card_image.source = card_media
    #card_image = Image(source=card_media, display_mode=self.display_mode)
    #self.cards_flow_panel.add_component(card_image)

    # Any code you write here will run before the form opens.
