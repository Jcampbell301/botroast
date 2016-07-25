import requests
import json
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from StringIO import StringIO
import prettytable    

global ACCESS_TOKEN	
global GROUP_ID
global MSG

URL = 'https://api.groupme.com/v3/'

ACCESS_TOKEN = ''
GROUP_ID = -1

def get_all_msg(acc_tok=ACCESS_TOKEN, gid=GROUP_ID):
	# First pass
	r = requests.get(URL + 'groups/' + str(gid) + '/messages?token=' + acc_tok + '&limit=100')
	MSG = r.json()['response']['messages']

	last_msg = MSG[-1]
	last_msg_id = last_msg['id']
	
	r = requests.get(URL + 'groups/' + str(gid) + '/messages?token=' + acc_tok + '&limit=100&before_id=' + str(last_msg_id))
	while r.status_code != 304:
		MSG = MSG + r.json()['response']['messages']

		last_msg = MSG[-1]
		last_msg_id = last_msg['id']
		r = requests.get(URL + 'groups/' + str(gid) + '/messages?token=' + acc_tok + '&limit=100&before_id=' + str(last_msg_id))
	return MSG

def get_activity(MSG):
	freq = {}
	num_words = {}
	name_id = {}
	got_like = {}
	gave_like = {}
	max_day = {}
	user_liked_by = {}
	user_liked = {}
	month = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
	hour = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0}
	day = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
	
	curr_date = datetime.datetime.fromtimestamp(MSG[0]['created_at'])
	msg_counter = {}
	max_msg = {}
	
	for msg in MSG:
		msg_date = datetime.datetime.fromtimestamp(msg['created_at'])
		month[msg_date.month] += 1
		hour[msg_date.hour] += 1
		day[msg_date.isoweekday()] += 1
		
		#Messages from previous day before curr_date (since traversing backward) => Must update max and reset activity counters for each member
		if msg_date.date() < curr_date.date():
			for member in max_msg.keys():
				if msg_counter[member] > max_msg[member]:
					max_day[member] = curr_date.date()
					max_msg[member] = msg_counter[member]
			for member in msg_counter.keys():
				msg_counter[member] = 1
			curr_date = msg_date
				
		# First post by a user. Need to initialize user into stat dictionaries
		if msg['user_id'] not in freq.keys():
			freq[msg['user_id']] = 1
			name_id[msg['user_id']] = msg['name']
			num_words[msg['user_id']] = 0
			max_day[msg['user_id']] = curr_date.date()
			msg_counter[msg['user_id']] = 1
			max_msg[msg['user_id']] = 1
			user_liked[msg['user_id']] = {}
			user_liked_by[msg['user_id']] = {}
			
			if msg['text'] is not None:
				num_words[msg['user_id']] = msg['text'].count(' ')+1 
			
			got_like[msg['user_id']] = len(msg['favorited_by'])
			
			for user in msg['favorited_by']:
				user_liked_by[msg['user_id']] = {user:1}
				if user not in user_liked.keys():
					user_liked[user] = {msg['user_id']:1}
				else:
					user_liked[user][msg['user_id']] = 1
			
			
			for id in msg['favorited_by']:
				if id not in gave_like.keys():
					gave_like[id] = 1
				else:
					gave_like[id] += 1
		else: # This user has posted before. Only need to update and not initialize 
			freq[msg['user_id']] += 1
			if msg['text'] is not None:
				num_words[msg['user_id']] += (msg['text'].count(' ')+1)
			
			got_like[msg['user_id']] += len(msg['favorited_by'])
			msg_counter[msg['user_id']] += 1
			
			for id in msg['favorited_by']:
				if id not in gave_like.keys():
					gave_like[id] = 1
					user_liked_by[msg['user_id']][id] = 1
					user_liked[id] = {msg['user_id']:1}
				else:
					gave_like[id] += 1
					if id not in user_liked_by[msg['user_id']].keys():
						user_liked_by[msg['user_id']][id] = 0
					user_liked_by[msg['user_id']][id] += 1
					if msg['user_id'] not in user_liked[id].keys():
						user_liked[id][msg['user_id']] = 0
					user_liked[id][msg['user_id']] += 1
	
	# Find max in user_liked and user_liked_by
	max_liked = {}
	for alper in user_liked.keys():
		max_liked[alper] = 'None'
		if len(user_liked[alper]) > 0:
			fvt = max(user_liked[alper], key=user_liked[alper].get)
			max_liked[alper] = name_id[fvt] + ' - ' + str(user_liked[alper][fvt])
			
	max_liked_by = {}
	for gracie in user_liked_by.keys():
		max_liked_by[gracie] = 'None'
		if len(user_liked_by[gracie]) > 0:
			fvt = max(user_liked_by[gracie], key=user_liked_by[gracie].get)
			max_liked_by[gracie] = name_id[fvt] + ' - ' + str(user_liked_by[gracie][fvt])
	
	activity_df = pd.DataFrame([name_id, freq, num_words, got_like, gave_like, max_day, max_msg]).T
	activity_df.columns = ['Member', 'Message Frequency', 'Words', 'Likes Received', 'Likes Given', 'Day of Maximum Activity', 'Max Messages Sent in 1 Day']
	activity_df['Words per Message'] = activity_df['Words'].divide(activity_df['Message Frequency'])
	activity_df['Likes per Message'] = activity_df['Likes Received'].divide(activity_df['Message Frequency'])
	activity_df['Likes Received to Likes Given'] = activity_df['Likes Received'].divide(activity_df['Likes Given'])
	
	like_df = pd.DataFrame([name_id]).T
	like_df.columns = ['Member']
	like_df = pd.DataFrame([name_id, max_liked_by, max_liked]).T
	like_df.columns = ['Member', 'Liked Most By', 'Likes Most']
	
	return [activity_df, month, hour, day, like_df]

