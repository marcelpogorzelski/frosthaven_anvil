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
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.achievement_image.source = self.get_image(achievemnet['Id'])

  def get_image(self, path):
    url = f"https://raw.githubusercontent.com/teamducro/gloomhaven-storyline/refs/heads/master/resources/img/achievements/{path}.png"
    return URLMedia(url)

    # Any code you write here will run before the form opens.
