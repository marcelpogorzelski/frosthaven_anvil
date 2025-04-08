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
    #print(anvil.server.cookies)
    #self.force_login()
    self.login()


  def login(self):
    if anvil.users.get_user(allow_remembered=True):
      open_form(Main(start_form=Frosthaven()))

  def force_login(self):
    anvil.server.call('force_login')
    print(anvil.users.get_user())
    anvil.users.change_password_with_form(require_old_password=False)

    
    

  def login_button_click(self, **event_args):
    anvil.users.login_with_form()
    self.login()

