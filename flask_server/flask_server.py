import flask

from celebrity_text_request_handler.celebrity_text_request_handler import CelebrityTextRequestHandler


requestHandler = CelebrityTextRequestHandler()
app = flask.Flask(__name__)

@app.route('/')
def root_route():
    return 'Welcome'

@app.route('/convert_text_to_celebrity_speech')
def convert_text_to_celebrity_speech():
    text = flask.request.args.get('text')
    celebrity = flask.request.args.get('celebrity')
    try:
    	requestHandler.handle(text, celebrity)
    except ValueError as e:
        print(e)
		return "ERROR"
    return 'You sent text: {} celebrity: {}'.format(text, celebrity)
