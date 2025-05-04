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
    self.item = self.achievement_drop_down.selected_value

  def get_image(self, path):
    url = f"https://raw.githubusercontent.com/teamducro/gloomhaven-storyline/refs/heads/master/resources/img/achievements/{path}.png"
    return URLMedia(url)

  def get_image_source(self):
    image_name = self.item['Id']
    if self.item['CurrentLevel'] > 1:
      image_name += str(self.item['CurrentLevel'])
    return self.get_image(image_name)

  def button_text(self):
    if self.item['Descriptor']:
      return f"Add new {self.item['Descriptor'][:-1]}"
    return ''

  def button_visible(self):
    #print(1)
    if self.item['Upgrades'] == 0:
      return False
    #print(2)
    if not self.item['Available']:
      return False
    #print(3)
    if self.item['Upgrades'] == self.item['CurrentLevel']:
      return False

    return True
      
  def show_levels(self):
    if not self.item['Available']:
      return False
    if self.item['Upgrades']:
      return True
    return False

  def available_check_box_change(self, **event_args):
    if self.item['Connected'] and self.available_check_box.checked:
      self.item['Connected']['Available'] = False
    self.item['Available'] = self.available_check_box.checked
    self.refresh_data_bindings()

  def achievement_drop_down_change(self, **event_args):
    self.item = self.achievement_drop_down.selected_value
    self.refresh_data_bindings()

  def upgrade_button_click(self, **event_args):
    self.item['CurrentLevel'] += 1
    self.refresh_data_bindings()
