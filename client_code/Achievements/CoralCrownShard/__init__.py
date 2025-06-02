from ._anvil_designer import CoralCrownShardTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CoralCrownShard(CoralCrownShardTemplate):
  def __init__(self, achievement, **properties):
    self.init_components(**properties)

    image_list = [self.image_1, self.image_2, self.image_3, self.image_4, self.image_5, self.image_6]

    for index, image in zip(range(achievement['CurrentLevel']), image_list):
      image.source = achievement['Image']
    for _, image in zip(range(6 - achievement['CurrentLevel']), reversed(image_list)):
      image.visible = False


