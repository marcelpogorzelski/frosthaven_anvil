from ._anvil_designer import ScenarioiDifficultyRowTemplateTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ScenarioiDifficultyRowTemplate(ScenarioiDifficultyRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    if self.item['Recommended']:
      self.background = 'theme:Secondary Container'
      #self.background = 'theme:Primary Container'
      
      #self.role = ['tonal-card']
    if self.item['Selected']:
      #self.background = 'theme:Primary Container'
      self.role = 'tonal-card'
      self.background = 'theme:Primary Container'
      

    # Any code you write here will run before the form opens.
