from ._anvil_designer import FinishScenarioRowTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class FinishScenarioRowTemplate(FinishScenarioRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.item["Player"] == "Frosthaven":
      self.gold_text_box.visible = False
      self.gold_text_box.enabled = False
      self.experience_text_box.visible = False
      self.experience_text_box.enabled = False
      self.gold_coin_text_box.visible = False
      self.gold_coin_text_box.enabled = False
      self.checkmarks_text_box.visible = False
      self.checkmarks_text_box.enabled = False

    self.item["Experience"] = None
    self.item["Gold"] = None
    self.item["GoldCoins"] = None
    self.item["CheckMarks"] = None
    self.item["Lumber"] = None
    self.item["Metal"] = None
    self.item["Hide"] = None
    self.item["Arrowvine"] = None
    self.item["Axenut"] = None
    self.item["Corpsecap"] = None
    self.item["Flamefruit"] = None
    self.item["Rockroot"] = None
    self.item["Snowthistle"] = None

    # Any code you write here will run before the form opens.
