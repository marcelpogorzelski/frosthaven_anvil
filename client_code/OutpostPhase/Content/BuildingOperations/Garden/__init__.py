from ._anvil_designer import GardenTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Plot import Plot
from .....Utilites import windowWidthWithMax


class Garden(GardenTemplate):
  def __init__(self, gamestate, finish_phase_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.finish_phase_tag = finish_phase_tag
    self.gamestate = gamestate

    self.finished = gamestate[finish_phase_tag]

    self.garden_level = self.gamestate['GardenBuilding']['CurrentBuilding']['Level']
    #self.garden_level = 4

    self.check_harvest_and_plant()
    self.add_plots()

    if self.finished:
      self.disable_phase()

  def check_harvest_and_plant(self):
    if self.garden_level >= 3:
      self.harvest = True
      self.plant = True
    else:
      self.harvest = self.gamestate['GardenHarvest']
      self.plant = not self.harvest

    if self.plant:
      self.finished_planting_button.enabled = True
    if self.harvest:
      self.harvest_button.enabled = True
      self.finished_planting_button.enabled = False

  def add_plot(self, plot_number):
    plot = Plot(self.gamestate, plot_number, self.plant, self.harvest)
    self.plots.append(plot)
    self.plot_flow_panel.add_component(plot, width=self.plot_width)
    
  def add_plots(self):
    self.plot_width, _ = windowWidthWithMax(maxWidth=800)
    self.plot_width = self.plot_width/3
    self.plots = list()
    if self.garden_level >= 1:
      self.add_plot('GardenPlot1')
    if self.garden_level >= 2:
      self.add_plot('GardenPlot2')
    if self.garden_level == 4:
      self.add_plot('GardenPlot3')

  def disable_phase(self):
    self.garden_column_panel.background = 'theme:Outline'
    self.harvest_button.enabled = False
    self.toggle_plant_buttons(False)
    self.plot_flow_panel.visible = False
    self.button_flow_panel.visible = False
    self.name_label.text += " - Finished"

  def set_as_finished(self):
    self.disable_phase()
    self.finished = True
    self.gamestate[self.finish_phase_tag] = True
    self.raise_event('x-building-finished')

  def toggle_plant_buttons(self, toggle):
    self.finished_planting_button.enabled = toggle
    for plot in self.plots:
      plot.plant_button.enabled = toggle

  def harvest_button_click(self, **event_args):
    self.harvest_button.enabled = False
    frosthaven = app_tables.frosthaven.search()[0]

    for plot in self.plots:
      if not plot.herb:
        continue
      frosthaven[plot.herb] += 1

    if not self.plant:
      self.set_as_finished()
    else:
      self.toggle_plant_buttons(True)

  def finished_planting_button_click(self, **event_args):
    self.toggle_plant_buttons(False)
    self.set_as_finished()

    
    

  
