from ._anvil_designer import GloomhavenItemsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

SLOT_CONVERSION = {
  'legs': 'Feet',
  '1h': 'One Hand',
  'small': 'Small',
  'head': 'Head',
  '2h': 'Two Hands',
  'body': 'Body'
}

class GloomhavenItems(GloomhavenItemsTemplate):
  def __init__(self, **properties):

    self.card_selected = False
    self.none_item = {
      'image_file': None,
      'cost': None,
      'usage': None,
    }
    
    self.item = dict()

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.gloomhaven_items = json.loads(app_tables.files.get(path='other_items.json')['file'].get_bytes())['gh']


  def number_text_box_pressed_enter(self, **event_args):
    item_number = self.number_text_box.text
    self.item = next(filter(lambda item: item['id'] == item_number, self.gloomhaven_items), dict())

    if not self.item:
      self.hide_item()
    else:
      self.show_item()

  def hide_item(self):
    self.number_text_box.text = None
    self.card_selected = False
    self.refresh_data_bindings()

  def show_item(self):
    self.card_selected = True
    if 'image_file' not in self.item:
      self.item['image_file'] = self.get_image()
    if 'usage' not in self.item:
      self.item['usage'] = 'Passive'
      if 'spent' in self.item:
        self.item['usage'] = 'Spent'
      if 'consumed' in self.item:
        self.item['usage'] = 'Lost'
        
    self.refresh_data_bindings()

  def get_image(self):
    url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{self.item['image']}"
    return URLMedia(url)
    

  def add_button_click(self, **event_args):
    pass
