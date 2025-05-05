from ._anvil_designer import AchievementTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Achievement(AchievementTemplate):
  def __init__(self, achievemnet, **properties):
    self.init_components(**properties)
    self.achievement_image.source = self.get_image(achievemnet['Id'])

  def get_image(self, path):
    return app_files.achievements.get(path + '.png')

