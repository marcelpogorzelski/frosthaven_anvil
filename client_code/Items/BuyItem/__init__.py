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
  def __init__(self, init_character, buy_item, **properties):
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
    selected_value = None
    
    character_items = []
    character_items.append(("None", self.item))
    for character in app_tables.characters.search():
      character_setup = self.setup_character(character)
      if character == init_character:
        selected_value = character_setup
      character_item = (str(character["Player"]), character_setup)
      character_items.append(character_item)
    self.character_drop_down.items = character_items
    
    if selected_value:
      self.character_drop_down.selected_value = selected_value
      self.item = selected_value
      self.reset_item_components()
      self.update_display()
    else:
      self.reset_item_components()
      self.update_full_display()

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

  def get_herb_display_text(self, price_value, player_resource, frosthaven_resource, resource):
    if (player_resource + frosthaven_resource) < price_value:
      return None
    player_price = min(price_value, player_resource)
    frosthaven_price = price_value - player_price

    background = 'Player'
    remainder_text = ''
    if frosthaven_price:
      background = 'Frosthaven'
      remainder_text = f" ({frosthaven_price} taken from Frosthaven)"
    price_text = f"{price_value} {resource} {remainder_text}"
    return {'price_text': price_text, 'visible': True, 'background': self.text_box_backgrounds[background], 'herb_price': {'Player': player_price, 'Frosthaven': frosthaven_price}}

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
        remainder_amount = character[resource] or 'None'
        remainder_text = f" ({remainder_amount} available)"

      price_text = f"{price}{remainder_text}"
      display_text[resource] = {'price_text': price_text, 'visible': visible, 'background': self.text_box_backgrounds[background]}

    for resource, price in character_setup['herb_price'].items():
      player_resource = character[resource]
      frosthaven_resource = self.frosthaven[resource]
      combined_resource = player_resource + frosthaven_resource

      if price == 0:
        none = {'price_text': '0', 'visible': False, 'background': self.text_box_backgrounds['Player'], 'herb_price': {'Player': 0, 'Frosthaven': 0}}
      else:
        none = self.get_herb_display_text(price, player_resource, frosthaven_resource, resource)
        if not none:
          background = 'Insufficient'
          character_setup['insufficient_resources'] = True
          remainder_amount = combined_resource or 'None'
          remainder_text = f" ({remainder_amount} available)"
          price_text = f"{price}{remainder_text}"
          none = {'price_text': price_text, 'visible': True, 'background': self.text_box_backgrounds['Insufficient']}

      one_herb = self.get_herb_display_text(price+1, player_resource, frosthaven_resource, resource)
      two_herbs = self.get_herb_display_text(price+2, player_resource, frosthaven_resource, resource)
      both = self.get_herb_display_text(price+3, player_resource, frosthaven_resource, resource)
      
      display_text[resource] = none
      herb_payment[resource] = dict()
      herb_payment[resource]['none'] = none
      herb_payment[resource]['one_herb'] = one_herb
      herb_payment[resource]['two_herbs'] = two_herbs
      herb_payment[resource]['both'] = both

    count, count2, count3 = (0,0,0)
    for _, herb_payment in herb_payment.items():
      if herb_payment['two_herbs']:
        count2 += 1
      if herb_payment['one_herb']:
        count += 1
      if herb_payment['both']:
        count3 += 1
        
    if character_setup['two_herbs']:
      insufficient = True
      if count2 > 0:
        insufficient = False
      character_setup['insufficient_resources'] = insufficient
      if character_setup['insufficient_resources']:
        return
  
    if character_setup['one_herb']:
      insufficient = True
      if count3 > 0:
        insufficient = False
      elif count > 1:
        insufficient = False
      character_setup['insufficient_resources'] = insufficient

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
    if not self.item['two_herbs']:
      return
    self.any_2_drop_down.visible = True
    self.any_2_label.visible = True
    if self.item['insufficient_resources']:
      self.any_2_drop_down.enabled = False
      return

    any_1_resource = self.any_1_drop_down.selected_value

    drop_down_items = list()
    drop_down_items.append(('Choose Herb', None))
    for resource, herb_payment in self.item['herb_payment'].items():
      tag = 'two_herbs'
      if resource == any_1_resource:
        tag = 'both'
      if not herb_payment[tag]:
        continue
      drop_down_items.append((herb_payment[tag]['price_text'], resource))
      
    self.any_2_drop_down.items = drop_down_items


  def handle_any_1_drop_down(self):
    if not self.item['one_herb']:
      return
    self.any_1_drop_down.visible = True
    self.any_1_label.visible = True
    if self.item['insufficient_resources']:
      self.any_1_drop_down.enabled = False
      return
      
    any_2_resource = self.any_2_drop_down.selected_value
    
    drop_down_items = list()
    drop_down_items.append(('Choose Herb', None))
    for resource, herb_payment in self.item['herb_payment'].items():
      tag = 'one_herb'
      if resource == any_2_resource:
        tag = 'both'
      if not herb_payment[tag]:
        continue
      drop_down_items.append((herb_payment[tag]['price_text'], resource))

    self.any_1_drop_down.items = drop_down_items

  def check_buy_button(self):
    if self.item['insufficient_resources']:
      self.buy_button.enabled = False
      return

    two_herbs = True
    if self.item['two_herbs']:
      two_herbs = self.any_2_drop_down.selected_value is not None
      
    one_herb = True
    if self.item['one_herb']:
      one_herb = self.any_1_drop_down.selected_value is not None

    self.buy_button.enabled = all([one_herb, two_herbs])
        
  def update_display(self):
    if self.item['item_owned']:
      self.price_label.text = 'You already own the item!'
      self.hide_all()
      return
    self.price_label.text = 'Price'

    self.handle_any_2_drop_down()
    self.handle_any_1_drop_down()
    
    for resource, display_text in self.item['display_text'].items():
      self.display_resource(resource, display_text['visible'], display_text['price_text'], display_text['background'])
    
    self.buy_button.visible = True
    self.add_button.visible = True
    
    self.check_buy_button()
    self.add_button.enabled = True

  def update_full_display(self):
    for resource, display_text in self.item['display_text'].items():
      self.display_resource(resource, display_text['visible'], display_text['price_text'], display_text['background'])

    if self.item['two_herbs']:
      self.any_2_drop_down.visible = True
    if self.item['one_herb']:
      self.any_1_drop_down.visible = True

  def reset_display(self):
    if self.item['character'] and not self.item['item_owned']:   
      for resource in Utilites.HERB_RESOURCES:
        self.item['display_text'][resource] = self.item['herb_payment'][resource]['none']
    self.buy_button.visible = False
    self.add_button.visible = False
    
    self.any_1_drop_down.items = [('', None)]
    self.any_1_drop_down.selected_value = None
    self.any_1_drop_down.visible = False
    self.any_1_label.visible = False

    self.any_2_drop_down.items = [('', None)]
    self.any_2_drop_down.selected_value = None
    self.any_2_drop_down.visible = False
    self.any_2_label.visible = False
    
    self.price_label.text = 'Price'

  def reset_item_components(self):
    self.item_component_flow_panel.clear()
    for item in self.item['item_components']:
      self.item_component_flow_panel.add_component(Image(source=item['Card']))

  def character_drop_down_change(self, **event_args):
    self.reset_display()
    self.item = self.character_drop_down.selected_value
    self.reset_item_components()
    if self.item['character']:
      self.update_display()
    else:
      self.update_full_display()

  def add_button_click(self, **event_args):
    if not confirm(f"Add {self.buy_item['Name']}?"):
      return
    Utilites.add_item(self.item['character'], self.buy_item)
    self.close_alert()


  def buy_button_click(self, **event_args):
    if not confirm(f"Buy {self.buy_item['Name']}?"):
      return
      
    character = self.item['character']
    player_payment = {}
    frosthaven_payment = {}
    for resource, price in self.item['gold_and_material_price'].items():
      player_payment[resource] = character[resource] - price
      
      if player_payment[resource] < 0:
        Notification(f"Not enought {resource}", timeout=10).show()
        self.close_alert()
        return

    any_1_resource = self.any_1_drop_down.selected_value
    any_2_resource = self.any_2_drop_down.selected_value
        
    for resource, herb_payment in self.item['herb_payment'].items():
      if resource == any_1_resource and resource == any_2_resource:
        herb_price = herb_payment['both']['herb_price']
      elif resource == any_1_resource:
        herb_price = herb_payment['one_herb']['herb_price']
      elif resource == any_2_resource:
        herb_price = herb_payment['two_herbs']['herb_price']
      else:
        herb_price = herb_payment['none']['herb_price']

      player_payment[resource] = character[resource] - herb_price['Player']
      frosthaven_payment[resource] = self.frosthaven[resource] - herb_price['Frosthaven']
      
      if (player_payment[resource] < 0) or (frosthaven_payment[resource] < 0):
        Notification(f"Not enought {resource}", timeout=10).show()
        self.close_alert()
        return
    
    character.update(
      Gold=player_payment['Gold'],
      Lumber=player_payment['Lumber'],
      Metal=player_payment['Metal'],
      Hide=player_payment['Hide'],
      Arrowvine=player_payment['Arrowvine'],
      Axenut=player_payment['Axenut'],
      Corpsecap=player_payment['Corpsecap'],
      Flamefruit=player_payment['Flamefruit'],
      Rockroot=player_payment['Rockroot'],
      Snowthistle=player_payment['Snowthistle']
    )
    
    self.frosthaven.update(
      Arrowvine=frosthaven_payment['Arrowvine'],
      Axenut=frosthaven_payment['Axenut'],
      Corpsecap=frosthaven_payment['Corpsecap'],
      Flamefruit=frosthaven_payment['Flamefruit'],
      Rockroot=frosthaven_payment['Rockroot'],
      Snowthistle=frosthaven_payment['Snowthistle']
    )
    
    Utilites.add_item(character, self.buy_item)
    for item in self.item['item_components']:
      Utilites.remove_item(character, item)
    self.close_alert()

  def process_any_drop_downs(self):
    if self.item['character']:
      for resource in Utilites.HERB_RESOURCES:
        self.item['display_text'][resource] = self.item['herb_payment'][resource]['none']

    any_1_resource = self.any_1_drop_down.selected_value
    any_2_resource = self.any_2_drop_down.selected_value

    if not any([any_1_resource, any_2_resource]):
      return

    if any_1_resource == any_2_resource:
      self.item['display_text'][any_1_resource] = self.item['herb_payment'][any_1_resource]['both']
      return
    if any_1_resource:
      self.item['display_text'][any_1_resource] = self.item['herb_payment'][any_1_resource]['one_herb']
    if any_2_resource:
      self.item['display_text'][any_2_resource] = self.item['herb_payment'][any_2_resource]['two_herbs']

  def any_drop_down_change(self, **event_args):
    self.process_any_drop_downs()
    self.update_display()

  def close_alert(self):
    self.raise_event("x-close-alert", value=self.item['character'])

  def cancel_button_click(self, **event_args):
    self.close_alert()



