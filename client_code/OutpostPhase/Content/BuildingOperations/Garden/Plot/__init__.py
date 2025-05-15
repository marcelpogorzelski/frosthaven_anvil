from ._anvil_designer import PlotTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Plot(PlotTemplate):
  def __init__(self, herb, plant, harvest, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.herb = herb
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
    #_/theme/garden/arrowvine-plot.png

    # Any code you write here will run before the form opens.

  def plant_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
