import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import URLMedia
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

#=IFS(C2<45,1,C2<95,2,C2<150,3,C2<210,4,C2<275,5,C2<345,6,C2<420,7,C2<500,8,C2>=500,9)
def get_level(experience):
  level = 0
  if experience < 45:
    level = 1
  elif experience < 95:
    level = 2
  elif experience < 150:
    level = 3
  elif experience < 210:
    level = 4
  elif experience < 275:
    level = 5
  elif experience < 345:
    level = 6
  elif experience < 420:
    level = 7
  elif experience < 500:
    level = 8
  elif experience >= 500:
    level = 9

  return level

#def get_resources_image():
  #lumber_image = URLMedia("_/theme/resource_images/fh-lumber-bw-icon.png")
  #thumb_lumber_image = anvil.image.generate_thumbnail(lumber_image, 120)
  #return lumber_image

#=ifs(B17<3, -10, B17<5,-5, B17<8,0,B17<11,5,B17<14,10, B17>=14,15)+B18
def get_total_defense(moral, defense):
  moral_defense = 0
  if moral < 3:
    moral_defense = -10
  if moral < 5:
    moral_defense = -5
  elif moral < 8:
    moral_defense = 0
  elif moral < 11:
    moral_defense = 5
  elif moral < 14:
    moral_defense = 10
  elif moral >= 14:
    moral_defense = 15
  
  return moral_defense + defense