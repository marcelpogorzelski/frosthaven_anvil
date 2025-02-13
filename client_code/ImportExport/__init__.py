from ._anvil_designer import ImportExportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import json
from anvil.tables import app_tables
from .. import Utilites


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
        print(item_price['Number'])
      
    
