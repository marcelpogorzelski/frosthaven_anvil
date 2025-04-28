from ._anvil_designer import TreasuresTemplateTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TreasuresTemplate(TreasuresTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def looted_check_box_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.raise_event('x-check-looted')
    self.refresh_data_bindings()
