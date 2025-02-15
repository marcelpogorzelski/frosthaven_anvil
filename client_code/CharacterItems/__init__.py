from ._anvil_designer import CharacterItemsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CharacterItems(CharacterItemsTemplate):
  def __init__(self, player_name,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.player_name = player_name
    self.populate_items()

  def populate_items(self):
    self.item_list = app_tables.items.search(Available=True)

    self.character_items_flow_panel.clear()
    for item in self.item_list:
      if not item[self.player_name]:
        continue
      #display_mode = 'shrink_to_fit'
      display_mode = 'original_size'
      item_image = Image(source=item['Card'], display_mode=display_mode, tooltip=f"Item {item['Number']}", tag=item)
      self.character_items_flow_panel.add_component(item_image)
