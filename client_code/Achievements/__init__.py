from ._anvil_designer import AchievementsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Achievement import Achievement
from .BrummixTracks import BrummixTracks
from .CoralCrownShard import CoralCrownShard

class Achievements(AchievementsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    for achievement in app_tables.achievements.search(Available=True):
      if achievement['Upgrades'] == 0:
        achievement_form = Achievement(achievement)
      elif achievement['Name'] == 'Brummix Tracks':
        achievement_form = BrummixTracks(achievement)
      elif achievement['Name'] == 'Coral Crown Shard':
        achievement_form = CoralCrownShard(achievement)
      self.achievements_flow_panel.add_component(achievement_form)
