from ._anvil_designer import ItemsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


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
    self.get_filter_items()
    self.populate_items()


  def populate_items(self):
    self.item_list = self.get_available_items()

    self.items_flow_panel.clear()
    for item in self.item_list:
      display_mode = 'shrink_to_fit'
      #display_mode = 'original_size'
      item_image = Image(source=item['Card'], display_mode=display_mode)
      self.items_flow_panel.add_component(item_image)

  def parse_filter_image(self, filter_image_list):
    return_list = list()
    for filter_image in filter_image_list:
      if not filter_image.background:
        continue
      return_list.append(filter_image.tag)
    return return_list
      
  def get_filter_items(self):
    self.type_selected_list = self.parse_filter_image(self.type_filters) or ['Head', 'Body', 'Feet', 'One Hand', 'Two Hands', 'Small']
    self.usage_selected_list = self.parse_filter_image(self.usage_filters) or ['Passive', 'Spent', 'Lost', 'Flip']
    if self.gold_image.background:
      self.gold_selected = True
    else:
      self.gold_selected = False
    
  def get_available_items(self):
    if self.gold_selected:
      return app_tables.items.search(Available=True, Type=q.any_of(*self.type_selected_list), Usage=q.any_of(*self.usage_selected_list), Gold=True)
    return app_tables.items.search(Available=True, Type=q.any_of(*self.type_selected_list), Usage=q.any_of(*self.usage_selected_list))
    

  def filter_mouse_down(self, x, y, button, keys, **event_args):
    """This method is called when a mouse button is pressed on this component"""
    if event_args['sender'].background:
      event_args['sender'].background = None
    else:
      event_args['sender'].background = self.orange
    self.get_filter_items()
    self.populate_items()
