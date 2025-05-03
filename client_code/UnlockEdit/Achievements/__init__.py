from ._anvil_designer import AchievementsTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Achievements(AchievementsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.achievement_drop_down.items = [(achievement['Name'], achievement) for achievement in app_tables.achievements.search()]
    items = list()
    self.groups = {'JAR': list(), 'CORE': list()}
    for achievement in app_tables.achievements.search():
      if achievement['Group']:
        self.groups[achievement['Group']].append(achievement)
      items.append((achievement['Name'],achievement))
    self.achievement_drop_down.items = items
    self.item = self.achievement_drop_down.selected_value

  def get_image_source(self):
    if not self.item['CurrentLevel']:
      self.achievement_image.source = f"https://raw.githubusercontent.com/teamducro/gloomhaven-storyline/refs/heads/master/resources/img/achievements/{self.item['Id']}.png"
    number = ''
    if not self.item['CurrentLevel'] > 0:
      pass
      

  def show_levels(self):
    if not self.item['Available']:
      return False
    if self.item['Upgrades']:
      return True
    return False

  def change_group(self):
    for achievement in self.groups[self.item['Group']]:
      if achievement == self.item:
        continue
      achievement['Available'] = False

  def available_check_box_change(self, **event_args):
    if self.item['Group'] and self.available_check_box.checked:
      self.change_group()
    self.item['Available'] = self.available_check_box.checked
    self.refresh_data_bindings()

  def achievement_drop_down_change(self, **event_args):
    self.item = self.achievement_drop_down.selected_value
    self.refresh_data_bindings()
