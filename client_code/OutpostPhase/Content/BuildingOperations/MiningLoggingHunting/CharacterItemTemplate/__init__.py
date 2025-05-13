from ._anvil_designer import CharacterItemTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CharacterItemTemplate(CharacterItemTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    #self.character = app_tables.characters.get(Player=self.item['Player'])
    self.name_label.text = f"{self.item['Character']['Player']} ({self.item['Character']['Gold']})"
    self.gold_text_box.text = self.item['InitialValue']
    

  def decrease_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def increase_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def gold_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass
