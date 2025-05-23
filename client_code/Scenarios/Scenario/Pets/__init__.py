from ._anvil_designer import PetsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pets(PetsTemplate):
  def __init__(self, pets, gamestate, pet_button, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.gamestate = gamestate
    self.pet_button = pet_button

    for pet in pets:
      pet_button = Button(text=pet['Name'], tag=pet, role='elevated-button')
      pet_button.add_event_handler('click', self.capture_pet)
      self.pet_flow_panel.add_component(pet_button)

  def capture_pet(self, **event_args):
    pet = event_args['sender'].tag
    if not confirm(f"Do you want to capture: {pet['Name']}?"):
      return
    pet['Captured'] = True
    self.close_alert(pet)

  def close_alert(self, pet):
    self.raise_event("x-close-alert", value=pet)