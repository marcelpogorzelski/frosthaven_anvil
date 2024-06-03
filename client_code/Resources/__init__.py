from ._anvil_designer import ResourcesTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Resources(ResourcesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.character_repeating_panel.items = app_tables.characters.search()
    self.frosthaven_data_row_panel.item = app_tables.frosthaven.search()[0]
    self.total_data_row_panel.item = self.get_resources()

  def get_resources(self):
    characters = app_tables.characters.search()
    frosthaven = app_tables.frosthaven.search()[0]

    total_resources = {'Name': 'Total', 'Gold': 0, 'Lumber': 0, 'Metal': 0, 'Hide': 0, 'Arrowvine': 0, 'Axenut': 0, 'Corpsecap': 0, 'Flamefruit': 0, 'Rockroot': 0, 'Snowthistle': 0}
    for resource in characters:
      total_resources['Gold'] += resource['Gold']
      total_resources['Lumber'] += resource['Lumber']
      total_resources['Metal'] += resource['Metal']
      total_resources['Hide'] += resource['Hide']
      total_resources['Arrowvine'] += resource['Arrowvine']
      total_resources['Axenut'] += resource['Axenut']
      total_resources['Corpsecap'] += resource['Corpsecap']
      total_resources['Flamefruit'] += resource['Flamefruit']
      total_resources['Rockroot'] += resource['Rockroot']
      total_resources['Snowthistle'] += resource['Snowthistle']

    
    total_resources['Gold'] += frosthaven['Gold']
    total_resources['Lumber'] += frosthaven['Lumber']
    total_resources['Metal'] += frosthaven['Metal']
    total_resources['Hide'] += frosthaven['Hide']
    total_resources['Arrowvine'] += frosthaven['Arrowvine']
    total_resources['Axenut'] += frosthaven['Axenut']
    total_resources['Corpsecap'] += frosthaven['Corpsecap']
    total_resources['Flamefruit'] += frosthaven['Flamefruit']
    total_resources['Rockroot'] += frosthaven['Rockroot']
    total_resources['Snowthistle'] += frosthaven['Snowthistle']
      
    #resources.append(total_resources)
    
    return total_resources



  
        
    
    

    # Any code you write here will run before the form opens.
