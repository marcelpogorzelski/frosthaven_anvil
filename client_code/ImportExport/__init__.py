from ._anvil_designer import ImportExportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import json
from anvil.tables import app_tables
from .. import Utilites

def parse_int_price(price):
  if price:
    return int(price)
  return 0


class ImportExport(ImportExportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def export_button_click(self, **event_args):
    backup_blob = Utilites.get_backup()
    download(backup_blob)

  def import_file_loader_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    item_prices = json.loads(file.get_bytes())

    for item_price in item_prices:
      item = app_tables.items.get(Number=item_price['Number'], Name=item_price['Name'])
      if not item:
        continue
      item['Gold'] = parse_int_price(item_price['Gold'])
      item['Lumber'] = parse_int_price(item_price['Lumber'])
      item['Metal'] = parse_int_price(item_price['Metal'])
      item['Hide'] = parse_int_price(item_price['Hide'])
      item['Arrowvine'] = parse_int_price(item_price['Arrowvine'])
      item['Axenut'] = parse_int_price(item_price['Axenut'])
      item['Corpsecap'] = parse_int_price(item_price['Corpsecap'])
      item['Rockroot'] = parse_int_price(item_price['Rockroot'])
      item['Flamefruit'] = parse_int_price(item_price['Flamefruit'])
      item['Snowthistle'] = parse_int_price(item_price['Snowthistle'])
      item['1Herb'] = False
      if item_price['1Herb'] == 1:
        item['1Herb'] = True
      item['2Herbs'] = False
      if item_price['2Herbs'] == 1:
        item['2Herbs'] = True
      item['Items'] = item_price['Items']
      item['TotalCount'] = parse_int_price(item_price['Count'])
      item['AvailableCount'] = parse_int_price(item_price['Count'])
      item.update()
      
    
