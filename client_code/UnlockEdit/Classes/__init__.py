from ._anvil_designer import ClassesTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Frosthaven_info

import anvil.js

def scale_up_icon(component, scale=2):
  dom_node = anvil.js.get_dom_node(component)
  for icon in dom_node.querySelectorAll('i'):
    icon.style.fontSize = f'{scale}em'


class Classes(ClassesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    for char_class in app_tables.classes.search(Available=False):
      class_button = Button(icon=f"_/theme/class_icons/{char_class['Nickname'].lower()}.png", role='elevated-button', tag=char_class)
      class_button.add_event_handler('click', self.add_class_button_click)
      scale_up_icon(class_button, 6)
      self.class_flow_panel.add_component(class_button)


  def add_class_button_click(self, **event_args):
    char_class = event_args['sender'].tag

    if not confirm(f"Do you want to add the class: {char_class['Nickname']}?"):
      return

    char_class['Available'] = True
    
    event_args['sender'].visible = False
    event_args['sender'].enabled = False
