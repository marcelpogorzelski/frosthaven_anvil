import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from anvil import get_open_form
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def go_to_character_items(player_name):
  main_form = get_open_form()
  main_form.open_character(player_name, tab='CharacterItems')

def go_to_character(player_name):
  main_form = get_open_form()
  main_form.open_character(player_name)

def go_to_scenario(scenario):
  main_form = get_open_form()
  main_form.open_scenario(scenario)

def go_to_scenarios():
  main_form = get_open_form()
  main_form.open_scenarios()

def go_to_finish_scenario(win):
  main_form = get_open_form()
  main_form.setup_active_scenario()
  main_form.open_finish_scenario(win)

def go_to_calendar():
  main_form = get_open_form()
  main_form.open_calendar()

def go_to_outpost():
  main_form = get_open_form()
  main_form.open_outpost()

def setup_active_scenario():
  main_form = get_open_form()
  main_form.setup_active_scenario()
