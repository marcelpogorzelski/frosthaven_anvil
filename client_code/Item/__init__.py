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
    
    self.frosthaven = app_tables.frosthaven.search()[0]
    
    self.craftable = True
    self.player = None

    self.setup()
    
  def setup(self):
    self.reset()
    
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
    self.sufficiant = True
    self.buy_button.visible = True
    self.check_if_sufficiant_founds()
    if self.sufficiant:
      pass
    else:
      return
      alert("Not enough gold")

  def check_price(self, text_box, price):
    if text_box.text > price:
      self.sufficiant = False
      text_box.background = 'theme:Primary'
      
  def check_if_sufficiant_founds(self):
    self.check_price(self.gold_text_box, self.player['Gold'])
    self.check_price(self.lumber_text_box, self.player['Lumber'])
    self.check_price(self.metal_text_box, self.player['Metal'])
    self.check_price(self.hide_text_box, self.player['Hide'])
    
  def add_item_to_price(self, price_item):
    self.set_price(price_item['Gold'], self.gold_text_box)
    self.set_price(price_item['Lumber'], self.lumber_text_box)
    self.set_price(price_item['Metal'], self.metal_text_box)
    self.set_price(price_item['Hide'], self.hide_text_box)
    self.set_price(price_item['Arrowvine'], self.arrowvine_text_box)
    self.set_price(price_item['Axenut'], self.axenut_text_box)
    self.set_price(price_item['Corpsecap'], self.corpsecap_text_box)
    self.set_price(price_item['Flamefruit'], self.flamefruit_text_box)
    self.set_price(price_item['Rockroot'], self.rockroot_text_box)
    self.set_price(price_item['Snowthistle'], self.snwothistle_text_box)
    if price_item['1Herb']:
      self.one_herb = price_item['1Herb']
    if price_item['2Herbs']:
      self.two_herbs = price_item['2Herbs']
    
  def set_price(self, price, text_box):
    if price > 0:
      text_box.text += price

  def parse_item_price(self, item):
    cost_items = app_tables.items.search(Number=q.any_of(*item['Items'].split(',')))
    for cost_item in cost_items:
      print(cost_item)

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
    if self.one_herb:
      self.any_1_label.visible = True
      self.any_1_drop_down.visible = True
    if self.two_herbs:
      self.any_2_label.visible = True
      self.any_2_drop_down.visible = True

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
    self.any_1_label.visible = False
    self.any_2_label.visible = False
    self.any_1_drop_down.visible = False
    self.any_2_drop_down.visible = False
    self.buy_button.visible = False

  def reset_border(self):
    self.gold_text_box.background = ''
    self.lumber_text_box.background = ''
    self.metal_text_box.background = ''
    self.hide_text_box.background = ''
    self.arrowvine_text_box.background = ''
    self.axenut_text_box.background = ''
    self.corpsecap_text_box.background = ''
    self.flamefruit_text_box.background = ''
    self.rockroot_text_box.background = ''
    self.snwothistle_text_box.background = ''

  def reset_prices(self):
    self.prices = {
      'Gold' : (0, self.gold_text_box,self.gold_image),
      'Lumber' : (0, self.lumber_text_box, self.lumber_image),
      'Metal' : (0, self.metal_text_box, self.metal_image),
      'Hide' : (0, self.hide_text_box, self.hide_image),
      'Arrowvine' : (0, self.arrowvine_text_box, self.arrowvine_image),
      'Axenut' : (0, self.axenut_text_box, self.axenut_image),
      'Corpsecap' : (0, self.corpsecap_text_box, self.corpsecap_image),
      'Flamefruit' : (0, self.flamefruit_text_box, self.flamefruit_image),
      'Rockroot' : (0, self.rockroot_text_box, self.rockroot_image),
      'Snowthistle' : (0, self.snwothistle_text_box, self.snowthistle_image),
    }    

  def reset(self):
    #self.set_not_visible()
    self.reset_prices()
    for price in self.prices:
      price[2].visible = False
      price[1].visible = False
      price[1].text = price[0]
      price[1].border = ''
    
    self.item_cost_image_1.source = None
    self.item_cost_image_2.source = None
    self.item_cost_image_3.source = None
    self.one_herb = False
    self.two_herbs = False
    self.any_1_drop_down.selected_value = ''
    self.any_2_drop_down.selected_value = ''

  def character_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.reset()
    self.player = event_args['sender'].selected_value
    self.setup()
        
    
