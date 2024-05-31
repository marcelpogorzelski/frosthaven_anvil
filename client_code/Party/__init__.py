from ._anvil_designer import PartyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Party(PartyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = app_tables.characters.get(Player='Marcel')
    #self.repeating_panel_1.items = app_tables.characters.search()

    # Any code you write here will run before the form opens.

  def outlined_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    print(self.item['Name'])
    print(event_args['sender'].text)
    self.item.update()

  def outlined_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass
