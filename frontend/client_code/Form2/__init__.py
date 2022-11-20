from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q

from anvil.tables import app_tables
from anvil.js.window import navigator, MediaRecorder, Audio,Blob,URL

from tailor_maid import Module1

class Form2(Form2Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.rich_text_2.content = anvil.server.call('get_weather')
    self.audio_chunks=[]
    self.recorder=None
    self.is_recording = False
    
    self.image_link = ""
    self.drop_down_1.items = [r['skin tone'] for r in app_tables.table_0.search()]
    self.drop_down_2.items = [r['clothing style'] for r in app_tables.table_1.search()]

    # Any code you write here will run when the form opens.
    

  def button_3_click(self, **event_args):
    """top sidebar button"""
    open_form("Form1")

  def button_4_click(self, **event_args):
    """bottom sidebar button"""
    open_form("Form2")

  def button_2_click(self, **event_args):
      if not self.is_recording:
            self.is_recording = True
            self.button_2.text='Stop Recording'
            self.audio_chunks=[]
            stream=navigator.mediaDevices.getUserMedia({'audio': True})
            self.recorder = MediaRecorder(stream)
            self.recorder.start()
            self.recorder.ondataavailable=self.save_audio
      else:
          self.recorder.stop()
          self.button_2.text = 'Voice Command'
          self.is_recording = False
            
  def save_audio(self,e):
        self.audio_chunks.append(e.data)
        js_blob=Blob(self.audio_chunks)
        # Ignore the content_type, anvil is retarded
        anvil_blob = anvil.js.to_media(js_blob,content_type='audio/wav',name='Audio.wav')
        print(anvil_blob.content_type)
        out, image_url = anvil.server.call('get_command', anvil_blob)
        print(out)
        print(image_url)
        
        self.image_1.source = image_url
        # no longer needed, use for verification purposes
        # download(anvil_blob)
    # anvil.server.call('getAudio')

  def set_image(self, url):
      self.image_1.source = url

  def button_1_click(self, **event_args):
    """suggest outfit button"""
    out, image_url = anvil.server.call('generate_image', self.drop_down_1.selected_value, self.drop_down_2.selected_value)
    self.image_1.source = image_url

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    anvil.server.call('change_skintone', self.drop_down_1.selected_value)
  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    anvil.server.call('change_style', self.drop_down_2.selected_value)


