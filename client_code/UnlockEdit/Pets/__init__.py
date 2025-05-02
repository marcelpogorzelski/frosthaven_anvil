from ._anvil_designer import PetsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Pets(PetsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    for pet in app_tables.pets.search(Captured=False):
      pet_button = Button(text=pet['Name'], tag=pet, role='elevated-button')
      pet_button.add_event_handler('click', self.capture_pet)
      self.pet_flow_panel.add_component(pet_button)
    
  def capture_pet(self, **event_args):
    pet = event_args['sender'].tag
    if not confirm(f"Do you want to capture: {pet['Name']}?"):
      return
    event_args['sender'].visible = False
    event_args['sender'].enabled = False
    pet['Captured'] = True
