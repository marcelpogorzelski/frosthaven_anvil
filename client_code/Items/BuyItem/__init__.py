from ._anvil_designer import BuyItemTemplate
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


class BuyItem(BuyItemTemplate):
  def __init__(self, buy_item, **properties):

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.item_image.source = buy_item["Card"]
    self.buy_item = buy_item

    self.text_box_backgrounds = {
      'Player': '',
      'Frosthaven': 'theme:Primary Container',
      'Insufficient': 'theme:Tertiary Container'
    }
    
    self.images_and_inputs = { 
      'Gold': {'image': self.gold_image, 'text_box': self.gold_text_box},
      'Lumber': {'image': self.lumber_image, 'text_box': self.lumber_text_box},
      'Metal': {'image': self.metal_image, 'text_box': self.metal_text_box},
      'Hide': {'image': self.hide_image, 'text_box': self.hide_text_box},
      'Arrowvine': {'image': self.arrowvine_image, 'text_box': self.arrowvine_text_box},
      'Axenut': {'image': self.axenut_image, 'text_box': self.axenut_text_box},
      'Corpsecap': {'image': self.corpsecap_image, 'text_box': self.corpsecap_text_box},
      'Flamefruit': {'image': self.flamefruit_image, 'text_box': self.flamefruit_text_box},
      'Rockroot': {'image': self.rockroot_image, 'text_box': self.rockroot_text_box},
      'Snowthistle': {'image': self.snowthistle_image, 'text_box': self.snowthistle_text_box},
    }
    
    self.item = self.init_setup(None)
    self.parse_full_item_price(self.item, buy_item)
    self.get_full_display_text(self.item)
    
    if self.item['uncraftable']:
      self.set_uncraftable()
      return

    if not self.item_in_store():
      self.set_not_in_store()
      return

    self.frosthaven = app_tables.frosthaven.search()[0]
    
    user = anvil.users.get_user(allow_remembered=True)
    self.player = app_tables.characters.get(Player=user["email"])

    selected_value = self.item
    
    character_items = []
    character_items.append(("None", self.item))
    for character in app_tables.characters.search():
      character_setup = self.setup_character(character)
      if character['Player'] == user["email"]:
        selected_value = character_setup
      character_item = (str(character["Player"]), character_setup)
      character_items.append(character_item)
    self.character_drop_down.items = character_items
    
    self.character_drop_down.selected_value = selected_value
    self.update_display()

  def set_uncraftable(self):
    item_list = ", ".join(self.item['uncraftable'])
    self.price_label.text = f"Cannot craft item. Missing item(s): {item_list}"
    self.character_drop_down.visible = False
    self.character_label.visible = False

  def set_not_in_store(self):
    self.price_label.text = (
      f"No more copies of item: {self.buy_item['Number']} - {self.buy_item['Name']}"
    )
    self.character_drop_down.visible = False
    self.character_label.visible = False
      
  def item_in_store(self):
    if self.buy_item["AvailableCount"] == 0:
      return False
    return True

  def item_owned(self, character):
    if self.buy_item in character["Items"]:
      return True
    return False

  def init_setup(self, character):
    init_gold_and_material_price = { resource: 0 for resource in  Utilites.MATERIAL_AND_GOLD_RESOURCES}
    init_herb_price = { resource: 0 for resource in  Utilites.HERB_RESOURCES}
    item_owned = False
    if character:
      item_owned = self.item_owned(character)
    init_setup = {
      'character': character,
      'display_text': dict(),
      'gold_and_material_price': init_gold_and_material_price,
      'herb_price': init_herb_price,
      'herb_payment': dict(),
      'item_components': list(),
      'one_herb': False,
      'two_herbs': False,
      'insufficient_resources': False,
      'uncraftable': list(),
      'item_owned': item_owned
    }

    return init_setup

  def setup_character(self, character):
    character_setup = self.init_setup(character)
  
    if character_setup['item_owned']:
      return character_setup

    self.parse_character_item_price(character_setup, self.buy_item)
    self.get_display_text(character_setup)
    return character_setup

  def get_display_text(self, character_setup):
    character = character_setup['character']
    display_text = character_setup['display_text']
    herb_payment = character_setup['herb_payment']
    
    for resource, price in character_setup['gold_and_material_price'].items():
      visible = price > 0
      background = 'Player'
      if not visible:
        display_text[resource] = {'price_text': '0', 'visible': visible, 'background': self.text_box_backgrounds[background]}
        continue

      remainder_text = ""
      if character[resource] < price:
        background = 'Insufficient'
        character_setup['insufficient_resources'] = True
        remainder_amount = character[resource] or 'No'
        remainder_text = f" ({remainder_amount} {resource.lower()} available)"

      price_text = f"{price}{remainder_text}"
      display_text[resource] = {'price_text': price_text, 'visible': visible, 'background': self.text_box_backgrounds[background]}

    for resource, price in character_setup['herb_price'].items():
      visible = price > 0
      background = 'Player'
      combined_rest = character[resource] + self.frosthaven[resource]
      herb_payment[resource] = {'Player': 0, 'Frosthaven': 0, 'PlayerRest': character[resource], 'FrosthavenRest': self.frosthaven[resource], 'CombinedRest': combined_rest}
      if not visible:
        display_text[resource] = {'price_text': '0', 'visible': visible, 'background': self.text_box_backgrounds[background]}
        continue
        
      combined_resource = character[resource] + self.frosthaven[resource]

      remainder_text = ''
      if  combined_resource < price:
        background = 'Insufficient'
        character_setup['insufficient_resources'] = True
        remainder_amount = combined_resource or 'No'
        remainder_text = f" ({remainder_amount} {resource.lower()} available)"

      elif character[resource] < price:
        background = 'Frosthaven'
        player_price = character[resource]
        frosthaven_price = price - character[resource]
        frosthaven_rest = self.frosthaven[resource] - frosthaven_price
        remainder_text = f" ({frosthaven_price} taken from Frosthaven)"
        herb_payment[resource] = {'Player': player_price, 'Frosthaven': frosthaven_price, 'PlayerRest': 0, 'FrosthavenRest': frosthaven_rest, 'CombinedRest': frosthaven_rest}
      else:
        player_price = price
        player_rest = character[resource] - price
        frosthaven_price = 0
        frosthaven_rest = self.frosthaven[resource]
        combined_rest = player_rest + frosthaven_rest
        herb_payment[resource] = {'Player': player_price, 'Frosthaven': frosthaven_price, 'PlayerRest': player_rest, 'FrosthavenRest': frosthaven_rest, 'CombinedRest': combined_rest}

      price_text = f"{price}{remainder_text}"
      display_text[resource] = {'price_text': price_text, 'visible': visible, 'background': self.text_box_backgrounds[background]}

  def parse_character_item_price(self, character_setup, item):
    character = character_setup['character']

    if item in character["Items"]:
      character_setup['item_components'].append(item)
      return
      
    for resource in Utilites.MATERIAL_AND_GOLD_RESOURCES:
      if item[resource] > 0:
        character_setup['gold_and_material_price'][resource] += item[resource]

    for resource in Utilites.HERB_RESOURCES:
      if item[resource] > 0:
        character_setup['herb_price'][resource] += item[resource]

    if item["1Herb"]:
      character_setup['one_herb'] = True
    if item["2Herbs"]:
      character_setup['two_herbs'] = True

    if not item['Items']:
      return
      
    for craft_component_item in item['Items']:
      self.parse_character_item_price(character_setup, craft_component_item)

  def get_full_display_text(self, full_setup):
    display_text = full_setup['display_text']

    for resource, price in full_setup['herb_price'].items():
      visible = price > 0
      if not visible:
        display_text[resource] = {'price_text': '0', 'visible': visible, 'background': self.text_box_backgrounds['Player']}
        continue

      price_text = f"{price}"
      display_text[resource] = {'price_text': price_text, 'visible': visible, 'background': self.text_box_backgrounds['Player']}
      
    for resource, price in full_setup['gold_and_material_price'].items():
      visible = price > 0
      if not visible:
        display_text[resource] = {'price_text': '0', 'visible': visible, 'background': self.text_box_backgrounds['Player']}
        continue

      price_text = f"{price}"
      display_text[resource] = {'price_text': price_text, 'visible': visible, 'background': self.text_box_backgrounds['Player']}

  def parse_full_item_price(self, full_setup, item):
    for resource in Utilites.MATERIAL_AND_GOLD_RESOURCES:
      if item[resource] > 0:
        full_setup['gold_and_material_price'][resource] += item[resource]

    for resource in Utilites.HERB_RESOURCES:
      if item[resource] > 0:
        full_setup['herb_price'][resource] += item[resource]
        
    if item["1Herb"]:
      full_setup['one_herb'] = True
    if item["2Herbs"]:
      full_setup['two_herbs'] = True

    if not item['Items']:
      return

    for craft_component_item in item['Items']:
      self.check_uncraftable(full_setup, craft_component_item)
      full_setup['item_components'].append(craft_component_item)

  def check_uncraftable(self, full_setup, item):
    if item['Items']:
      for craft_component_item in item['Items']:
        self.check_uncraftable(full_setup, item)
        
    if not item['Available']:
      full_setup['uncraftable'].append(item['Number'])

  def display_resource(self, resource, visible, price_text, background):
    self.images_and_inputs[resource]['image'].visible = visible
    self.images_and_inputs[resource]['text_box'].visible = visible
    self.images_and_inputs[resource]['text_box'].text = price_text
    self.images_and_inputs[resource]['text_box'].background = background

  def hide_all(self):
    for resource, images_and_inputs in self.images_and_inputs.items():
      images_and_inputs['image'].visible = False
      images_and_inputs['text_box'].visible = False

  def handle_any_2_drop_down(self):
    self.any_2_drop_down.visible = self.item['two_herbs']
    self.any_2_label.visible = self.item['two_herbs']
    if not self.item['two_herbs']:
      self.any_2_drop_down.selected_value = None
      return

    drop_down_items = [('Choose herb', None)]
    for resource, payment in self.item['herb_payment'].items():
      if payment['CombinedRest'] < 2:
        continue
        
      drop_down_item_text = f"2 {resource}"   
      if payment['PlayerRest'] < 2:
        frosthaven_price = 2 - payment['PlayerRest']
        drop_down_item_text += f"  ({frosthaven_price} from Frosthaven)"
      drop_down_items.append((drop_down_item_text, resource))
    self.any_2_drop_down.items = drop_down_items

  def handle_any_1_drop_down(self):
    self.any_1_drop_down.visible = self.item['one_herb']
    self.any_1_label.visible = self.item['one_herb']
    if not self.item['one_herb']:
      self.any_1_drop_down.selected_value = None
      return

    
    
  def update_display(self):
    if self.item['item_owned']:
      self.price_label.text = 'You already own the item!'
      self.hide_all()
      return
    self.price_label.text = 'Price'
    for resource, display_text in self.item['display_text'].items():
      self.display_resource(resource, display_text['visible'], display_text['price_text'], display_text['background'])

    self.handle_any_2_drop_down()
    self.handle_any_1_drop_down()

    if not self.item['character']:
      self.buy_button.visible = False
      self.add_button.visible = False
      return
    
    self.buy_button.visible = True
    self.add_button.visible = True
    self.buy_button.enabled = not self.item['insufficient_resources']
    self.add_button.enabled = True

  def character_drop_down_change(self, **event_args):
    self.item = self.character_drop_down.selected_value
    self.update_display()

  def add_button_click(self, **event_args):
    Utilites.add_item(self.item['character'], self.buy_item)
    self.raise_event("x-close-alert")





  




  def buy_button_click(self, **event_args):
    if self.free_check_box.checked:
      if not self.player:
        alert("Choose a player in the drop down menu")
        return
      if not confirm(
        f"Do you want to add item:\n   {self.item['Number']} - {self.item['Name']}"
      ):
        return

      Utilites.add_item(self.player, self.item)
      navigation.go_to_character_items(self.player["Player"])
      return

    if self.two_herbs:
      if not self.any_2_drop_down.selected_value:
        alert("Select a herb from 'Any 2' drop down")
        return
      two_herb_name = self.any_2_drop_down.selected_value["Herb"]
      two_herb_player = self.any_2_drop_down.selected_value["Player"]
      two_herb_frosthaven = self.any_2_drop_down.selected_value["Frosthaven"]
      if two_herb_name in self.payment:
        self.payment[two_herb_name]["Player"] += two_herb_player
        self.payment[two_herb_name]["Frosthaven"] += two_herb_frosthaven
      else:
        self.payment[two_herb_name] = {
          "Player": two_herb_player,
          "Frosthaven": two_herb_frosthaven,
        }
    if self.one_herb:
      if not self.any_1_drop_down.selected_value:
        alert("Select a herb from 'Any 1' drop down")
        return

    player_display_name = self.player["Player"]
    player_payment_string = player_display_name + ":\n"
    frosthaven_payment_string = "\nFrosthaven:\n"

    for resource_name, values in self.payment.items():
      player_price = values["Player"]
      if player_price > 0:
        player_payment_string += (
          "  - " + str(resource_name) + ": " + str(player_price) + "\n"
        )
      frosthaven_price = values["Frosthaven"]
      if frosthaven_price > 0:
        frosthaven_payment_string += (
          "  - " + str(resource_name) + ": " + str(frosthaven_price) + "\n"
        )

    items_string = "\nItems:\n"

    for item in self.items_as_price:
      items_string += "  - " + item["Number"] + ": " + item["Name"] + "\n"
    if not confirm((player_payment_string + frosthaven_payment_string + items_string)):
      self.setup()
      return

    for resource_name, values in self.payment.items():
      player_price = values["Player"]
      if player_price > 0:
        self.player[resource_name] -= player_price
      frosthaven_price = values["Frosthaven"]
      if frosthaven_price > 0:
        self.frosthaven[resource_name] -= frosthaven_price

    self.player.update()
    self.frosthaven.update()
    for item in self.items_as_price:
      Utilites.remove_item(self.player, item)
    Utilites.add_item(self.player, self.item)
    navigation.go_to_character_items(self.player["Player"])



