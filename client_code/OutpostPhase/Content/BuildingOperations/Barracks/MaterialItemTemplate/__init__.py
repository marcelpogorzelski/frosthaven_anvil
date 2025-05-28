from ._anvil_designer import MaterialItemTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ......Utilites import bounded_text_box

class MaterialItemTemplate(MaterialItemTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.max_count = min(self.item['MaxRecruit'], self.item['Count'])
    self.count_text_box.text = self.item['Init']
    self.item['Amount'] = self.item['Init']
    self.set_buttons()

  def set_count_text_box(self):
    bounded_text_box(self.count_text_box, 0, self.max_count)
    self.item['Amount'] = self.count_text_box.text
    self.set_buttons()
    self.parent.raise_event('x-update-resources')
    
  def set_buttons(self):
    self.increase_button.enabled = self.count_text_box.text < self.max_count
    self.decrease_button.enabled = self.count_text_box.text > 0

  def count_text_box_change(self, **event_args):
    self.set_count_text_box()

  def decrease_button_click(self, **event_args):
    self.count_text_box.text -= 1
    self.set_count_text_box()

  def increase_button_click(self, **event_args):
    self.count_text_box.text += 1
    self.set_count_text_box()

