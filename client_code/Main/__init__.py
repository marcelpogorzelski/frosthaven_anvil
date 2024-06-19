from ._anvil_designer import MainTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Character import Character
from ..Frosthaven import Frosthaven
from ..Party import Party
from ..Resources import Resources
from ..ImportExport import ImportExport
from ..Calendar import Calendar
from ..Scenarios import Scenarios

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.frosthave_link.role = 'selected'
    self.change_form(Frosthaven())
 
  def change_form(self, form):
    self.content_panel.clear()
    self.content_panel.add_component(form, full_width_row=True)

  def reset_links(self, **event_args):
    for comp in self.navbar_column_panel.get_components():
      if type(comp) is Spacer:
        continue
      if comp.role == 'selected':
        comp.role = ''

  def navbar_link_select(self, link):
    self.reset_links()
    link.role = 'selected'

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')

  def frosthave_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Frosthaven())

  def party_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Party())

  def resources_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Resources())

  def havard_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Character('Håvard'))

  def kristian_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Character('Kristian'))

  def john_magne_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Character('John Magne'))

  def marcel_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Character('Marcel'))

  def import_export_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(ImportExport())

  def calendar_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Calendar())

  def scenarios_link_click(self, **event_args):
    self.navbar_link_select(event_args['sender'])
    self.change_form(Scenarios())
