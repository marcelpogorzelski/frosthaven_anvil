from ._anvil_designer import MainTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Character import Character

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.initialize_navbar_links()

  def initialize_navbar_links(self):
    self.havard_link.tag.form_to_open = Character('Havard')
    self.kristian_link.tag.form_to_open = Character('Kristian')
    self.john_magne_link.tag.form_to_open = Character('John Magne')
    self.marcel_link.tag.form_to_open = Character('Marcel')

  def reset_links(self, **event_args):
    self.marcel_link.role = ''
    self.havard_link.role = ''
    self.kristian_link.role = ''
    self.john_magne_link.role = ''

  def navbar_link_click(self, **event_args):
    self.reset_links()
    event_args['sender'].role = 'selected'
    open_form(event_args['sender'].tag.form_to_open)
