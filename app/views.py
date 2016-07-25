import flask
import json
from flask import request
from bot import Bot
import requests
from flask import flash, redirect
from forms import RegisterForm, AnalyzeForm
from flask_sqlalchemy import SQLAlchemy
from app import models
import analysis as anal
from prettytable import PrettyTable
import time
import datetime
from StringIO import StringIO
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

@app.route('/analyze', methods=['GET', 'POST'])
def get_analysis():
	form = AnalyzeForm()
	
	if form.validate_on_submit():
		flash('Analysis requested for Group_ID="%s"' % (form.group_id.data))
		
		MSG = anal.get_all_msg(acc_tok=form.tok_id.data, gid=form.group_id.data)
		results = anal.get_activity(MSG)
		anal.graph(form.group_id.data, results[0], results[1], results[2], results[3])
		
		df = results[0]
		pt = PrettyTable([''] + list(df.columns))
		for row in df.itertuples():
			pt.add_row(row)
		
		ret = '<pre>'
		ret += 'Analytics of GROUP# ' + str(form.group_id.data) + '<br>'
		ret += 'Requested at ' + datetime.datetime.today().isoformat(' ') + '<br> <br>'
		ret += 'Total Number of Messages: ' + str(df['Message Frequency'].sum()) + '<br>'
		ret += 'Total Number of Words: ' + str(df['Words'].sum()) + '<br>'
		ret += 'Total Likes: ' + str(df['Likes Received'].sum()) + '<br>'
		ret += 'Total Days: ' + str((datetime.datetime.fromtimestamp(MSG[0]['created_at'])-datetime.datetime.fromtimestamp(MSG[-1]['created_at'])).days) + '<br>'
		ret += pt.get_string() + '</pre>'
		ret += '<br>'
		
		like_df = results[4]
		pt = PrettyTable([''] + list(like_df.columns))
		for row in like_df.itertuples():
			pt.add_row(row)
		
		ret += '<pre>' + pt.get_string() + '</pre><br><br>'
		
		ret += '<img src= {{ act_url }}>'
		ret += '<img src={{ m_url }}>'
		ret += '<img src={{ l_url }}>'
		ret += '<img src={{ r_url }}>'
		
		
		file_name = str(form.group_id.data) + '_ANALYTICS.html'
		with open('./app/templates/' + file_name, 'w') as html_file:
			html_file.truncate()
			html_file.write(ret)
	
		# msgstats = str(form.group_id.data) + '_MSG_STATS.png'
		# likestats = str(form.group_id.data) + '_LIKE_STATS.png'
		# ratiostats = str(form.group_id.data) + '_RATIO_STATS.png'
		# actstats = str(form.group_id.data) + '_ACTIVITY_STATS.png'
		
		# m_url = flask.url_for("static", filename=msgstats)
		# act_url = flask.url_for("static", filename=actstats)
		# l_url = flask.url_for("static", filename=likestats)
		# r_url = flask.url_for("static", filename=ratiostats)
		# return flask.render_template(str(form.group_id.data)+'_ANALYTICS.html', m_url=m_url, act_url=act_url, l_url=l_url, r_url=r_url)
		return redirect(flask.url_for('view_analytics', group_id=form.group_id.data))
	return flask.render_template('analytics.html', form=form)
	
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

@app.route('/analytics/<group_id>', methods=['GET'])
def view_analytics(group_id):
	file_name = str(group_id) + '_ANALYTICS.html'
	
	msgstats = str(group_id) + '_MSG_STATS.png'
	likestats = str(group_id) + '_LIKE_STATS.png'
	ratiostats = str(group_id) + '_RATIO_STATS.png'
	actstats = str(group_id) + '_ACTIVITY_STATS.png'
	
	m_url = flask.url_for("static", filename=msgstats)
	act_url = flask.url_for("static", filename=actstats)
	l_url = flask.url_for("static", filename=likestats)
	r_url = flask.url_for("static", filename=ratiostats)
	
	return flask.render_template(str(group_id)+'_ANALYTICS.html', m_url=m_url, act_url=act_url, l_url=l_url, r_url=r_url)