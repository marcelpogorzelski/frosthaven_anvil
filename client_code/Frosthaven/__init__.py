from ._anvil_designer import FrosthavenTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites


class Frosthaven(FrosthavenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = app_tables.frosthaven.search()[0]
  
    self.total_defense_text_box.text = Utilites.get_total_defense(moral=self.item['Moral'], defense=self.item['Defense'])

  def text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.total_defense_text_box.text = Utilites.get_total_defense(moral=self.moral_text_box.text, defense=self.bonus_defense_text_box.text)

