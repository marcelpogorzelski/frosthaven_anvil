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
    self.card_image.source = card['Image']
