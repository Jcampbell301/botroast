from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
import requests

class RegisterForm(Form):
	bot_id = StringField('bot_id', validators=[DataRequired()])
	tok_id = StringField('tok_id', validators=[DataRequired()])
	group_id = StringField('group_id', validators=[DataRequired()])
	
	def validate(self):
		print('Trying to validate')
		r = requests.get("https://api.groupme.com/v3/bots?token=" + str(self.tok_id.data))
		print(r)
		resp = r.json()
		print(resp)
		print(resp['meta']['code'])
		if resp['meta']['code'] != 200:
			print 'wee'
			print self.errors
			self.errors['tok_id'] = 'Invalid Access Token'
			print 'not working'
			return False
		
		found = False
		for bot in resp['response']:
			if self.bot_id.data == bot['bot_id'] and self.group_id.data != bot['group_id']:
				self.errors['group_id'] = 'This bot does not belong to inputted group.'
				return False
			elif self.bot_id.data == bot['bot_id'] and self.group_id.data == bot['group_id']:
				found = True
				break
		if not found:
			self.errors['bot_id'] = 'Invalid Bot ID'
			return False
		return True