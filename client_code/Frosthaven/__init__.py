from ._anvil_designer import FrosthavenTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
from anvil.js.window import window


class Frosthaven(FrosthavenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = app_tables.frosthaven.search()[0]
    if window.innerWidth < 900:
      column_width = (window.innerWidth / 3) - 10
      data_grid_columns = self.data_grid_1.columns
      for column in data_grid_columns:
        column['width'] = column_width
      self.data_grid_1.columns = data_grid_columns
    self.total_defense_text_box.text = Utilites.get_total_defense(
      moral=self.item["Moral"], defense=self.item["Defense"]
    )

  def text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.total_defense_text_box.text = Utilites.get_total_defense(
      moral=self.moral_text_box.text, defense=self.bonus_defense_text_box.text
    )
