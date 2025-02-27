import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#

class_names = { 
  "Blinkblade": { 'id': "BB", 'name': "Blinkblade" },
  "Bannerspear": { 'id': "BN", 'name': "Banner Spear"},
  "Boneshaper": { 'id': "BO", 'name': "Boneshaper"},
  "Drifter": { 'id': "DF", 'name': "Drifter" },
  "Deathwalker": { 'id': "DW", 'name': "Deathwalker" },
  "Geminate": { 'id': "GE", 'name': "Geminate" },
  "Coral": { 'id': "CR", 'name': "Crashing Tide", 'altName': "Coral" },
  "Kelp": { 'id': "DT", 'name': "Deepwraith", 'altName': "Kelp" },
  "Fist": { 'id': "FF", 'name': "Frozen Fist", 'altName': "Fist" },
  "Prism": { 'id': "HV", 'name': "Hive", 'altName': "Prism" },
  "Astral": { 'id': "IF", 'name': "Infuser", 'altName': "Astral" },
  "Drill": { 'id': "ME", 'name': "Metal Mosaic", 'altName': "Drill" },
  "Shackles": { 'id': "PC", 'name': "Pain Conduit", 'altName': "Shackles" },
  "Meteor": { 'id': "PY", 'name': "Pyroclast", 'altName': "Meteor" },
  "Snowflake": { 'id': "SD", 'name': "Snowdancer", 'altName': "Snowflake" },
  "Shards": { 'id': "SH", 'name': "Shattersong", 'altName': "Shards" },
  "Trap": { 'id': "TA", 'name': "Trapper", 'altName': "Trap" },
}

def say_hello():
  print("Hello, world")
