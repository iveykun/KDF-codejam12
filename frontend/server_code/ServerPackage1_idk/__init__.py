import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server package. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def getAudio():
  """Records audio from your local microphone inside a colab notebook
  Returns
  -------
  tuple
    audio (numpy.ndarray), sample rate (int)
  Obs:
  To write this piece of code I took inspiration/code from a lot of places.
  It was late night, so I'm not sure how much I created or just copied o.O
  Here are some of the possible references:
  https://blog.addpipe.com/recording-audio-in-the-browser-using-pure-html5-and-minimal-javascript/
  https://stackoverflow.com/a/18650249
  https://hacks.mozilla.org/2014/06/easy-audio-capture-with-the-mediarecorder-api/
  https://air.ghost.io/recording-to-an-audio-file-using-html5-and-js/
  https://stackoverflow.com/a/49019356
  """

  AUDIO_HTML = """
  <script>
  var my_div = document.createElement("DIV");
  var my_p = document.createElement("P");
  var my_btn = document.createElement("BUTTON");
  var t = document.createTextNode("Press to start recording");
  my_btn.appendChild(t);
  //my_p.appendChild(my_btn);
  my_div.appendChild(my_btn);
  document.body.appendChild(my_div);
  var base64data = 0;
  var reader;
  var recorder, gumStream;
  var recordButton = my_btn;
  var handleSuccess = function(stream) {
    gumStream = stream;
    var options = {
      //bitsPerSecond: 8000, //chrome seems to ignore, always 48k
      mimeType : 'audio/webm;codecs=opus'
      //mimeType : 'audio/webm;codecs=pcm'
    };            
    //recorder = new MediaRecorder(stream, options);
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = function(e) {            
      var url = URL.createObjectURL(e.data);
      var preview = document.createElement('audio');
      preview.controls = true;
      preview.src = url;
      document.body.appendChild(preview);
      reader = new FileReader();
      reader.readAsDataURL(e.data); 
      reader.onloadend = function() {
        base64data = reader.result;
        //console.log("Inside FileReader:" + base64data);
      }
    };
    recorder.start();
    };
  recordButton.innerText = "Recording... press to stop";
  navigator.mediaDevices.getUserMedia({audio: true}).then(handleSuccess);
  function toggleRecording() {
    if (recorder && recorder.state == "recording") {
        recorder.stop();
        gumStream.getAudioTracks()[0].stop();
        recordButton.innerText = "Saving the recording... pls wait!"
    }
  }
  // https://stackoverflow.com/a/951057
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  var data = new Promise(resolve=>{
  //recordButton.addEventListener("click", toggleRecording);
  recordButton.onclick = ()=>{
  toggleRecording()
  sleep(2000).then(() => {
    // wait 2000ms for the data to be available...
    // ideally this should use something like await...
    //console.log("Inside data:" + base64data)
    resolve(base64data.toString())
  });
  }
  });
        
  </script>
  """

  display(HTML(AUDIO_HTML))
  data = eval_js("data")
  binary = b64decode(data.split(',')[1])
  
  process = (ffmpeg
    .input('pipe:0')
    .output('pipe:1', format='wav')
    .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, quiet=True, overwrite_output=True)
  )
  output, err = process.communicate(input=binary)
  
  riff_chunk_size = len(output) - 8
  # Break up the chunk size into four bytes, held in b.
  q = riff_chunk_size
  b = []
  for i in range(4):
      q, r = divmod(q, 256)
      b.append(r)

  # Replace bytes 4:8 in proc.stdout with the actual size of the RIFF chunk.
  riff = output[:4] + bytes(b) + output[8:]

  sr, audio = wav_read(BytesIO(riff))

  return audio, sr

