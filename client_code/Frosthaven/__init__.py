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
    self.item = app_tables.frosthaven.search()[0]
    self.fill_total_defense()


  def adjust_width(self):
    if window.innerWidth >= 900:
      return
      
    column_width = (window.innerWidth / 3) - 10
    
    data_grid_columns = self.data_grid_1.columns
    for column in data_grid_columns:
      column['width'] = column_width
    self.data_grid_1.columns = data_grid_columns

    label_data_grid_columns = self.label_data_grid.columns
    label_data_grid_columns[0]['width'] = window.innerWidth - 30
    self.label_data_grid.columns = label_data_grid_columns

    name_data_grid_columns = self.name_data_grid.columns
    print(window.innerWidth)
    name_data_grid_columns[0]['width'] = column_width * 2
    name_data_grid_columns[1]['width'] = column_width

    self.name_data_grid.columns = name_data_grid_columns

  def fill_total_defense(self):
    moral = self.moral_text_box.text or 0
    defense = self.bonus_defense_text_box.text or 0
    self.total_defense_text_box.text = Utilites.get_total_defense(
      moral=moral, defense=defense
    )

  def total_defense_change(self, **event_args):
    self.fill_total_defense()


  def prosperity_level_change(self, **event_args):
    Utilites.bounded_text_box(self.prosperity_text_box, 0, 132)
    Utilites.set_prosperity(self.item, self.prosperity_text_box.text or 0)

