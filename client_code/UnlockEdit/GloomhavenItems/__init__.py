from ._anvil_designer import GloomhavenItemsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

class GloomhavenItems(GloomhavenItemsTemplate):
  def __init__(self, **properties):

    self.card_selected = False
    self.image_file = None

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    

    self.gloomhaven_items = json.loads(app_tables.files.get(path='other_items.json')['file'].get_bytes())['gh']


  def number_text_box_pressed_enter(self, **event_args):
    item_number = self.number_text_box.text
    self.item = next(filter(lambda item: item['id'] == item_number, self.gloomhaven_items), None)

    if not self.item:
      self.hide_item()
    else:
      self.show_item()

  def hide_item(self):
    self.item = None
    self.number_text_box.text = None
    self.card_selected = False
    self.image_file = None
    self.refresh_data_bindings()

  def show_item(self):
    self.card_selected = True
    self.image_file = self.get_image(self.item['image'])
    self.refresh_data_bindings()

  def get_image(self, path):
    url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{path}"
    return URLMedia(url)
    

  def add_button_click(self, **event_args):
    pass
