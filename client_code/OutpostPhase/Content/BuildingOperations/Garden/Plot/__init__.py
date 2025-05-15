from ._anvil_designer import PlotTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Planting import Planting

class Plot(PlotTemplate):
  def __init__(self, gamestate, plot_number, plant, harvest, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.herb = gamestate[plot_number]
    self.gamestate = gamestate
    self.plot_number = plot_number
    self.plant = plant
    self.harvest = harvest
    self.herb_images = {
      'Arrowvine': '_/theme/garden/arrowvine-plot.png',
      'Axenut': '_/theme/garden/axenut-plot.png',
      'Corpsecap': '_/theme/garden/corpsecap-plot.png',
      'Flamefruit': '_/theme/garden/flamefruit-plot.png',
      'Rockroot': '_/theme/garden/rockroot-plot.png',
      'Snowthistle': '_/theme/garden/snowthistle-plot.png',
    }

    self.plot_image.source = self.herb_images.get(self.herb, '_/theme/garden/empty-plot.png')

    if self.plant:
      self.plant_button.visible = True

    if not self.harvest:
      self.plant_button.enabled = True


  def plant_button_click(self, **event_args):
    frosthaven = app_tables.frosthaven.search()[0]
    
    planted_herb = alert(content=Planting(frosthaven), title='Planting', large=True, dismissible=False, buttons=[('Cancel', None)])
    if not planted_herb:
      return
    self.plant_button.enabled = False
    self.herb = planted_herb
    self.gamestate[self.plot_number] = planted_herb
    frosthaven[planted_herb] -= 1
    self.plot_image.source = self.herb_images.get(self.herb, '_/theme/garden/empty-plot.png')
    