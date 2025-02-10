from ._anvil_designer import UnlockEditTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class UnlockEdit(UnlockEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.item_type_drop_down.items = ['Head', 'Body', 'Feet', 'One Hand', 'Two Hands', 'Small']
    self.item_usage_drop_down.items = ['Passive', 'Spent', 'Lost', 'Flip']

    self.previous_item = self.item_number_text_box.text
    self.item_change()

    building_list = []
    for building in app_tables.available_buildings.search():
      building_list.append((str(building['Number']), building))
    self.building_drop_down.items = building_list
    self.building_change()

    scenario_list = []
    #for scenario in app_tables.scenarios.search(Status='Undiscovered'):
    for scenario in app_tables.scenarios.search():
      scenario_list.append((scenario['Number'], scenario))
    self.scenario_drop_down.items = scenario_list
    self.scenario_change()

    # Any code you write here will run before the form opens.

  def add_class_button_click(self, **event_args):
    if not self.add_class_text_box.text:
      return
    new_class = self.add_class_text_box.text
    if not confirm(f"Do you want to add the class: {new_class}?"):
      return
    if len(app_tables.classes.search(Name=new_class)) > 0:
      return
    app_tables.classes.add_row(Name=new_class)
    self.add_class_text_box.text = ''

  def item_show(self, visible):
    self.item_name_text_box.visible = visible
    self.item_image.visible = visible
    self.item_type_drop_down.visible = visible
    self.item_usage_drop_down.visible = visible
    self.item_gold_check_box.visible = visible

  def item_change(self):
    self.item_selected = app_tables.items.get(Number=self.item_number_text_box.text)

    if not self.item_selected:
      alert(f"{self.item_number_text_box.text} is not an item! Returning to item {self.previous_item}")
      self.item_number_text_box.text = self.previous_item
      self.item_selected = app_tables.items.get(Number=self.item_number_text_box.text)
    self.previous_item = self.item_number_text_box.text
    
    self.item_show(self.item_selected['Available'])
    self.item_available_check_box.checked = self.item_selected['Available']
    
    self.item_name_text_box.text = self.item_selected['Name']
    self.item_image.source = self.item_selected['Card']
    self.item_type_drop_down.selected_value = self.item_selected['Type']
    self.item_usage_drop_down.selected_value = self.item_selected['Usage']
    self.item_gold_check_box.checked = self.item_selected['HasGoldCost']

  def item_number_text_box_pressed_enter(self, **event_args):
    self.item_change()
    
  def item_drop_down_change(self, **event_args):
    self.item_change()

  def item_available_check_box_change(self, **event_args):
    self.item_selected['Available'] = self.item_available_check_box.checked
    self.item_selected.update()
    self.item_change()

  def item_gold_check_box_change(self, **event_args):
    self.item_selected['HasGoldCost'] = self.item_gold_check_box.checked
    self.item_selected.update()

  def item_type_drop_down_change(self, **event_args):
    self.item_selected['Type'] = self.item_type_drop_down.selected_value
    self.item_selected.update()

  def item_usage_drop_down_change(self, **event_args):
    self.item_selected['Usage'] = self.item_usage_drop_down.selected_value
    self.item_selected.update()

  def building_change(self):
    self.building_selected = self.building_drop_down.selected_value
    if self.building_selected['CurrentLevel'] > 0:
      self.building = app_tables.buildings.get(Name=self.building_selected['Name'], Level=self.building_selected['CurrentLevel'])
      self.building_image.source = self.building['Card Front']
    else:
      self.building = app_tables.buildings.get(Name=self.building_selected['Name'], Level=self.building_selected['CurrentLevel'])
      print(self.building)
      self.building_image.source = None
    
    available = self.building_selected['Available']
    self.building_available_check_box.checked = available
    self.building_text_box.visible = available
    self.building_image.visible = available
    self.building_level_drop_down.visible = available

    if self.building:
      self.building_image.source = self.building['Card Front']
    else:
      self.building_image.source = None
    self.building_text_box.text = self.building_selected['Name']
    self.building_level_drop_down.items = [str(level) for level in range(self.building_selected['Max Level']+1)]
    self.building_level_drop_down.selected_value = str(self.building_selected['CurrentLevel'])
    
    
  def building_drop_down_change(self, **event_args):
    self.building_change()
    
  def building_available_check_box_change(self, **event_args):
    available = self.building_available_check_box.checked
    self.building_text_box.visible = available
    self.building_image.visible = available
    self.building_level_drop_down.visible = available

    self.building_selected['Available'] = available
    self.building_selected.update()

  def building_level_drop_down_change(self, **event_args):
    self.building_selected['CurrentLevel'] = int(self.building_level_drop_down.selected_value)
    self.building_selected.update()
    self.building_change()

  def scenario_change(self):
    self.scenario_selected = self.scenario_drop_down.selected_value
    if self.scenario_selected['Status'] == 'Undiscovered':
      available = False
    else:
      available = True
    
    self.scenario_name_text_box.visible = available
    self.scenario_image.visible = available
    
    self.scenario_status_drop_down.selected_value = self.scenario_selected['Status']
    self.scenario_name_text_box.text = self.scenario_selected['Name']
    
    if self.scenario_selected['Number'][0:1] == 'So':
      self.scenario_image.source = None
      return
    sticker_name = self.scenario_selected['Name'].lower().replace(' ', '-')
    sticker_number = int(self.scenario_selected['Number'][1:])
    sticker_media = URLMedia(f"https://github.com/any2cards/frosthaven/blob/master/images/art/frosthaven/stickers/individual/location-stickers/fh-{sticker_number:03d}-{sticker_name}.png?raw=true")
    self.scenario_image.source = sticker_media
    
  
  def scenario_drop_down_change(self, **event_args):
    self.scenario_change()

  def scenario_status_drop_down_change(self, **event_args):
    self.scenario_selected['Status'] = self.scenario_status_drop_down.selected_value
    self.scenario_selected.update()
    self.scenario_change()
    return
    new_status = self.scenario_status_drop_down.selected_value
    if new_status == 'Undiscovered':
      available = False
    else:
      available = True

    self.scenario_name_text_box.visible = available
    self.scenario_image.visible = available
    
    self.scenario_selected['Status'] = new_status
    self.scenario_selected.update()
    




