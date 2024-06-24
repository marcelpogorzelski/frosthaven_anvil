from ._anvil_designer import CalendarRowTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CalendarRowTemplate(CalendarRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def get_calendar_background(self, week, finished):
    if finished:
      return 'theme:On Disabled'
    if ((week - 1) // 10 + 1) % 2:
      return '#FFFFAD'
    else:
      return '#ADD8E6'

  def finished_check_box_change(self, **event_args):
    calendar_row = event_args['sender'].parent
    current_week = calendar_row.item['Week']
    if not event_args['sender'].checked:
      next_week = app_tables.calendar.get(Week=current_week+1)
      if next_week['Finished']:
        event_args['sender'].checked = True
        calendar_row.item['Finished'] = True
        calendar_row.item.update()
        
    else:
      previous_week = app_tables.calendar.get(Week=current_week-1)
      if not previous_week['Finished']:
        event_args['sender'].checked = False
        calendar_row.item['Finished'] = False
        calendar_row.item.update()
        
    calendar_row.background = self.get_calendar_background(current_week, event_args['sender'].checked)
