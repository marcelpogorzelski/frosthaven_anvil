from ._anvil_designer import AddClassTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AddClass(AddClassTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def add_class_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.add_class_text_box.text:
      return
    new_class = self.add_class_text_box.text
    if not confirm(f"Do you want to add the class: {new_class}?"):
      return
    if len(app_tables.classes.search(Name=new_class)) > 0:
      return
    app_tables.classes.add_row(Name=new_class)
    self.add_class_text_box.text = ''