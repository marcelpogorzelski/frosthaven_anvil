from ._anvil_designer import ClassesTemplate
from anvil import *
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

    #_/theme/class_icons/trap.png

    unlocked_classes = [unlocked_class['Nickname'] for unlocked_class in app_tables.classes.search()]

    for nickname in Frosthaven_info.class_names.keys():
      if nickname in unlocked_classes:
        continue
      class_button = Button(icon=f'_/theme/class_icons/{nickname.lower()}.png', role='elevated-button', tag=nickname)
      class_button.add_event_handler('click', self.add_class_button_click)
      scale_up_icon(class_button, 6)
      self.class_flow_panel.add_component(class_button)


  def add_class_button_click(self, **event_args):
    nickname = event_args['sender'].tag

    if not confirm(f"Do you want to add the class: {nickname}?"):
      return

    class_name = Frosthaven_info.class_names[nickname]["name"]
    class_id = Frosthaven_info.class_names[nickname]["id"]
    
    app_tables.classes.add_row(Name=class_name, Id=class_id, Nickname=nickname)
    event_args['sender'].visible = False
    event_args['sender'].enabled = False
