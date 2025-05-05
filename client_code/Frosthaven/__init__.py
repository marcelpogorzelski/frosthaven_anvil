from ._anvil_designer import FrosthavenTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites
from anvil.js.window import window


class Frosthaven(FrosthavenTemplate):
  def __init__(self, **properties):
    self.item = app_tables.frosthaven.search()[0]
    
    self.init_components(**properties)
  
    self.adjust_width()


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
    name_data_grid_columns[0]['width'] = column_width * 3
    #name_data_grid_columns[1]['width'] = column_width

    self.name_data_grid.columns = name_data_grid_columns
    
  def set_walls_drop_down(self):
    prosperity_level = self.item['ProsperityLevel']
    walls = 1
    if prosperity_level == 2:
      walls = 2
    elif prosperity_level == 3:
      walls = 3
    elif prosperity_level >= 6:
      walls = 5
    elif prosperity_level >= 4:
      walls = 4

    offset = ''
    if window.innerWidth >= 900:
      offset = '‎ ' * 20
    return [(f'{offset}{wall_number}{offset}', wall_number) for wall_number in range(0, walls+1)]


  def prosperity_level_change(self, **event_args):
    Utilites.bounded_text_box(self.prosperity_text_box, 0, 132)
    Utilites.set_prosperity(self.item, self.prosperity_text_box.text or 0)
    self.refresh_data_bindings()

  def moral_text_box_change(self, **event_args):
    Utilites.bounded_text_box(self.moral_text_box, 0, 20)
    Utilites.set_moral(self.item, self.moral_text_box.text or 0)
    self.refresh_data_bindings()

  def walls_drop_down_change(self, **event_args):
    Utilites.set_walls(self.item, int(self.walls_drop_down.selected_value))
    self.refresh_data_bindings()

  def guards_text_box_change(self, **event_args):
    Utilites.bounded_text_box(self.guards_text_box, 0, 10)
    self.item['Guards'] = self.guards_text_box.text or 0

  def text_box_change(self, **event_args):
    text_box = event_args['sender']
    Utilites.bounded_text_box(text_box, 0, 10000)
    self.item[text_box.tag] = text_box.text or 0
    

