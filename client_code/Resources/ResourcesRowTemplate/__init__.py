from ._anvil_designer import ResourcesRowTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Utilites


class ResourcesRowTemplate(ResourcesRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.gold_text_box.tag = 'Gold'
    self.lumber_text_box.tag = 'Lumber'
    self.metal_text_box.tag = 'Metal'
    self.hide_text_box.tag = 'Hide'
    
    self.arrowvine_text_box.tag = 'Arrowvine'
    self.axenut_text_box.tag = 'Axenut'
    self.corpsecap_text_box.tag = 'Corpsecap'
    self.flamefruit_text_box.tag = 'Flamefruit'
    self.rockroot_text_box.tag = 'Rockroot'
    self.snowthistle_text_box.tag = 'Snowthistle'


  def text_box_change(self, **event_args):
    self.item[event_args['sender'].tag] = event_args['sender'].text
    self.parent.raise_event('x-update-value')
    #resource_form = self.parent.parent.parent
    #resource_form.total_row_replace()

  def experience_text_box_change(self, **event_args):
    experience = int(self.experience_text_box.text) or 0
    if experience > 500:
      self.experience_text_box.text = 500
    if experience < 0:
      self.experience_text_box.text = 0
    
    Utilites.set_experience(self.item, experience)

  def check_text_box_change(self, **event_args):
    checkmarks = int(self.check_text_box.text) or 0
    if checkmarks > 18:
      self.check_text_box.text = 18
    if checkmarks < 0:
      self.check_text_box.text = 0
    Utilites.set_checkmarks(self.item, checkmarks)
