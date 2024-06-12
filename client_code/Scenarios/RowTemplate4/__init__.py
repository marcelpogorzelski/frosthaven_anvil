from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def foregroud_color(self, hex):
    red, green, blue = tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
    print(red, (red/255.0) ** 2))
    #let cieY = Math.pow(sR/255.0,2.2) * 0.2126 +
    #      Math.pow(sG/255.0,2.2) * 0.7152 +
    #      Math.pow(sB/255.0,2.2) * 0.0722; 
    cieY = (((red/255.0) ** 2) *  0.2126 ) + (((green/255.0) ** 2) *  0.7152) + (((blue/255.0) ** 2) *  0.0722)
    if cieY < 0.36:
      return "#ffffff"
    else:
      return "#000000"
