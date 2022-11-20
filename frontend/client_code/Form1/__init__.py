from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.drop_down_1.items = [r['skin tone'] for r in app_tables.table_0.search()]
    self.drop_down_2.items = [r['clothing style'] for r in app_tables.table_1.search()]

    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
      """This is add to databse """
      # Call the google colab function and pass it the iris measurements
      color, response, percentage = anvil.server.call('imagenet1kmedia', self.image_1.source)
      alert(f"{color} colored {response} has been added to database!")


  def file_loader_1_change(self, file, **event_args):
    """This is upload FileLoader"""
    #alert(file.url)
    #response, percentage = anvil.server.call('imagenet1kmedia', file)
    self.image_1.source = file
    self.button_2.enabled = True
    self.file_loader_1.enabled = False
    #alert(response)

  def button_2_click(self, **event_args):
    """This is the delete button"""
    self.file_loader_1.clear()
    self.file_loader_1.enabled = True
    self.button_2.enabled = False
    self.image_1.source = None

  def button_3_click(self, **event_args):
    """This is first sidebar button"""
    open_form("Form1")

  def button_4_click(self, **event_args):
    """This second sidebar button"""
    open_form("Form2")

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    anvil.server.call('change_skintone', self.drop_down_1.selected_value)

  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    anvil.server.call('change_style', self.drop_down_2.selected_value)






