from ._anvil_designer import ItemsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import window
from .Item import Item
from .SellItem import SellItem

class Items(ItemsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.orange = ' #FFA500'
    self.display_mode = 'fill_width'
    self.image_width = 300
    if window.innerWidth < 600:
      self.image_width = 100
    
    self.head_image.tag = 'Head'
    self.body_image.tag = 'Body'
    self.feet_image.tag = 'Feet'
    self.one_hand_image.tag = 'One Hand'
    self.two_hands_image.tag = 'Two Hands'
    self.small_image.tag = 'Small'
    self.type_filters = (
      self.head_image,
      self.body_image,
      self.feet_image,
      self.one_hand_image,
      self.two_hands_image,
      self.small_image
    )
    
    self.persistant_image.tag = 'Passive'
    self.spent_image.tag = 'Spent'
    self.lost_image.tag = 'Lost'
    self.flip_image.tag = 'Flip'
    self.usage_filters = (
      self.persistant_image,
      self.spent_image,
      self.lost_image,
      self.flip_image
    )

    self.all_images = list()
    self.load_items()
    self.resize_items()

  def load_image(self, item):
    item_image = Image(source=item['Card'], display_mode=self.display_mode, tooltip=f"Item {item['Number']}", tag=item)
    item_image.add_event_handler('mouse_down', self.process_item)
    self.items_flow_panel.add_component(item_image, width=self.image_width)
    self.all_images.append(item_image)

  def load_items(self):
    for item in app_tables.items.search(Available=True):
      self.load_image(item)
    self.items_flow_panel.visible = True

  def resize_items(self):
    self.items_flow_panel.visible = False
    self.items_flow_panel.clear()
    for image in self.all_images:
      self.items_flow_panel.add_component(image, width=self.image_width)
    self.items_flow_panel.visible = True

  def filter_item(self, item):
    if item['Type'] not in self.current_type_filters:
      return False
    if item['Usage'] not in self.current_usage_filters:
      return False
    if self.in_store_link.background:
      if item['AvailableCount'] == 0:
        return False
    if self.gold_image.background:
      if not item['HasGoldCost']:
        return False
    if self.current_items:
      if item['Number'] not in self.current_items:
        return False
    return True

  def parse_filter_image(self, filter_image_list):
    return_list = list()
    for filter_image in filter_image_list:
      if not filter_image.background:
        continue
      return_list.append(filter_image.tag)
    if return_list:
      return return_list
    return None
    
  def update_visible_images(self):
    self.items_flow_panel.visible = False
    self.current_type_filters = self.parse_filter_image(self.type_filters) or ['Head', 'Body', 'Feet', 'One Hand', 'Two Hands', 'Small']
    self.current_usage_filters = self.parse_filter_image(self.usage_filters) or ['Passive', 'Spent', 'Lost', 'Flip']
    if self.item_number_text_box.text:
      self.current_items = list(self.item_number_text_box.text.split(","))
    else:
      self.current_items = None
    for image in self.all_images:
      if self.filter_item(image.tag):
        image.visible = True
      else:
        image.visible = False
    self.items_flow_panel.visible = True

  def process_item(self, **event_args):
    item = event_args['sender']-
    get_open_form().change_form(Item(item.tag))
    #get_open_form().change_form(SellItem(item.tag))


  def filter_mouse_down(self, x, y, button, keys, **event_args):
    if event_args['sender'].background:
      event_args['sender'].background = None
    else:
      event_args['sender'].background = self.orange

    self.update_visible_images()

  def item_number_text_box_pressed_enter(self, **event_args):
    self.update_visible_images()

  def in_store_link_click(self, **event_args):
    if event_args['sender'].background:
      event_args['sender'].background = None
    else:
      event_args['sender'].background = self.orange

    self.update_visible_images()

  def decrease_items_click(self, **event_args):
    if self.image_width <= 100:
      self.image_width -= 25
    else:
      self.image_width -= 50
    self.resize_items()

  def increase_items_click(self, **event_args):
    if self.image_width < 100:
      self.image_width += 25
    else:
      self.image_width += 50
    self.resize_items()

    
