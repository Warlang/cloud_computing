from celery import Celery
import sys
import os
import json
import urllib2


app = Celery('tasks', backend='amqp', broker='amqp://')


	

@app.task
def oneFileCounts(fname):
	print fname + " is running."
	text = getText(fname)
	counters = countWords(text)
	print "Results been completed for: " + fname
	return counters

def validText(text):
	#'retweeted_status' if that exist in the json object its a retweet otherwiese not
	if ('retweeted_status' not in text):
		return True 
	else:
		return False


def countWords(text):
	counters = {'han':0 , 'hon': 0, 'den':0, 'det':0, 'denna':0, 'denne':0, 'hen':0} #Count each words in
	list_of_words = ['han','hon','den','det','denna','denne','hen'] #List of words to check for 
	for word in list_of_words:
		n = text.count(word)
		counters[word] = counters.get(word) + n
	return counters


def getText(fname):
	text = " "
	skipRow = False
	for row in urllib2.urlopen(fname):
		if (skipRow):
			skipRow = False
		else:
			skipRow = True
			json_obj = json.loads(row)		
			if (validText(json_obj)):
				text = text + json_obj['text']
		status()#Can remove this if program works
	return text


# --- PRINT STATUS HELPER ---
status_helper = 0
def status()
	status_helper = status_helper + 1
	if(status_helper > 5000):
		status_helper = 0
		print "5000 have been noticed"