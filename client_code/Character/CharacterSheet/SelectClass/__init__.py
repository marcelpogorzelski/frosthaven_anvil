from ._anvil_designer import SelectClassTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.js

def scale_up_icon(component, scale=2):
  dom_node = anvil.js.get_dom_node(component)
  for icon in dom_node.querySelectorAll('i'):
    icon.style.fontSize = f'{scale}em'

class SelectClass(SelectClassTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    active_classes = [character['Class'] for character in app_tables.characters.search()]

    for char_class in app_tables.classes.search(Available=True):
      if char_class in active_classes:
        continue
      class_button = Button(icon=f"_/theme/class_icons/{char_class['Nickname'].lower()}.png", role='elevated-button', tag=char_class)
      class_button.add_event_handler('click', self.change_class_button_click)
      scale_up_icon(class_button, 3)
      self.class_flow_panel.add_component(class_button)

  def change_class_button_click(self, **event_args):
    self.raise_event("x-close-alert", value=event_args['sender'].tag)
