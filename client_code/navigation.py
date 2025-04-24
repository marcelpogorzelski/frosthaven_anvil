from anvil import get_open_form
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def go_to_character_items(player_name):
  main_form = get_open_form()

  items_link = main_form.player_links[player_name]['Items Link']
  main_form.open_player_link(player_name, items_link)

def go_to_character(player_name):
  main_form = get_open_form()

  items_link = main_form.player_links[player_name]['Sheet Link']
  main_form.open_player_link(player_name, items_link)