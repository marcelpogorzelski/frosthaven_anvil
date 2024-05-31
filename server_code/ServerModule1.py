import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def get_character_by_player(name):
  result = app_tables.characters.get(Player=name)
  return result

@anvil.server.callable
def get_classes():
  item_list = []
  for row in app_tables.classes.search():
    item_list.append((row['Name'], row['Name']))
  return item_list
