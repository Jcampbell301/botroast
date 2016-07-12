import requests
import json
import time

BOT_ID = '6c059ca743bdf06151f0e4ef6c'
URL = 'https://api.groupme.com/v3/'
POST_URL ='https://api.groupme.com/v3/bots/post/'

def post(msg):
	r = requests.post(POST_URL, data={"bot_id": BOT_ID, "text": msg})
	return r.text