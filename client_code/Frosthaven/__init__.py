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

    self.adjust_width()
    self.frosthaven_label.text = 'Frosthaven'
    self.item = app_tables.frosthaven.search()[0]
    self.fill_total_defense()
    self.fill_prosperity_level()

  def adjust_width(self):
    if window.innerWidth < 900:
      column_width = (window.innerWidth / 3) - 10
      data_grid_columns = self.data_grid_1.columns
      for column in data_grid_columns:
        column['width'] = column_width
      self.data_grid_1.columns = data_grid_columns

  def fill_total_defense(self):
    moral = self.moral_text_box.text or 0
    defense = self.bonus_defense_text_box.text or 0
    self.total_defense_text_box.text = Utilites.get_total_defense(
      moral=moral, defense=defense
    )

  def total_defense_change(self, **event_args):
    self.fill_total_defense()

  def fill_prosperity_level(self):
    prosperity = self.prosperity_text_box.text or 0
    self.prosperity_level_text_box.text = Utilites.get_prosperity_level(
      prosperity=prosperity
    )

  def prosperity_level_change(self, **event_args):
    self.fill_prosperity_level()

