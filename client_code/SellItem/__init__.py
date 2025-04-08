from ._anvil_designer import SellItemTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class SellItem(SellItemTemplate):
  def __init__(self, player_name, item_list, gold_price, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.herb_names = ['Arrowvine', 'Axenut', 'Corpsecap', 'Flamefruit', 'Rockroot', 'Snowthistle']
    
    self.player_name = player_name
    self.player_name_label.text = player_name
    self.gold_text_box.text = gold_price

    self.item_list = item_list
    self.herb_choice_drop_down_list = list()
    
    for item in item_list:
      self.item_flow_panel.add_component(Image(source=item['Card']))
      if item['Destilled']:
        self.herb_choise_label.visible = True
        self.add_herb_choice(item)

    self.sell_button = Button(role='filled-button', text='Sell')
    self.sell_button.add_event_handler('click', self.sell_click)
    self.sell_card.add_component(self.sell_button)


  def add_herb_choice(self, item):
    herb_drop_down_items = list()

    if item['2Herbs']:
      herb_drop_down = DropDown(items=self.herb_names)
      self.sell_card.add_component(herb_drop_down)
      self.herb_choice_drop_down_list.append(herb_drop_down)
      return
      
    for herb_name in self.herb_names:
      if item[herb_name] > 0:
        herb_drop_down_items.append(herb_name)
    herb_drop_down = DropDown(items=herb_drop_down_items)
    self.sell_card.add_component(herb_drop_down)
    self.herb_choice_drop_down_list.append(herb_drop_down)
    

  def sell_click(self, **event_args):
    if not confirm("Are you sure you want to sell"):
      return
    
    player_name = self.player_name.replace(" ", "_")
    
    for item in self.item_list:
      item[player_name] = False
      item['AvailableCount'] += 1

    character = app_tables.characters.get(Player=self.player_name)
    character['Gold'] += self.gold_text_box.text
    for herb_drop_down in self.herb_choice_drop_down_list:
      herb_name = herb_drop_down.selected_value
      character[herb_name] += 1
    self.go_to_character(self.player_name)

    
  def go_to_character(self, player_name):
    main_form = get_open_form()

    items_link = main_form.player_links[player_name]['Sheet Link']
    main_form.open_player_link(player_name, items_link)
