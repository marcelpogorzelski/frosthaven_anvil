from ._anvil_designer import ScenarioDiffucultyRowTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ScenarioDiffucultyRowTemplate(ScenarioDiffucultyRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.set_event_handler("x-hightlight-level", self.handle_my_event)

  def handle_my_event(self, **event_args):
    if event_args['scenario_level'] == self.item['Level']:
      event_args['sender'].role = 'tonal-card'
    else:
      event_args['sender'].role = ''
