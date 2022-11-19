from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Form1")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Form2")


