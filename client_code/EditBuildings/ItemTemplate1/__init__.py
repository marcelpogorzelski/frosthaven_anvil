from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.building_number_drop_down.items = [str(i) for i in range(self.item['Count'] + 1)]
    self.building_number_drop_down.selected_value = str(self.item['Level'])
    self.name_text_box.text = self.item['Name']

    # Any code you write here will run before the form opens.
