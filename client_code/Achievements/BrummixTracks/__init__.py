from ._anvil_designer import BrummixTracksTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from itertools import repeat


class BrummixTracks(BrummixTracksTemplate):
  def __init__(self, achievement, **properties):
    self.init_components(**properties)

    brummix_image_path = self.get_image(achievement['Id'])

    for _ in repeat(None, achievement['CurrentLevel']):
      self.achievemnet_flow_panel.add_component(Image(source=brummix_image_path))

  def get_image(self, path):
    return app_files.achievements.get(path + '.png')
