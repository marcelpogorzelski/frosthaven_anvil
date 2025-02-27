from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Main import Main
from ..Frosthaven import Frosthaven


class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def login_button_click(self, **event_args):
    anvil.users.login_with_form()
    if anvil.users.get_user():
      open_form(Main(start_form=Frosthaven()))

