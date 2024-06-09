from ._anvil_designer import Form1Template
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    self.flow_panel_1.add_component(Label(text=self.drop_down_1.selected_value))
    remove_button = Button(icon='fa:remove')
    remove_button.set_event_handler()
    self.flow_panel_1.add_component(remove_button)

  def remove_button_click(self, **event_args):
    ...