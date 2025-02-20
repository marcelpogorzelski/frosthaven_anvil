from ._anvil_designer import ItemsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Item import Item


class Items(ItemsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.orange = ' #FFA500'
    
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
    self.selected_item_numbers = q.none_of("a")
    self.get_filter_items()
    self.populate_items()


  def populate_items(self):
    self.items_flow_panel.visible = False
    self.item_list = self.get_available_items()
    
    self.items_flow_panel.clear()
    for item in self.item_list:
      #display_mode = 'shrink_to_fit'
      display_mode = 'original_size'
      item_image = Image(source=item['Card'], display_mode=display_mode, tooltip=f"Item {item['Number']}", tag=item)
      item_image.add_event_handler('mouse_down', self.process_item)
      self.items_flow_panel.add_component(item_image)
    self.items_flow_panel.visible = True

  def process_item(self, **event_args):
    item = event_args['sender']
    get_open_form().change_form(Item(item.tag))

  
  def parse_filter_image(self, filter_image_list):
    return_list = list()
    for filter_image in filter_image_list:
      if not filter_image.background:
        continue
      return_list.append(filter_image.tag)
    if return_list:
      return q.any_of(*return_list)
    return None

  def parse_item_numbers(self):
    if not self.item_number_text_box.text:
      self.item_number_selected_list = q.none_of("a")
      return
    parsed_items = list(self.item_number_text_box.text.split(","))
    self.item_number_selected_list = q.any_of(*parsed_items)
    
    
  def get_filter_items(self):
    self.type_selected_list = self.parse_filter_image(self.type_filters) or q.any_of('Head', 'Body', 'Feet', 'One Hand', 'Two Hands', 'Small')
    self.usage_selected_list = self.parse_filter_image(self.usage_filters) or q.any_of('Passive', 'Spent', 'Lost', 'Flip')
    self.parse_item_numbers()
    if self.all_link.background:
      self.available_selected = q.greater_than(-1)
    else:
      self.available_selected = q.greater_than(0)
    if self.gold_image.background:
      self.gold_selected_list = q.any_of(True)
    else:
      self.gold_selected_list = q.any_of(True, False)

    
  def get_available_items(self):
    return app_tables.items.search(Available=True, Type=self.type_selected_list, Usage=self.usage_selected_list, HasGoldCost=self.gold_selected_list, Number=self.item_number_selected_list, AvailableCount=self.available_selected)

    
  def filter_mouse_down(self, x, y, button, keys, **event_args):
    if event_args['sender'].background:
      event_args['sender'].background = None
    else:
      event_args['sender'].background = self.orange
    self.get_filter_items()
    self.populate_items()

  def item_number_text_box_pressed_enter(self, **event_args):
    self.get_filter_items()
    self.populate_items()

  def all_link_click(self, **event_args):
    if event_args['sender'].background:
      event_args['sender'].background = None
    else:
      event_args['sender'].background = self.orange
    self.get_filter_items()
    self.populate_items()

    
