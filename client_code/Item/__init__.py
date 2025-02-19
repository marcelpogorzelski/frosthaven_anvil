from ._anvil_designer import ItemTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CharacterItems import CharacterItems


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
    self.player = self.character_drop_down.selected_value
    if self.player:
      if self.item[self.player['Player']]:
        self.price_label.text = 'You already own the item!'
        self.free_check_box.visible = False
        return

    if self.item['AvailableCount'] == 0:
      self.price_label.text = f"No more copies of item: {self.item['Number']} - {self.item['Name']}"
      self.free_check_box.visible = False
      self.character_drop_down.visible = False
      self.character_label.visible = False
      return

    if self.free_check_box.checked:
      self.buy_button.text = 'Add item'
      self.buy_button.enabled = True
      self.buy_button.visible = True
      self.price_label.text = 'Add item for free'
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
      self.available_resources[resource] = {'Player': player_resource_count, 'Sum': -1}
      
    for resource in self.combined_resources:
      player_resource_count = self.player[resource]
      frosthaven_resource_count = self.frosthaven[resource]
      sum_resource_count = player_resource_count + frosthaven_resource_count
      self.available_resources[resource] = {'Player': player_resource_count, 'Sum': sum_resource_count}

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
        self.uncraftable(cost_item)
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

  def show_resource(self, resource_name):
    resource = self.prices[resource_name]
    if resource['Price'] == 0:
      return

    if not self.player:
      resource['TextBox'].text = resource['Price']
      resource['Image'].visible = True
      resource['TextBox'].visible = True
      return

    price = resource['Price']
    available_player = self.available_resources[resource_name]['Player']
    available_total = self.available_resources[resource_name]['Sum']

    if available_player >= price:
      resource['TextBox'].text = price
      self.payment[resource_name] = {'Player': price}
    elif available_total >= price:
      remainder = price - available_player
      resource['TextBox'].type = 'text'
      resource['TextBox'].text = f'{price} ({remainder} taken from Frosthaven)'
      resource['TextBox'].background = 'theme:Tertiary Container'
      if available_player > 0:
        self.payment[resource_name] = {'Player': available_player, 'Frosthaven': remainder}
      else:
        self.payment[resource_name] = {'Frosthaven': remainder}
    else:
      self.insufficient_funds = True
      resource['TextBox'].type = 'text'
      if available_total == -1:
        available_total = available_player
      if available_total == 0:
        resource['TextBox'].text = f'{price} (No {resource_name.lower()} available)'
      else:
        resource['TextBox'].text = f'{price} ({available_total} {resource_name.lower()} available)'
      resource['TextBox'].background = 'theme:Primary Container'

    resource['Image'].visible = True
    resource['TextBox'].visible = True


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

    if not self.player:
      return
    
    if self.insufficient_funds:
      self.buy_button.text = 'Insufficient resources'
    else:
      self.buy_button.enabled = True
    self.buy_button.visible = True


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
      price['TextBox'].type = 'number'
      price['TextBox'].background = ''

    self.payment = dict()

    self.one_herb = False
    self.two_herbs = False
    self.any_1_drop_down.selected_value = ''
    self.any_2_drop_down.selected_value = ''
    self.any_1_label.visible = False
    self.any_2_label.visible = False
    self.any_1_drop_down.visible = False
    self.any_2_drop_down.visible = False

    self.insufficient_funds = False
    self.buy_button.text = 'Buy'
    self.buy_button.visible = False
    self.buy_button.enabled = False

    self.price_label.text = 'Price'

    self.available_resources = dict()

    self.items_as_price = list()
    self.items_as_price_flow_panel.clear()

    self.free_check_box.visible = True

  def character_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.setup()

  def buy_button_click(self, **event_args):
    if self.free_check_box.checked:
      if not self.player:
        alert("Choose a player in the drop down menu")
        return
      if not confirm(f"Do you want to add item:\n   {self.item['Number']} - {self.item['Name']}"):
        return
      self.item[self.player['Player']] = True
      self.item['AvailableCount'] -= 1
      self.go_to_character_items(self.player['Player'])
      return
    player_name = self.player['Player']
    player_payment_string = player_name + ':\n'
    frosthaven_payment_string = '\nFrosthaven:\n'
    
    for resource_name, values in self.payment.items():
      if 'Player' in values:
        player_price = values['Player']
        player_payment_string += "  - " + str(resource_name) + ": " + str(player_price) + "\n"
      if 'Frosthaven' in values:
        frosthaven_price = values['Frosthaven']
        frosthaven_payment_string += "  - " + str(resource_name) + ": " + str(frosthaven_price)  + "\n"

    items_string = '\nItems:\n'

    for item in self.items_as_price:
      items_string += "  - " + item['Number'] + ": " + item['Name'] + "\n"
    if not confirm((player_payment_string + frosthaven_payment_string + items_string)):
      return

    for resource_name, values in self.payment.items():
      if 'Player' in values:
        self.player[resource_name] -= values['Player']
      if 'Frosthaven' in values:
        self.frosthaven[resource_name] -= values['Frosthaven']
    self.player.update()
    self.frosthaven.update()
    for item in self.items_as_price:
      item[self.player['Player']] = False
      item['AvailableCount'] += 1
      item.update()
    self.item[self.player['Player']] = True
    self.item['AvailableCount'] -= 1
    self.go_to_character_items(self.player['Player'])

  def free_check_box_change(self, **event_args):
    self.setup()

  def go_to_character_items(self, character_name):
    main_form = get_open_form()
    if character_name == 'Håvard':
      main_form.havard_items_click(sender = main_form.havard_items_link)
      return
      
    if character_name == 'Marcel':
      main_form.marcel_items_click(sender = main_form.marcel_items_link)
      return
      
    if character_name == 'Kristian':
      main_form.kristian_items_click(sender = main_form.kristian_items_link)
      return
      
    if character_name == 'John Magne':
      main_form.john_magne_items_click(sender = main_form.john_magne_items_link)
      return
      
    
        
      
        
    