def graph(gid, activity_df, month_act, hours_act, day_act):	
	plt.figure(1)
	f, ax = plt.subplots(1, 2)
	
	activity_df.plot(kind='bar', x='Member', y='Message Frequency', colormap='Set2', legend=False, ax=ax[0])
	ax[0].set_ylabel('Message Frequency')
	ax[0].set_title('Message Frequency')
	
	activity_df.plot(kind='bar', x='Member', y='Words per Message', colormap='Set2', legend=False, ax=ax[1])
	ax[1].set_ylabel('Words per Message')
	ax[1].set_title('Words per Message')
	
	plt.tight_layout()
	plt.savefig('./app/static/' + str(gid) + '_MSG_STATS.png')
	
	plt.figure(2)
	f2, ax2 = plt.subplots(1, 2)
	
	activity_df.plot(kind='bar', x='Member', y='Likes Received', colormap='Set2', legend=False, ax=ax2[0])
	ax2[0].set_ylabel('Likes Received')
	ax2[0].set_title('Likes Received')
	
	
	activity_df.plot(kind='bar', x='Member', y='Likes Given', colormap='Set2', legend=False, ax=ax2[1])
	ax2[1].set_ylabel('Likes Given')
	ax2[1].set_title('Likes Given')
	
	plt.tight_layout()
	plt.savefig('./app/static/' + str(gid) + '_LIKE_STATS.png')
	
	plt.figure(3)
	f3, ax3 = plt.subplots(1, 2)
	
	activity_df.plot(kind='bar', x='Member', y='Likes per Message', colormap='Set2', legend=False, ax=ax3[0])
	ax3[0].set_ylabel('Likes per Message')
	ax3[0].set_title('Likes per Message')
	
	activity_df.plot(kind='bar', x='Member', y='Likes Received to Likes Given', colormap='Set2', legend=False, ax=ax3[1])
	ax3[1].set_ylabel('Likes Received to Likes Given')
	ax3[1].set_title('Likes Received to Likes Given Ratio')
	
	#plt.show()
	
	plt.tight_layout()
	plt.savefig('./app/static/' + str(gid) + '_RATIO_STATS.png')
	
	plt.figure(4)
	f4, ax4 = plt.subplots(3)

	ax4[0].plot(month_act.keys(), month_act.values())
	ax4[0].set_xlabel('Month')
	ax4[0].set_ylabel('Activity (Messages)')
	ax4[0].set_xticks(range(1, 13))
	
	ax4[1].plot(hours_act.keys(), hours_act.values())
	ax4[1].set_xlabel('Hour of the Day')
	ax4[1].set_ylabel('Activity (Messages)')
	ax4[1].set_xticks(range(24))
	
	ax4[2].plot(day_act.keys(), day_act.values())
	ax4[2].set_xlabel('Day of the Week')
	ax4[2].set_ylabel('Activity (Messages)')
	ax4[2].set_xticks(range(1, 8))
	ax4[2].set_xticklabels(['M', 'T', 'W', 'R', 'F', 'S', 'U'])
	
	plt.tight_layout()
	plt.savefig('./app/static/' + str(gid) + '_ACTIVITY_STATS.png')

# if __name__ == '__main__':
	# parser = argparse.ArgumentParser(description = 'Conducts stastical analysis on a GroupMe Group Chat.')
	# parser.add_argument('acc_tok', type=str, help = 'Must pass a valid access token generated by GroupMe.')
	# parser.add_argument('gid', type=int, help = 'Must pass a valid group id of a group which you are currently a member of. Can be found under Settings of a Group in GroupMe.')
	# arg = parser.parse_args()
	
	# ACCESS_TOKEN = arg.acc_tok
	# GROUP_ID = arg.gid
	# MSG = get_all_msg(acc_tok=ACCESS_TOKEN, gid=GROUP_ID)
	# results = get_activity(MSG)
	# print(results[0])
	# print(results[1])
	# print(results[2])
	# print(results[3])