from ._anvil_designer import ItemsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Items(ItemsTemplate):
  def __init__(self, **properties):
    self.icon_image_height = 50
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    # Any code you write here will run before the form opens.
    self.current_item = self.number_text_box.text
    self.change_item()

  def change_item(self):
    next_item = app_tables.items.search(Number=self.number_text_box.text)
    if len(next_item) == 0:
      alert(
        f"{self.number_text_box.text} is not an item! Returning to item {self.current_item}"
      )
      self.number_text_box.text = self.current_item
      return
    self.item = next_item[0]
      
    self.current_item = self.number_text_box.text
    print(self.current_item)
    self.refresh_data_bindings()

  def number_text_box_pressed_enter(self, **event_args):
    self.change_item()

  def available_check_box_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.item['Available'] = self.available_check_box.checked
    self.refresh_data_bindings()
