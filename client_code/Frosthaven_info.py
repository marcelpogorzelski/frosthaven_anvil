import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#https://github.com/cmlenius/gloomhaven-card-browser/blob/main/data/scripts/characters.js

class_names = {
  "Blinkblade": { 'id': "BB", 'name': "Blinkblade" },
  "Bannerspear": { 'id': "BN", 'name': "Banner Spear"},
  "Boneshaper": { 'id': "BO", 'name': "Boneshaper"},
  "Drifter": { 'id': "DF", 'name': "Drifter" },
  "Deathwalker": { 'id': "DW", 'name': "Deathwalker" },
  "Geminate": { 'id': "GE", 'name': "Geminate" },
  "Coral": { 'id': "CR", 'name': "Crashing Tide"},
  "Kelp": { 'id': "DT", 'name': "Deepwraith"},
  "Fist": { 'id': "FF", 'name': "Frozen Fist"},
  "Prism": { 'id': "HV", 'name': "Hive"},
  "Astral": { 'id': "IF", 'name': "Infuser"},
  "Drill": { 'id': "ME", 'name': "Metal Mosaic"},
  "Shackles": { 'id': "PC", 'name': "Pain Conduit"},
  "Meteor": { 'id': "PY", 'name': "Pyroclast"} ,
  "Snowflake": { 'id': "SD", 'name': "Snowdancer"},
  "Shards": { 'id': "SH", 'name': "Shattersong"},
  "Trap": { 'id': "TA", 'name': "Trapper"}
}