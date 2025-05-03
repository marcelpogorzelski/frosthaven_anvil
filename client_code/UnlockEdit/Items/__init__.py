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
    prev = {'item': None}
    drop_down_items = list()
    self.items = dict()
    
    for item in app_tables.items.search():
      drop_down_items.append(item['Number'])

      self.items[item['Number']] = {'item': item, 'prev': prev['item'], 'next': None}
      if prev:
        prev['next'] = item
      prev = self.items[item['Number']]
      
    self.item_drop_down.items = drop_down_items
    
    
    self.change_item()

  def change_item(self):
    self.item = self.items[self.item_drop_down.selected_value]['item']
    self.refresh_data_bindings()

  def available_check_box_change(self, **event_args):
    self.item['Available'] = self.available_check_box.checked
    self.refresh_data_bindings()

  def item_drop_down_change(self, **event_args):
    self.change_item()

  def next_button_click(self, **event_args):
    next = self.items[self.item['Number']]['next']
    if not next:
      return
    #self.item = next
    self.item_drop_down.selected_value = next['Number']
    self.change_item()

  def prev_button_click(self, **event_args):
    prev = self.items[self.item['Number']]['prev']
    if not prev:
      return
    self.item_drop_down.selected_value = prev['Number']
    self.change_item()
