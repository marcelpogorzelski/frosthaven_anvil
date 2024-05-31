from ._anvil_designer import FrosthavenTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites


class Frosthaven(FrosthavenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.frosthaven = app_tables.frosthaven.search()[0]
    self.name_text_box.text = self.frosthaven['Name']
    self.inspiration_text_box.text = self.frosthaven['Inspiration']
    self.moral_text_box.text = self.frosthaven['Moral']
    self.soldiers_text_box.text = self.frosthaven['Soldiers']
    self.bonus_defense_text_box.text = self.frosthaven['Defense']
    self.total_defense_text_box.text = Utilites.get_total_defense(moral=self.frosthaven['Moral'], defense=self.frosthaven['Defense'])
    self.populate_resource_panel()

  def populate_resource_panel(self):
    self.gold_text_box.text = self.frosthaven["Gold"]
    self.lumber_text_box.text = self.frosthaven["Lumber"]
    self.metal_text_box.text = self.frosthaven["Metal"]
    self.hide_text_box.text = self.frosthaven["Hide"]
    self.arrowvine_text_box.text = self.frosthaven["Arrowvine"]
    self.axenut_text_box.text = self.frosthaven["Axenut"]
    self.corpsecap_text_box.text = self.frosthaven["Corpsecap"]
    self.flamefruit_text_box.text = self.frosthaven["Flamefruit"]
    self.rockroot_text_box.text = self.frosthaven["Rockroot"]
    self.snowthistle_text_box.text = self.frosthaven["Snowthistle"]

  def change_frosthaven_value(self, new_value, key):
    self.frosthaven[key] = new_value
    self.frosthaven.update()
    if key == "Experience":
      self.level_text_box.text = Utilites.get_level(self.frosthaven[key])

  def inc_button_click(self, **event_args):
    new_value = event_args["sender"].tag.text + 1
    event_args["sender"].tag.text = new_value
    self.change_frosthaven_value(new_value, event_args["sender"].tag.tag)

  def dec_button_click(self, **event_args):
    new_value = event_args["sender"].tag.text - 1
    event_args["sender"].tag.text = new_value
    self.change_frosthaven_value(new_value, event_args["sender"].tag.tag)

  def text_box_pressed_enter(self, **event_args):
    self.change_frosthaven_value(event_args["sender"].text, event_args["sender"].tag)

  def text_box_change(self, **event_args):
    self.change_frosthaven_value(event_args["sender"].text, event_args["sender"].tag)
