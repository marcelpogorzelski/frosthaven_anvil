from ._anvil_designer import DefendAttackTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DefendAttack(DefendAttackTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.item = app_tables.frosthaven.search()[0]
    self.barracks_level = app_tables.available_buildings.get(Number=98)['CurrentBuilding']['Level'] - 1
    self.attack_mod = 5+10*self.barracks_level
    self.attack_mod_label.text=f"Advantage and -{ self.attack_mod} attack"

    self.check_guards()

  def check_guards(self):
    if self.item['Guards'] <= 0:
      self.use_guard_button.enabled = False
    # Any code you write here will run before the form opens.

  def use_guard_button_click(self, **event_args):
    self.item['Guards'] -= 1
    self.check_guards()
    self.refresh_data_bindings()
    Notification("Used Guard", timeout=6).show()
