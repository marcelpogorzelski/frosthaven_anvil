from ._anvil_designer import CharacterItemsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .SellItem import SellItem
from ... import navigation
from ... import Utilites


class CharacterItems(CharacterItemsTemplate):
  def __init__(self, player_name,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.player_name = player_name
    self.character = app_tables.characters.get(Player=player_name)

    self.player_label.text = player_name
    self.image_border = 'thick solid green'
    self.populate_items()

  def populate_items(self):
    self.sell_value_text_box.text = 0
    self.herbs_back_text_box.text = 0
    self.total_price = 0
    self.total_herbs = 0
    self.character_items_flow_panel.clear()
    for item in self.character['Items']:
      #display_mode = 'shrink_to_fit'
      display_mode = 'original_size'
      if item['Destilled']:
        tag = {'Item': item}
        self.total_herbs += 1
      else: 
        sell_price = self.get_item_sell_price(item)
        self.total_price += sell_price
        tag = {'Item': item, 'Sell_Price': sell_price}
      item_image = Image(source=item['Card'], display_mode=display_mode, tooltip=f"Item {item['Number']}", tag=tag)
      item_image.add_event_handler('mouse_down', self.item_image_click)
      self.character_items_flow_panel.add_component(item_image)

  def get_item_sell_price(self, item):
    if item['HasGoldCost']:
      return int(item['Gold'] / 2)
    sell_price = 0
    for resource_name in Utilites.MATERIAL_AND_HERB_RESOURCES:
      sell_price += item[resource_name]
    item_compnent_count = 0
    if item['Items']:
      item_compnent_count = len(item['Items'])
    sell_price += item_compnent_count
    return sell_price * 2
      
  def item_image_click(self, **event_args):
    item_image = event_args['sender']
    if item_image.border:
      item_image.border = None
      self.sub_item(item_image.tag)
    else:
      item_image.border = self.image_border
      self.add_item(item_image.tag)

  def add_item(self, tag):
    item = tag['Item']
    if item['Destilled']:
      self.herbs_back_text_box.text += 1
    else:
      self.sell_value_text_box.text += tag['Sell_Price']

  def sub_item(self, tag):
    item = tag['Item']
    if item['Destilled']:
      self.herbs_back_text_box.text -= 1
    else:
      self.sell_value_text_box.text -= tag['Sell_Price']

  def set_border_for_all(self, border):
    for item_image in self.character_items_flow_panel.get_components():
      item_image.border = border

  def select_all_button_click(self, **event_args):
    self.set_border_for_all(self.image_border)
    self.sell_value_text_box.text = self.total_price
    self.herbs_back_text_box.text = self.total_herbs

  def clear_button_click(self, **event_args):
    self.set_border_for_all(None)
    self.sell_value_text_box.text = 0
    self.herbs_back_text_box.text = 0

  def get_selected_items(self):
    items = []
    for item_image in self.character_items_flow_panel.get_components():
      items.append(item_image.tag)
    return items

  def sell_button_click(self, **event_args):
    sell_item_list = list()
    for item_image in self.character_items_flow_panel.get_components():
      if not item_image.border:
        continue
      item = item_image.tag['Item']
      sell_item_list.append(item)
    if len(sell_item_list) == 0:
      return
    main_form = get_open_form()
    main_form.change_form(SellItem(self.player_name, sell_item_list, self.sell_value_text_box.text))

  def lose_button_click(self, **event_args):
    remove_item_list = list()
    items_string = 'Are you sure you want to remove following items:\n'
    for item_image in self.character_items_flow_panel.get_components():
      if not item_image.border:
        continue
      item = item_image.tag['Item']
      items_string += "  - " + item['Number'] + ": " + item['Name'] + "\n"
      remove_item_list.append(item)
    if len(remove_item_list) == 0:
      return
    if not confirm(items_string):
      return
    
    for item in remove_item_list:
      Utilites.remove_item(self.character, item)
      
    if self.character['Items']:
      self.populate_items()
    else:
      navigation.go_to_character(self.player_name)
    

