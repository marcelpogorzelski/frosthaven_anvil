from ._anvil_designer import MainTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Character import Character
from ..Frosthaven import Frosthaven

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.initialize_navbar_links()
    self.frosthave_link.role = 'selected'
    self.go_to_character(self.frosthave_link.tag.form_to_open)

  def go_to_character(self, character):
    self.content_panel.clear()
    self.content_panel.add_component(character)
    

  def initialize_navbar_links(self):
    self.havard_link.tag.form_to_open = Character('Håvard')
    self.kristian_link.tag.form_to_open = Character('Kristian')
    self.john_magne_link.tag.form_to_open = Character('John Magne')
    self.marcel_link.tag.form_to_open = Character('Marcel')
    self.frosthave_link.tag.form_to_open = Frosthaven()

  def reset_links(self, **event_args):
    self.marcel_link.role = ''
    self.havard_link.role = ''
    self.kristian_link.role = ''
    self.john_magne_link.role = ''
    self.frosthave_link.role = ''

  def navbar_link_click(self, **event_args):
    self.reset_links()
    event_args['sender'].role = 'selected'
    self.go_to_character(event_args['sender'].tag.form_to_open)
    #open_form(event_args['sender'].tag.form_to_open)

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')
