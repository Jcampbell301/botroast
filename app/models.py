from app import db

class User(db.Model):
	bot_id = db.Column(db.String(120), primary_key=True)
	acc_tok = db.Column(db.String(120), index=True)
	group_id = db.Column(db.Integer)
	
	def __repr__(self):
		return '<BOT ID %r>' % (self.bot_id)
	
	