import flask
import json
from flask import request
from .bot import Bot
import requests

app = flask.Flask(__name__)
artoo = Bot('6c059ca743bdf06151f0e4ef6c')

@app.route('/', methods=['GET', 'POST'])
def index():
	return flask.render_template('index.html')

@app.route('/post', methods=['POST'])
def ping():
	if request.method == 'POST':
		msg = request.get_data()['text']
		if msg.split()[0][0] == '!': #Msg is a command
			artoo.respond(msg)
			
	return flask.render_template('index.html')
	
if __name__ == '__main__':
	app.run(host='0.0.0.0')