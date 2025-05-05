from ._anvil_designer import PetsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .PetTemplate import PetTemplate

class Pets(PetsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    for pet in app_tables.pets.search(Captured=True):
      self.pet_flow_panel.add_component(PetTemplate(pet))
      

    # Any code you write here will run before the form opens.
