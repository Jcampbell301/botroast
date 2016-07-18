import flask
import json
from flask import request
from bot import Bot
import requests
from flask import flash, redirect
from forms import RegisterForm
from flask_sqlalchemy import SQLAlchemy
from app import models

from app import app
from app import db

@app.route('/', methods=['GET', 'POST'])
def index():
	return flask.render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		flash('Login requested for Bot_ID="%s"' % (form.bot_id.data))
		
		users = models.User.query.all()
		present = False
		for u in users:
			# If this bot_id is already in db, update with new information
			if u.bot_id == form.bot_id.data:
				u.acc_tok = form.tok_id.data
				u.group_id = form.group_id.data
				present = True
				
		if not present: # Else, create new user in db
				new_user = models.User(bot_id=form.bot_id.data, acc_tok=form.tok_id.data, group_id=int(form.group_id.data))
				db.session.add(new_user)
				db.session.commit()
				
		return "Registration Succesful!"
	return flask.render_template('register.html', form=form)
	
@app.route('/callback/<bot_id>', methods=['POST'])
def callback(bot_id):
	req_bot = models.User.query.get(bot_id)
	tmp_bot = Bot(req_bot.bot_id, req_bot.acc_tok, req_bot.group_id)
	if request.method == 'POST':
		mreq = json.loads(request.get_data())
		msg = mreq['text']
		
		if msg.split()[0][0] == '!': #Msg is a command
			tmp_bot.respond(msg)
			
	return flask.render_template('index.html')