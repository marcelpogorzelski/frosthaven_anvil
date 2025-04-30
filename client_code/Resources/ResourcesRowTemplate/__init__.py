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
    self.setup_tags()

  def setup_tags(self):
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
    text_box = event_args['sender']
    Utilites.bounded_text_box(text_box, 0, 10000)
    self.item[text_box.tag] = text_box.text or 0
    self.parent.raise_event('x-update-value')

  def experience_text_box_change(self, **event_args):
    Utilites.bounded_text_box(self.experience_text_box, 0, 500)
    
    Utilites.set_experience(self.item, self.experience_text_box.text or 0)

  def check_text_box_change(self, **event_args):
    Utilites.bounded_text_box(self.check_text_box, 0, 18)
    #checkmarks = int(self.check_text_box.text) or 0

    Utilites.set_checkmarks(self.item, self.check_text_box.text or 0)
