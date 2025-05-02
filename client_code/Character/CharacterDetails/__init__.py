from ._anvil_designer import CharacterDetailsTemplate
from anvil import *
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

    self.player_name_label.text = player_name
    self.character = app_tables.characters.get(Player=player_name)
    class_info = Frosthaven_info.class_names[self.character['Class']['Nickname']]
    self.mat_front_image.source = self.get_image(class_info['matImage'])
    self.mat_back_image.source = self.get_image(class_info['matImageBack'])
    self.sheet_image.source = self.get_image(class_info['sheetImage'])
    
  def get_image(self, path):
    url = f"https://raw.githubusercontent.com/cmlenius/gloomhaven-card-browser/images/images/{path}"
    return URLMedia(url)


