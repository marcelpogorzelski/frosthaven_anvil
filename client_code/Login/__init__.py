from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Main import Main
from ..Frosthaven import Frosthaven
from .. import Utilites

class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.login()

  def login(self):
    user = anvil.users.get_user()
    if user:
      open_form(Main(player_name=user['email']))
    
  def login_button_click(self, **event_args):
    anvil.users.login_with_form()
    self.login()

