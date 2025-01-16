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

    item_list = []
    for item in app_tables.items.search():
      item_list.append((item['Number'], item))
    self.edit_item_drop_down.items = item_list
    
    self.item_type_drop_down.items = ['Head', 'Body', 'Feet', 'One Hand', 'Two Hands', 'Small']
    self.item_usage_drop_down.items = ['Passive', 'Spent', 'Lost', 'Flip']
    
    self.change_edit_item()

    building_list = []
    for building in app_tables.available_buildings.search():
      building_list.append((str(building['Number']), building))
    self.building_drop_down.items = building_list
    self.change_edit_building()

    # Any code you write here will run before the form opens.

  def add_class_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.add_class_text_box.text:
      return
    new_class = self.add_class_text_box.text
    if not confirm(f"Do you want to add the class: {new_class}?"):
      return
    if len(app_tables.classes.search(Name=new_class)) > 0:
      return
    app_tables.classes.add_row(Name=new_class)
    self.add_class_text_box.text = ''

  def change_edit_item(self):
    self.edit_item = self.edit_item_drop_down.selected_value
    
    available = self.edit_item['Available']
    self.item_available_check_box.checked = available
    self.item_name_text_box.visible = available
    self.item_image.visible = available
    self.item_type_drop_down.visible = available
    self.item_usage_drop_down.visible = available
    self.item_gold_check_box.visible = available
    
    self.item_name_text_box.text = self.edit_item['Name']
    self.item_image.source = self.edit_item['Card']
    self.item_type_drop_down.selected_value = self.edit_item['Type']
    self.item_usage_drop_down.selected_value = self.edit_item['Usage']
    self.item_gold_check_box.checked = self.edit_item['Gold']
    
  def edit_item_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.change_edit_item()

  def item_available_check_box_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    available = self.item_available_check_box.checked
    self.item_name_text_box.visible = available
    self.item_image.visible = available
    self.item_type_drop_down.visible = available
    self.item_usage_drop_down.visible = available
    self.item_gold_check_box.visible = available

    self.edit_item['Available'] = available
    self.edit_item.update()

  def item_gold_check_box_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.edit_item['Gold'] = self.item_gold_check_box.checked
    self.edit_item.update()

  def item_type_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.edit_item['Type'] = self.item_type_drop_down.selected_value
    self.edit_item.update()

  def item_usage_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.edit_item['Usage'] = self.item_usage_drop_down.selected_value
    self.edit_item.update()

  def change_edit_building(self):
    self.available_building = self.building_drop_down.selected_value
    if self.available_building['CurrentLevel'] > 0:
      self.building = app_tables.buildings.get(Name=self.available_building['Name'], Level=self.available_building['CurrentLevel'])
      self.building_image.source = self.building['Card Front']
    else:
      self.building_image.source = None
    
    available = self.available_building['Available']
    self.building_available_check_box.checked = available
    self.building_text_box.visible = available
    self.building_image.visible = available
    self.building_level_drop_down.visible = available

    self.building_text_box.text = self.available_building['Name']
    self.building_level_drop_down.items = [str(level) for level in range(self.available_building['Max Level']+1)]
    self.building_level_drop_down.selected_value = str(self.available_building['CurrentLevel'])
    
    
  def building_drop_down_change(self, **event_args):
    self.change_edit_building()
    
  def building_available_check_box_change(self, **event_args):
    available = self.building_available_check_box.checked
    self.building_text_box.visible = available
    if self.available_building['CurrentLevel'] > 0:
      self.building_image.visible = available
    self.building_level_drop_down.visible = available

    self.available_building['Available'] = available
    self.available_building.update()

  def building_level_drop_down_change(self, **event_args):
    self.available_building['CurrentLevel'] = int(self.building_level_drop_down.selected_value)
    self.available_building.update()
    if self.available_building['CurrentLevel'] > 0:
      self.building = app_tables.buildings.get(Name=self.available_building['Name'], Level=self.available_building['CurrentLevel'])
      self.building_image.source = self.building['Card Front']
      self.building_image.visible = True
    else:
      self.building_image.visible = False
    




