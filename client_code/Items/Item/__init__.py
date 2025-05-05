from ._anvil_designer import ItemTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import navigation
from ... import Utilites

class Item(ItemTemplate):
  def __init__(self, item,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item_image.source = item['Card']
    self.item = item

    self.frosthaven = app_tables.frosthaven.search()[0]

    user = anvil.users.get_user(allow_remembered=True)
    self.player = app_tables.characters.get(Player=user['email'])
    
    character_list = []
    character_list.append(('None', None))
    for character in app_tables.characters.search():
      character_list.append((str(character['Player']), character))
    self.character_drop_down.items = character_list
    self.character_drop_down.selected_value = self.player
    
    self.craftable = True
    self.setup()
    
  def setup(self):
    self.reset()
    self.player = self.character_drop_down.selected_value
    if self.player:
      if self.item in self.player['Items']:
        self.price_label.text = 'You already own the item!'
        self.free_check_box.visible = False
        return

    if self.item['AvailableCount'] == 0:
      self.price_label.text = f"No more copies of item: {self.item['Number']} - {self.item['Name']}"
      self.free_check_box.visible = False
      self.character_drop_down.visible = False
      self.character_label.visible = False
      return

    if self.free_check_box.checked and self.character_drop_down.selected_value:
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
    for resource in Utilites.MATERIAL_AND_GOLD_RESOURCES:
      player_resource_count = self.player[resource]
      self.available_resources[resource] = {'Player': player_resource_count, 'Sum': -1}
      
    for resource in Utilites.HERB_RESOURCES:
      player_resource_count = self.player[resource]
      frosthaven_resource_count = self.frosthaven[resource]
      sum_resource_count = player_resource_count + frosthaven_resource_count
      self.available_resources[resource] = {'Player': player_resource_count, 'Sum': sum_resource_count}

  def process_crafting(self):
    self.set_visible()

  def parse_item_price(self, item):
    if self.player:
      if item in self.player['Items']:
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
      self.payment[resource_name] = {'Player': price, 'Frosthaven': 0}
    elif available_total >= price:
      remainder = price - available_player
      resource['TextBox'].type = 'text'
      resource['TextBox'].text = f'{price} ({remainder} taken from Frosthaven)'
      resource['TextBox'].background = 'theme:Tertiary Container'
      if available_player > 0:
        self.payment[resource_name] = {'Player': available_player, 'Frosthaven': remainder}
      else:
        self.payment[resource_name] = {'Player': 0, 'Frosthaven': remainder}
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

  def show_two_herbs(self):
    if not self.two_herbs:
      return

    if not self.player:
      self.any_2_label.visible = True
      self.any_2_drop_down.visible = True
      return
  
    any_2_drop_down_list = list()
    any_2_drop_down_list.append(('Please select a herb', None))
    for herb_name in Utilites.HERB_RESOURCES:
      price = self.prices[herb_name]['Price']
      available_player = self.available_resources[herb_name]['Player'] - price
      available_total = self.available_resources[herb_name]['Sum'] - price

      if available_player >= 2:
        drop_down_text = herb_name
        drop_down_select = {'Player': 2, 'Frosthaven': 0, 'Herb': herb_name}
        any_2_drop_down_list.append((drop_down_text, drop_down_select))
      elif available_total >= 2:
        frosthaven_portion = 2 - available_player
        drop_down_text = f"{herb_name} ({frosthaven_portion} from Frosthaven)"
        drop_down_select = {'Player': available_player, 'Frosthaven': frosthaven_portion, 'Herb': herb_name}
        any_2_drop_down_list.append((drop_down_text, drop_down_select))

    if len(any_2_drop_down_list) == 1:
      self.insufficient_funds = True
      any_2_drop_down_list = ["Insufficient herbs"]
      self.any_2_drop_down.enabled = False
      
    self.any_2_drop_down.items = any_2_drop_down_list

    self.any_2_label.visible = True
    self.any_2_drop_down.visible = True


  def set_visible(self):
    for resource in self.prices.keys():
      self.show_resource(resource)
    
    self.show_two_herbs()

    for item in self.items_as_price:
      self.items_as_price_flow_panel.add_component(Image(source=item['Card']))

    if self.one_herb:
      self.any_1_label.visible = True
      self.any_1_drop_down.visible = True

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
    self.any_2_drop_down.enabled = True

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
    self.setup()

  def buy_button_click(self, **event_args):
    if self.free_check_box.checked:
      if not self.player:
        alert("Choose a player in the drop down menu")
        return
      if not confirm(f"Do you want to add item:\n   {self.item['Number']} - {self.item['Name']}"):
        return

      Utilites.add_item(self.player, self.item)
      navigation.go_to_character_items(self.player['Player'])
      return

    if self.two_herbs:
      if not self.any_2_drop_down.selected_value:
        alert("Select a herb from 'Any 2' drop down")
        return
      two_herb_name = self.any_2_drop_down.selected_value['Herb']
      two_herb_player = self.any_2_drop_down.selected_value['Player']
      two_herb_frosthaven = self.any_2_drop_down.selected_value['Frosthaven']
      if two_herb_name in self.payment:
        self.payment[two_herb_name]['Player'] += two_herb_player
        self.payment[two_herb_name]['Frosthaven'] += two_herb_frosthaven
      else:
        self.payment[two_herb_name] = {'Player': two_herb_player, 'Frosthaven': two_herb_frosthaven}
    if self.one_herb:
      if not self.any_1_drop_down.selected_value:
        alert("Select a herb from 'Any 1' drop down")
        return
        
    player_display_name = self.player['Player']
    player_payment_string = player_display_name + ':\n'
    frosthaven_payment_string = '\nFrosthaven:\n'
    
    for resource_name, values in self.payment.items():
      player_price = values['Player']
      if player_price > 0:
        player_payment_string += "  - " + str(resource_name) + ": " + str(player_price) + "\n"
      frosthaven_price = values['Frosthaven']
      if frosthaven_price > 0:
        frosthaven_payment_string += "  - " + str(resource_name) + ": " + str(frosthaven_price)  + "\n"

    items_string = '\nItems:\n'

    for item in self.items_as_price:
      items_string += "  - " + item['Number'] + ": " + item['Name'] + "\n"
    if not confirm((player_payment_string + frosthaven_payment_string + items_string)):
      self.setup()
      return

    for resource_name, values in self.payment.items():
      player_price = values['Player']
      if player_price > 0:
        self.player[resource_name] -= player_price
      frosthaven_price = values['Frosthaven']
      if frosthaven_price > 0:
        self.frosthaven[resource_name] -= frosthaven_price
      
    self.player.update()
    self.frosthaven.update()
    for item in self.items_as_price:
      Utilites.remove_item(self.player, item)
    Utilites.add_item(self.player, self.item)
    navigation.go_to_character_items(self.player['Player'])

  def free_check_box_change(self, **event_args):
    self.setup()

      