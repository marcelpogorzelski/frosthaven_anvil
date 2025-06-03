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

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.other_items = json.loads(app_tables.files.get(path='other_items.js')['file'].get_bytes())



  def number_text_box_pressed_enter(self, **event_args):
    item_number = self.number_text_box.text

    for item in self.other_items:
      if item['expansion'] != 'Gloomhaven':
        continue
      if item['name'] == f"item {item_number:03}":
        self.show_item(item)
        return

    def show_item(self, item):
      self.item = item
      pass

  def get_image(self, path):
    url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{path}"
    return URLMedia(url)
    

  def add_button_click(self, **event_args):
    pass
