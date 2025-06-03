from ._anvil_designer import CharacterDetailsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Frosthaven_info


class CharacterDetails(CharacterDetailsTemplate):
  def __init__(self, player_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #self.adjust_width()

    self.character = app_tables.characters.get(Player=player_name)
    
    self.mat_front_image.source = self.character['Class']['MatImage']
    self.mat_back_image.source = self.character['Class']['MatBackImage']
    self.sheet_image.source = self.character['Class']['SheetImage']


