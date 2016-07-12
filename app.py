import flask
import json
from flask import request
import bot

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		bot.post(request.get_json())
	return flask.render_template('index.html')
	
if __name__ == '__main__':
	app.run(host='0.0.0.0')