from ._anvil_designer import ItemTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Item(ItemTemplate):
  def __init__(self, item,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item_image.source = item['Card']
    self.item = item
    character_list = []
    character_list.append(('None', None))
    for character in app_tables.characters.search():
      character_list.append((str(character['Player']), character))
    self.character_drop_down.items = character_list
    self.craftable = True
    self.player = None
    self.frosthaven = app_tables.frosthaven.search()[0]

    self.setup()
    
  def setup(self):
    self.add_item_to_price(self.item)
    self.set_cost_items()
    if self.craftable:
      self.process_crafting()
    else:
      self.character_drop_down.visible = False
      self.character_label.visible = False
      self.reset()

  def process_crafting(self):
    self.set_visible()
    if not self.player:
      return

  def get_available_resources(self):
    pass

  def add_item_to_price(self, price_item):
    self.set_price(price_item['Gold'], self.gold_image, self.gold_text_box)
    self.set_price(price_item['Lumber'], self.lumber_image, self.lumber_text_box)
    self.set_price(price_item['Metal'], self.metal_image, self.metal_text_box)
    self.set_price(price_item['Hide'], self.hide_image, self.hide_text_box)
    self.set_price(price_item['Arrowvine'], self.arrowvine_image, self.arrowvine_text_box)
    self.set_price(price_item['Axenut'], self.axenut_image, self.axenut_text_box)
    self.set_price(price_item['Corpsecap'], self.corpsecap_image, self.corpsecap_text_box)
    self.set_price(price_item['Flamefruit'], self.flamefruit_image, self.flamefruit_text_box)
    self.set_price(price_item['Rockroot'], self.rockroot_image, self.rockroot_text_box)
    self.set_price(price_item['Snowthistle'], self.snowthistle_image, self.snwothistle_text_box)

  def set_price(self, price, image, text_box):
    if price > 0:
      text_box.text += price

  def set_cost_items(self):
    if not self.item['Items']:
      return
    self.cost_items = list()
    image_list = [self.item_cost_image_3,self.item_cost_image_2, self.item_cost_image_1]
    for cost_item in self.item['Items'].split(','):
      cost_item = app_tables.items.get(Number=cost_item)
      if not cost_item['Available']:
        self.uncraftable(cost_item)
        continue
      player_has_item = True
      if self.player:
        print(self.player)
        player_has_item = cost_item[self.player['Player']]
      if player_has_item:
        self.cost_items.append(cost_item)
        cost_image = image_list.pop()
        cost_image.source = cost_item['Card']
      else:
        self.add_item_to_price(cost_item)


  def uncraftable(self, item):
    item_number = item['Number']
    if self.price_label.text == 'Price':
      self.price_label.text = f'Cannot craft item. Missing item: {item_number}'
      self.craftable = False
    else:
      self.price_label.text += f', {item_number}'

  def set_visible_if_cost_value(self, image, text_box):
    if text_box.text > 0:
      image.visible = True
      text_box.visible = True

  def set_image_visible_if_source(self, image):
    if image.source:
      image.visible = True

  def set_visible(self):
    self.set_visible_if_cost_value(self.gold_image, self.gold_text_box)
    self.set_visible_if_cost_value(self.lumber_image, self.lumber_text_box)
    self.set_visible_if_cost_value(self.metal_image, self.metal_text_box)
    self.set_visible_if_cost_value(self.hide_image, self.hide_text_box)
    self.set_visible_if_cost_value(self.arrowvine_image, self.arrowvine_text_box)
    self.set_visible_if_cost_value(self.axenut_image, self.axenut_text_box)
    self.set_visible_if_cost_value(self.corpsecap_image, self.corpsecap_text_box)
    self.set_visible_if_cost_value(self.flamefruit_image, self.flamefruit_text_box)
    self.set_visible_if_cost_value(self.rockroot_image, self.rockroot_text_box)
    self.set_visible_if_cost_value(self.snowthistle_image, self.snwothistle_text_box)
    self.set_image_visible_if_source(self.item_cost_image_1)
    self.set_image_visible_if_source(self.item_cost_image_2)
    self.set_image_visible_if_source(self.item_cost_image_3)

  def set_not_visible(self):
    self.gold_image.visible = False
    self.gold_text_box.visible = False
    self.lumber_image.visible = False
    self.lumber_text_box.visible = False
    self.metal_image.visible = False
    self.metal_text_box.visible = False
    self.hide_image.visible = False
    self.hide_text_box.visible = False
    self.arrowvine_image.visible = False
    self.arrowvine_text_box.visible = False
    self.axenut_image.visible = False
    self.axenut_text_box.visible = False
    self.corpsecap_image.visible = False
    self.corpsecap_text_box.visible = False
    self.flamefruit_image.visible = False
    self.flamefruit_text_box.visible = False
    self.rockroot_image.visible = False
    self.rockroot_text_box.visible = False
    self.snowthistle_image.visible = False
    self.snwothistle_text_box.visible = False
    self.item_cost_image_1.visible = False
    self.item_cost_image_2.visible = False
    self.item_cost_image_3.visible = False

  def reset(self):
    self.set_not_visible()
    self.gold_text_box.text = 0
    self.lumber_text_box.text = 0
    self.metal_text_box.text = 0
    self.hide_text_box.text = 0
    self.arrowvine_text_box.text = 0
    self.axenut_text_box.text = 0
    self.corpsecap_text_box.text = 0
    self.flamefruit_text_box.text = 0
    self.rockroot_text_box.text = 0
    self.snwothistle_text_box.text = 0
    self.item_cost_image_1.source = None
    self.item_cost_image_2.source = None
    self.item_cost_image_3.source = None

  def character_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.reset()
    self.player = event_args['sender'].selected_value
    self.setup()
        
    
