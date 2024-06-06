from ._anvil_designer import CalendarTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Utilites


class Calendar(CalendarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.calendar_repeating_panel.items = app_tables.calendar.search(tables.order_by('Week'))

    current_week = app_tables.calendar.search(tables.order_by('Week'),Finished=False)[0]['Week']
    current_page = int((current_week-1)/10)
    self.calendar_data_grid.set_page(current_page)
