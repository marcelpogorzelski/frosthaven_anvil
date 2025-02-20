from ._anvil_designer import CharacterItemsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math


class CharacterItems(CharacterItemsTemplate):
  def __init__(self, player_name,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.resource_names = ['Lumber', 'Metal', 'Hide', 'Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle']
    
    self.player_name = player_name
    self.player_label.text = player_name
    self.image_border = 'thick solid green'
    self.populate_items()

  def populate_items(self):
    self.item_list = app_tables.items.search(Available=True)

    self.character_items_flow_panel.clear()
    for item in self.item_list:
      if not item[self.player_name]:
        continue
      #display_mode = 'shrink_to_fit'
      display_mode = 'original_size'
      sell_price = self.get_item_sell_price(item)
      tag = {'Item': item, 'Sell_Price': sell_price}
      item_image = Image(source=item['Card'], display_mode=display_mode, tooltip=f"Item {item['Number']}", tag=tag)
      item_image.add_event_handler('mouse_down', self.select_item)
      self.character_items_flow_panel.add_component(item_image)

  def get_item_sell_price(self, item):
    if item['HasGoldCost']:
      return math.floor(item['Gold'] / 2)
    sell_price = 0
    for resource_name in self.resource_names:
      sell_price += item[resource_name]
    sell_price += len(item['Items'].split(',')) - 1
    return sell_price * 2
      
    

  def select_item(self, **event_args):
    item_image = event_args['sender']
    print(item_image.tag['Sell_Price'])
    if item_image.border:
      item_image.border = None
    else:
      item_image.border = self.image_border
