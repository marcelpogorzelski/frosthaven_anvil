from ._anvil_designer import BarracksTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .....Utilites import MATERIAL_RESOURCES, bounded_text_box
from ..CharacterPay import CharacterPay


class Barracks(BarracksTemplate):
  def __init__(self, gamestate, finish_phase_tag, **properties):
    self.phase_enabled = False
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.finish_phase_tag = finish_phase_tag
    self.gamestate = gamestate

    self.finished = gamestate[finish_phase_tag]
    if self.finished:
      self.disable_phase()

    self.character_pay_form = None

  def setup_barracks(self):
    self.barracks_level = app_tables.available_buildings.get(Number=98)['CurrentBuilding']['Level']
    self.guard_count = app_tables.frosthaven.search()[0]['Guards']

    self.max_guard_count = 2 + (self.barracks_level * 2)
    self.missing_quard_count = self.max_guard_count - self.guard_count

    if self.missing_quard_count == 0:
      self.set_as_finished()
      return
    
    if self.missing_quard_count >= 2 and self.barracks_level >= 3:
      self.max_recruit = 2
    else:
      self.max_recruit = 1

    self.count_text_box.text = self.max_recruit
    
    self.missing_guard_label.text = f"Missing {self.missing_quard_count} guards"

    #self.buy_count = int((self.barracks_level + 1) / 2)
    
    self.update_input()

    self.material_repeating_panel.set_event_handler('x-update-resources', self.check_recruit_button)

    self.phase_enabled = True
    self.refresh_data_bindings()

  def update_input(self):
    self.setup_material_resource()
    self.setup_character_pay()
    self.update_resource()

  def setup_material_resource(self):
    self.frosthaven = app_tables.frosthaven.search()[0]
    resource_items = list()
    
    for resource in MATERIAL_RESOURCES:
      if self.frosthaven[resource] == 0:
        continue
      image = f"_/theme/resource_images/fh-{resource.lower()}-bw-icon.png"
      resource_item = {'Image': image, 'Resource': resource, 'Count': self.frosthaven[resource], 'MaxRecruit': self.count_text_box.text, 'Init': 0}
      resource_items.append(resource_item)

    for _ in range(self.count_text_box.text):
      init = max(resource_items, key=lambda x: x['Count'] - x['Init'])
      init['Init'] += 1

    self.material_repeating_panel.items = resource_items

  def setup_character_pay(self):
    self.total_gold = self.count_text_box.text * 3
    if self.character_pay_form:
      self.character_pay_form.update_total_gold(self.total_gold)
    else:
      event_handler = 'x-update-gold'
      self.character_pay_form = CharacterPay(self.total_gold, event_handler)
      self.character_pay_form.set_event_handler(event_handler, self.check_recruit_button)
      self.character_pay_flow_panel.add_component(self.character_pay_form, width=500)
    
  def disable_phase(self):
    self.barracks_column_panel.background = 'theme:Outline'
    self.barracks_start_flow_panel.visible = False
    self.phase_enabled = False
    self.refresh_data_bindings()
    self.name_label.text += " - Finished"

  def set_as_finished(self):
    self.disable_phase()
    self.finished = True
    self.gamestate[self.finish_phase_tag] = True
    self.raise_event("x-building-finished")

  def start_button_click(self, **event_args):
    self.barracks_start_flow_panel.visible = False
    self.setup_barracks()
    
  def set_buttons(self):
    self.count_increase_button.enabled = self.count_text_box.text < self.max_recruit
    self.count_decrease_button.enabled = self.count_text_box.text > 0
    
  def count_increase_button_click(self, **event_args):
    self.count_text_box.text += 1
    self.set_buttons()
    self.update_input()

  def count_decrease_button_click(self, **event_args):
    self.count_text_box.text -= 1
    self.set_buttons()
    self.update_input()

  def count_text_box_change(self, **event_args):
    bounded_text_box(self.count_text_box, 0, self.max_recruit)
    self.set_buttons()
    self.update_input()

  def check_recruit_button(self, **event_args):
    self.update_resource()

  def update_resource(self):
    material_sum = sum(resource_item['Amount'] for resource_item in self.material_repeating_panel.items)
    button_enabled = True
    if material_sum != self.count_text_box.text:
      button_enabled = False
    if self.character_pay_form.sum_gold != self.total_gold:
      button_enabled = False
    self.recruit_button.enabled = button_enabled

  def recruit_button_click(self, **event_args):
    guards_recruited = self.count_text_box.text
    if guards_recruited == 0:
      Notification("No guards recruited", timeout=6).show()
      self.set_as_finished()
      return
      
    frosthaven = app_tables.frosthaven.search()[0]

    resource_amounts = dict()
    for resource in self.material_repeating_panel.items:
      resource_amounts[resource['Resource']] = resource['Amount']

    lumber = frosthaven['Lumber'] - resource_amounts['Lumber']
    metal = frosthaven['Metal'] - resource_amounts['Metal']
    hide = frosthaven['Hide'] - resource_amounts['Hide']
    guards = frosthaven['Guards'] + guards_recruited

    frosthaven.update(
      Lumber=lumber,
      Metal=metal,
      Hide=hide,
      Guards=guards
    )
    
    self.character_pay_form.pay()

    notification_text = "One guard recruited"
    if guards_recruited >= 2:
      notification_text = f"{guards_recruited} guards recruited"

    Notification(notification_text, timeout=6).show()
    
    self.set_as_finished()
    
    
