import requests
import json
import time
import analysis as anal

class Bot:
	'GroupMe Bot that does a lot of things. Dope af.'
	# BOT_ID = '6c059ca743bdf06151f0e4ef6c'
	POST_URL = 'https://api.groupme.com/v3/bots/post/'
	CMDS = ['!help', '!burn', '!since', '!history', '!spell', '!roast', '!add_roast', '!impersonate', '!mood']
	HELP = "Hello, I'm a bot. I do things. Here are some things I do.\n!help - List commands.\n!burn - Post the addresses for the Wikipedia List of Burn Centers and UChicago Burn Center.\n!since <String> - Return time since the last instance of the given <String>.\n!history - Return analysis of this group's history.\n!spell <user> - Check/Correct spelling of given <user> last message.\n!roast - Returns random roast from list. May implement personal roasts in the future.\n!add_roast <String> - Adds <String> to roast list.\n!impersonate <user> - Quotes something substantial <user> has said in the past.\n!mood <user> - Returns mood/sentiment of <user> last message."
	
	def __init__(self, BOT_ID, ACCESS_TOKEN, GROUP_ID):
		self.BOT_ID = BOT_ID
		self.ACCESS_TOKEN = ACCESS_TOKEN
		self.GROUP_ID = GROUP_ID
		
		self.MSG = anal.get_all_msg(self.ACCESS_TOKEN, self.GROUP_ID)
		results = anal.get_activity(self.MSG)
		self.DF = results[0]
		self.DATA_MONTH = results[1]
		self.DATA_HOURS = results[2]
		
	def post(self, msg):
		r = requests.post(POST_URL, data={"bot_id": self.BOT_ID, "text": msg})
		return r.text
	
	def burn(self):
		return "https://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_States\nhttp://www.uchospitals.edu/specialties/burn-center/"
			
	def respond(self, msg):
		cmd = msg.split()[0]
		resp = 'Cool cool.'
		if cmd not in CMDS:
			resp = 'Invalid command. !help for help'
		elif cmd == '!help':
			resp = HELP
		elif cmd == '!burn':
			resp = self.burn()
		requests.post(POST_URL, data={'bot_id': self.BOT_ID, "text": resp})