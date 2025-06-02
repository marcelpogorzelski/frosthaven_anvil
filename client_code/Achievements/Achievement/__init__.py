from ._anvil_designer import AchievementTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Achievement(AchievementTemplate):
  def __init__(self, achievement, **properties):
    self.init_components(**properties)
    self.achievement_image.source = achievement['Image']


