import flask
import json
from flask import request

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		print('TRIED TO POST')
		print(request.form)
	else:
		print('TRIED TO GET')
	return flask.render_template("index.html")

@app.route('/post', methods=['GET', 'POST'])
def post():
	if request.method == 'POST':
		print('TRIED TO POST')
		print(request.form)
	else:
		print('TRIED TO GET')
	
	return flask.render_template("index.html")
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)