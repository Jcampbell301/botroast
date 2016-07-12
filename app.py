import flask
import json
from flask import request
import bot
import requests

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	# if request.method == 'POST':
		# bot.post(request.get_json())
		# bot.post('Lorem ipsum')
	return flask.render_template('index.html')

@app.route('/post', methods=['POST'])
def groupme_post():
	if request.method == 'POST':
		bot.post(request.get_data())
	return flask.render_template('index.html')
if __name__ == '__main__':
	app.run(host='0.0.0.0')