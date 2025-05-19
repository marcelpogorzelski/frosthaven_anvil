from ._anvil_designer import SellItemTemplate
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


class SellItem(SellItemTemplate):
  def __init__(self, sell_item, **properties):
    init_gold_and_material_price = { resource: 0 for resource in  Utilites.MATERIAL_AND_GOLD_RESOURCES}
    init_herb_price = { resource: 0 for resource in  Utilites.HERB_RESOURCES}
    #display_text = { resource: {'visible': False} for resource in Utilites.ALL_RESOURCES}

    self.item = {
      'character': None,
      'gold_and_material_price': init_gold_and_material_price,
      'herb_price': init_herb_price,
      'item_components': list(),
      'one_herb': False,
      'two_herbs': False,
      'insufficient_resources': False,
      'uncraftable': list(),
      'item_owned': False
    }
    self.parse_full_item_price(self.item, sell_item)
    self.item['display_text'] = self.get_full_display_text(self.item)

    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item_image.source = sell_item["Card"]
    #self.item = app_tables.items.get(Number=item['Number'])
    #self.item = None
    self.sell_item = sell_item

    self.frosthaven = app_tables.frosthaven.search()[0]

    if not self.item_in_store():
      self.price_label.text = (
        f"No more copies of item: {self.sell_item['Number']} - {self.sell_item['Name']}"
      )
      self.free_check_box.visible = False
      self.character_drop_down.visible = False
      self.character_label.visible = False
      return

    user = anvil.users.get_user(allow_remembered=True)
    self.player = app_tables.characters.get(Player=user["email"])

    character_items = []
    character_items.append(("None", None))

    for character in app_tables.characters.search():
      character_setup = self.setup_character(character)
      character_item = (str(character["Player"]), character_setup)
      character_items.append(character_item)
    self.character_drop_down.items = character_items
    self.character_drop_down.selected_value = self.player

  def item_in_store(self):
    if self.sell_item["AvailableCount"] == 0:
      return False
    return True

  def item_owned(self, character):
    if self.sell_item in character["Items"]:
      return True
    return False

  def setup_character(self, character):
    init_gold_and_material_price = { resource: 0 for resource in  Utilites.MATERIAL_AND_GOLD_RESOURCES}
    init_herb_price = { resource: 0 for resource in  Utilites.HERB_RESOURCES}
    character_setup = {
      'character': character,
      'gold_and_material_price': init_gold_and_material_price,
      'herb_price': init_herb_price,
      'item_components': list(),
      'one_herb': False,
      'two_herbs': False,
      'insufficient_resources': False,
      'uncraftable': list(),
      'item_owned': self.item_owned(character)
    }
  
    if character_setup['item_owned']:
      return character_setup

    self.parse_character_item_price(character_setup, self.sell_item)
    character_setup['display_text'] = self.get_display_text(character_setup)
    return character_setup

  def get_display_text(self, character_setup):
    character = character_setup['character']
    display_text = {}
    
    for resource, price in character_setup['gold_and_material_price'].items():
      visible = price > 0
      if not visible:
        display_text[resource] = {'price_text': '0', 'visible': visible}
        continue

      remainder_text = ""
      if character[resource] < price:
        character_setup['insufficient_resources'] = True
        remainder_amount = character[resource] or 'No'
        remainder_text = f" ({remainder_amount} {resource.lower()} available)"

      price_text = f"{price}{remainder_text}"
      display_text[resource] = {'price_text': price_text, 'visible': visible}

    for resource, price in character_setup['herb_price'].items():
      visible = price > 0
      if not visible:
        display_text[resource] = {'price_text': '0', 'visible': visible}
        continue
      combined_resource = character[resource] + self.frosthaven[resource]

      if  combined_resource < price:
        character_setup['insufficient_resources'] = True
        remainder_amount = combined_resource or 'No'
        remainder_text = f" ({remainder_amount} {resource.lower()} available)"

      elif character[resource] < price:
        frosthaven_price = price - character[resource]
        remainder_text = f" ({frosthaven_price} taken from Frosthaven)"
        
      price_text = f"{price}{remainder_text}"
      display_text[resource] = {'price_text': price_text, 'visible': visible}
    return display_text

  def parse_character_item_price(self, character_setup, item):
    character = character_setup['character']
    if not item['Available']:
      character_setup['uncraftable'].append(item['Number'])
      return

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

    if not item['Items2']:
      return
      
    for craft_component_item in item['Items2']:
      self.parse_character_item_price(character_setup, craft_component_item)

  def get_full_display_text(self, full_setup):
    display_text = {}

    for resource, price in full_setup['gold_and_material_price'].items():
      visible = price > 0
      if not visible:
        display_text[resource] = {'price_text': '0', 'visible': visible}
        continue

      price_text = f"{price}"
      display_text[resource] = {'price_text': price_text, 'visible': visible}
    return display_text

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

    if not item['Items2']:
      return

    for craft_component_item in item['Items2']:
      if not item['Available']:
        full_setup['uncraftable'].append(item['Number'])
        continue
      full_setup['item_components'].append(item)



  def character_drop_down_change(self, **event_args):
    print(self.character_drop_down.selected_value)







      

  def get_character_resources(self, character):
    character_resources = {}
    for resource in Utilites.MATERIAL_AND_GOLD_RESOURCES:
      character_resources[resource] = {"Player": character[resource], "Sum": -1}

    for resource in Utilites.HERB_RESOURCES:
      sum_resource = character[resource] + self.frosthaven[resource]
      character_resources[resource] = {
        "Player": character[resource],
        "Sum": sum_resource,
      }
    return character_resources


  def item_free(self):
    if self.free_check_box.checked and self.character_drop_down.selected_value:
      self.buy_button.text = "Add item"
      self.buy_button.enabled = True
      self.buy_button.visible = True
      self.price_label.text = "Add item for free"
      return True
    return False

  def parse_full_item_price2(self, item):
    for resource, price in self.prices.items():
      if item[resource] > 0:
        price["Price"] += item[resource]
    if item["1Herb"]:
      self.one_herb = True
    if item["2Herbs"]:
      self.two_herbs = True
      
    for craft_component_item in item['Items2']:
      if not craft_component_item["Available"]:
        self.uncraftable(craft_component_item)
        return
      self.items_as_price.append(craft_component_item)

  def uncraftable(self, item):
    self.craftable = False
    item_number = item["Number"]
    if self.price_label.text == "Price":
      self.price_label.text = f"Cannot craft item. Missing item(s): {item_number}"
    else:
      self.price_label.text += f", {item_number}"

  def show_resource(self, resource_name):
    resource = self.prices[resource_name]
    if resource["Price"] == 0:
      return

    if not self.player:
      resource["TextBox"].text = resource["Price"]
      resource["Image"].visible = True
      resource["TextBox"].visible = True
      return

    price = resource["Price"]
    available_player = self.available_resources[resource_name]["Player"]
    available_total = self.available_resources[resource_name]["Sum"]

    if available_player >= price:
      resource["TextBox"].text = price
      self.payment[resource_name] = {"Player": price, "Frosthaven": 0}
    elif available_total >= price:
      remainder = price - available_player
      resource["TextBox"].type = "text"
      resource["TextBox"].text = f"{price} ({remainder} taken from Frosthaven)"
      resource["TextBox"].background = "theme:Tertiary Container"
      if available_player > 0:
        self.payment[resource_name] = {
          "Player": available_player,
          "Frosthaven": remainder,
        }
      else:
        self.payment[resource_name] = {"Player": 0, "Frosthaven": remainder}
    else:
      self.insufficient_funds = True
      resource["TextBox"].type = "text"
      if available_total == -1:
        available_total = available_player
      if available_total == 0:
        resource["TextBox"].text = f"{price} (No {resource_name.lower()} available)"
      else:
        resource[
          "TextBox"
        ].text = f"{price} ({available_total} {resource_name.lower()} available)"
      resource["TextBox"].background = "theme:Primary Container"

    resource["Image"].visible = True
    resource["TextBox"].visible = True

  def show_two_herbs(self):
    if not self.two_herbs:
      return

    if not self.player:
      self.any_2_label.visible = True
      self.any_2_drop_down.visible = True
      return

    any_2_drop_down_list = list()
    any_2_drop_down_list.append(("Please select a herb", None))
    for herb_name in Utilites.HERB_RESOURCES:
      price = self.prices[herb_name]["Price"]
      available_player = self.available_resources[herb_name]["Player"] - price
      available_total = self.available_resources[herb_name]["Sum"] - price

      if available_player >= 2:
        drop_down_text = herb_name
        drop_down_select = {"Player": 2, "Frosthaven": 0, "Herb": herb_name}
        any_2_drop_down_list.append((drop_down_text, drop_down_select))
      elif available_total >= 2:
        frosthaven_portion = 2 - available_player
        drop_down_text = f"{herb_name} ({frosthaven_portion} from Frosthaven)"
        drop_down_select = {
          "Player": available_player,
          "Frosthaven": frosthaven_portion,
          "Herb": herb_name,
        }
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
      self.items_as_price_flow_panel.add_component(Image(source=item["Card"]))

    if self.one_herb:
      self.any_1_label.visible = True
      self.any_1_drop_down.visible = True

    if not self.player:
      return

    if self.insufficient_funds:
      self.buy_button.text = "Insufficient resources"
    else:
      self.buy_button.enabled = True
    self.buy_button.visible = True

  def reset_prices(self):
    self.prices = {
      "Gold": {"Price": 0, "TextBox": self.gold_text_box, "Image": self.gold_image},
      "Lumber": {
        "Price": 0,
        "TextBox": self.lumber_text_box,
        "Image": self.lumber_image,
      },
      "Metal": {"Price": 0, "TextBox": self.metal_text_box, "Image": self.metal_image},
      "Hide": {"Price": 0, "TextBox": self.hide_text_box, "Image": self.hide_image},
      "Arrowvine": {
        "Price": 0,
        "TextBox": self.arrowvine_text_box,
        "Image": self.arrowvine_image,
      },
      "Axenut": {
        "Price": 0,
        "TextBox": self.axenut_text_box,
        "Image": self.axenut_image,
      },
      "Corpsecap": {
        "Price": 0,
        "TextBox": self.corpsecap_text_box,
        "Image": self.corpsecap_image,
      },
      "Flamefruit": {
        "Price": 0,
        "TextBox": self.flamefruit_text_box,
        "Image": self.flamefruit_image,
      },
      "Rockroot": {
        "Price": 0,
        "TextBox": self.rockroot_text_box,
        "Image": self.rockroot_image,
      },
      "Snowthistle": {
        "Price": 0,
        "TextBox": self.snowthistle_text_box,
        "Image": self.snowthistle_image,
      },
    }

  def reset(self):
    self.reset_prices()
    for price in self.prices.values():
      price["Image"].visible = False
      price["TextBox"].visible = False
      price["TextBox"].text = 0
      price["TextBox"].type = "number"
      price["TextBox"].background = ""

    self.payment = dict()

    self.one_herb = False
    self.two_herbs = False
    self.any_1_drop_down.selected_value = ""
    self.any_2_drop_down.selected_value = ""
    self.any_1_label.visible = False
    self.any_2_label.visible = False
    self.any_1_drop_down.visible = False
    self.any_2_drop_down.visible = False
    self.any_2_drop_down.enabled = True

    self.insufficient_funds = False
    self.buy_button.text = "Buy"
    self.buy_button.visible = False
    self.buy_button.enabled = False

    self.price_label.text = "Price"

    self.available_resources = dict()

    self.items_as_price = list()
    self.items_as_price_flow_panel.clear()

    self.free_check_box.visible = True



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

  def free_check_box_change(self, **event_args):
    self.setup()
