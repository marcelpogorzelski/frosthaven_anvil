from ._anvil_designer import SettingsTemplate
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


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def export_button_click(self, **event_args):
    backup_blob = Utilites.get_backup()
    download(backup_blob)

  def import_file_loader_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    file_data = json.loads(file.get_bytes())

    for treasure in file_data:
      app_tables.treasures.add_row(Number=treasure['Number'], Content=treasure['Treasure'], Looted=False)



  def change_password_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.change_password_with_form(require_old_password=False)
    #anvil.users.reset_password('aa_chill_meeting', 'Marcel_Frost')



      
    
