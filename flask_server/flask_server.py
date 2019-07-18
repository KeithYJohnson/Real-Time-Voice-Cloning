import flask

from vocoder_caller.vocoder_caller import VocoderCaller


vocoderCaller = VocoderCaller()
app = flask.Flask(__name__)

@app.route('/')
def root_route():
    return 'Welcome'

@app.route('/convert_text_to_celebrity_speech')
def convert_text_to_celebrity_speech():
    text = flask.request.args.get('text')
    celebrity = flask.request.args.get('celebrity')
    vocoderCaller.call_vocoder(text)
    return 'You sent text: {} celebrity: {}'.format(text, celebrity)
