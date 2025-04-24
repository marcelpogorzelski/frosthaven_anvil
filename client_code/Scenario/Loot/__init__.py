from ._anvil_designer import LootTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Loot(LootTemplate):
  def __init__(self, loot, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    loot['Money'] = loot.pop('Coins')
    loot['treasure-chest-item'] = loot.pop('Item')

    loot_items = list()
    for name in ['Money', 'Lumber', 'Metal', 'Hide', 'Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle', 'treasure-chest-item']:
      count = loot[name]
      if not count:
        continue
      item = { 'Source': f'_/theme/resource_images/fh-{name.lower()}-bw-icon.png', 'Count': count}
      loot_items.append(item)

    self.loot_repeating_panel.items = loot_items

