from ._anvil_designer import ResourcesRowTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Utilites


class ResourcesRowTemplate(ResourcesRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    resource_form = self.parent.parent.parent
    resource_form.total_row_replace()

  def experience_text_box_change(self, **event_args):
    player = event_args['sender'].tag
    experience = event_args['sender'].text or 0
    player['Level'] = Utilites.get_level(experience=experience)
    player.update()