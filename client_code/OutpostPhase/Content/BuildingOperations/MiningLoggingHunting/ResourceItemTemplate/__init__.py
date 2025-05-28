from ._anvil_designer import ResourceItemTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ......Utilites import bounded_text_box

class ResourceItemTemplate(ResourceItemTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.increase_button.enabled = False
    self.max_amount = app_tables.available_buildings.get(Number=self.item['BuildingNumber'])['CurrentBuilding']['Level']
    self.item['Amount'] = self.max_amount
    self.refresh_data_bindings()

  def set_amount_text_box(self):
    bounded_text_box(self.amount_text_box, 0, self.max_amount)
    self.item['Amount'] = self.amount_text_box.text
    self.set_buttons()
    self.parent.raise_event('x-update-total-gold')

  def set_buttons(self):
    self.increase_button.enabled = self.amount_text_box.text < self.max_amount
    self.decrease_button.enabled = self.amount_text_box.text > 0
    
  def decrease_button_click(self, **event_args):
    self.amount_text_box.text -= 1
    self.set_amount_text_box()

  def increase_button_click(self, **event_args):
    self.amount_text_box.text += 1
    self.set_amount_text_box()

  def amount_text_box_change(self, **event_args):
    self.set_amount_text_box()
    
