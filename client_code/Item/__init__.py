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

    self.solo_resources = ['Gold', 'Lumber', 'Metal', 'Hide']
    self.combined_resources = ['Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle']
    
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
    if self.player:
      if self.item[self.player['Player']]:
        self.price_label.text = 'You already own the item!'
        return
    self.parse_item_price(self.item)
    if self.player:
      self.get_available_founds()
    
    if self.craftable:
      self.process_crafting()
    else:
      self.character_drop_down.visible = False
      self.character_label.visible = False

  def get_available_founds(self):
    for resource in self.solo_resources:
      player_resource_count = self.player[resource]
      self.available_resources[resource] = {'Player': player_resource_count, 'Frosthaven': None, 'Sum': None}
      
    for resource in self.combined_resources:
      player_resource_count = self.player[resource]
      frosthaven_resource_count = self.frosthaven[resource]
      sum_resource_count = player_resource_count + frosthaven_resource_count
      self.available_resources[resource] = {'Player': player_resource_count, 'Frosthaven': frosthaven_resource_count, 'Sum': sum_resource_count}

  def process_crafting(self):
    self.set_visible()
    if not self.player:
      return

  def parse_item_price(self, item):
    if self.player:
      if item[self.player['Player']]:
        self.items_as_price.append(item)
        return
    for resource, price in self.prices.items():
      if item[resource] > 0:
        price['Price'] += item[resource]
    if item['1Herb']:
      self.one_herb = True
    if item['2Herbs']:
      self.two_herbs = True
    cost_items = app_tables.items.search(Number=q.any_of(*item['Items'].split(',')))
    for cost_item in cost_items:
      if not cost_item['Available']:
        self.uncraftable(item)
        return
      if self.player:
        self.parse_item_price(cost_item)
      else:
        self.items_as_price.append(cost_item)

  def uncraftable(self, item):
    self.craftable = False
    item_number = item['Number']
    if self.price_label.text == 'Price':
      self.price_label.text = f'Cannot craft item. Missing item(s): {item_number}'
    else:
      self.price_label.text += f', {item_number}'

  def set_image_visible_if_source(self, image):
    if image.source:
      image.visible = True

  def show_resource(self, resource):
    price = self.prices[resource]
    if price['Price'] == 0:
      return
      
    price['TextBox'].text = price['Price']
    price['Image'].visible = True
    price['TextBox'].visible = True
    
    if not self.player:
      return
      
    available_count = self.available_resources[resource]
    if available_count['Player'] >= price['Price']:
      return
    
    price['TextBox'].background = 'theme:Primary Container'
    if available_count['Frosthaven'] is None:
      return
    print(f"{resource}: {available_count['Sum']}")
    #print(f"{resource}: {available_count['Sum']}")
    if available_count['Sum'] >= price['Price']:
      return
    #print("adfga")
    price['TextBox'].background = 'theme:Primary'


  def set_visible(self):
    for resource in self.prices.keys():
      self.show_resource(resource)

    for item in self.items_as_price:
      self.items_as_price_flow_panel.add_component(Image(source=item['Card']))
      
    if self.one_herb:
      self.any_1_label.visible = True
      self.any_1_drop_down.visible = True
    if self.two_herbs:
      self.any_2_label.visible = True
      self.any_2_drop_down.visible = True


  def reset_prices(self):
    self.prices = {
      'Gold' : {'Price': 0, 'TextBox': self.gold_text_box, 'Image': self.gold_image},
      'Lumber' : {'Price': 0, 'TextBox': self.lumber_text_box, 'Image': self.lumber_image},
      'Metal' : {'Price': 0, 'TextBox': self.metal_text_box, 'Image': self.metal_image},
      'Hide' : {'Price': 0, 'TextBox': self.hide_text_box, 'Image': self.hide_image},
      'Arrowvine' : {'Price': 0, 'TextBox': self.arrowvine_text_box, 'Image': self.arrowvine_image},
      'Axenut' : {'Price': 0, 'TextBox': self.axenut_text_box, 'Image': self.axenut_image},
      'Corpsecap' : {'Price': 0, 'TextBox': self.corpsecap_text_box, 'Image': self.corpsecap_image},
      'Flamefruit' : {'Price': 0, 'TextBox': self.flamefruit_text_box, 'Image': self.flamefruit_image},
      'Rockroot' : {'Price': 0, 'TextBox': self.rockroot_text_box, 'Image': self.rockroot_image},
      'Snowthistle' : {'Price': 0, 'TextBox': self.snowthistle_text_box, 'Image': self.snowthistle_image},
    }    

  def reset(self):
    self.reset_prices()
    for price in self.prices.values():
      price['Image'].visible = False
      price['TextBox'].visible = False
      price['TextBox'].text = 0
      price['TextBox'].background = ''

    self.one_herb = False
    self.two_herbs = False
    self.any_1_drop_down.selected_value = ''
    self.any_2_drop_down.selected_value = ''
    self.any_1_label.visible = False
    self.any_2_label.visible = False
    self.any_1_drop_down.visible = False
    self.any_2_drop_down.visible = False
    
    self.buy_button.visible = False

    self.price_label.text = 'Price'

    self.available_resources = dict()

    self.items_as_price = list()
    self.items_as_price_flow_panel.clear()

  def character_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.player = event_args['sender'].selected_value
    self.setup()
        
    
