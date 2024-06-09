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
    #self.status_list = ['Available', 'Finished', 'Locked']

    # Any code you write here will run before the form opens.

  def status_filter_button_click(self, **event_args):
    selected_value = self.drop_down_1.selected_value
    if not selected_value:
      return
    #self.drop_down_1.items =[value for value in self.drop_down_1.items if value != self.drop_down_1.selected_value]
    selected_value_label = Label(text=selected_value, tag='Status')
    self.flow_panel_1.add_component(selected_value_label)
    remove_button = Button(icon='fa:remove', tag=selected_value_label)
    remove_button.set_event_handler('click', self.remove_button_click)
    self.flow_panel_1.add_component(remove_button)
    self.drop_down_1.items =[value for value in self.drop_down_1.items if value != selected_value]

  def remove_button_click(self, **event_args):
    if event_args['sender'].tag == 'Status':
      self.drop_down_1.items = self.drop_down_1.items.append(event_args['sender'].tag.text).sort()
      ...
    event_args['sender'].tag.remove_from_parent()
    event_args['sender'].remove_from_parent()