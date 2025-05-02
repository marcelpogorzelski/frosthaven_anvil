from ._anvil_designer import PetTemplateTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PetTemplate(PetTemplateTemplate):
  def __init__(self, pet, **properties):
    self.pet = pet
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
