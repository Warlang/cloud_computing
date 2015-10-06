from flask import Flask
import json
import subprocess
import sys
import time

#special for celery
from celery import Celery

app = Celery('tweets_read_v4', backend='amqp', broker='amqp://')
#end of special

#	--- Attributes ---
fname = 'tweets_16.txt'
f = open(fname) #Open file stream
list_of_words = ['han','hon','den','det','denna','denne','hen'] #List of words to check for
counters = {'han':0 , 'hon': 0, 'den':0, 'det':0, 'denna':0, 'denne':0, 'hen':0} #Count each words in 
result = None#Just to have it global
nr_cores = 1 #Change if you gonna use more cores
nr_splits = 0 #part of splits thats been done
#Checks the lenght of a file!
file_array = f.readlines() #read in the file
file_len = len(file_array)
#print len(file_array)

#	--- Functions ---
#start the counting
def start():
	status = False

	while (nr_cores != nr_splits):
		doSplit()
		status = doPart.delay(nr_splits)


@app.task
def getStatus():
	if(result == None):
		return False
	return True

@app.task
def getResult():
	return result



#getPart return value to show which split you will get
#Side effect update nr of splits made and we will do same amount of splits as num of cores.
def doSplit():
	global nr_splits
	nr_splits = nr_splits + 1

#TODO put it in thir own "part" result list
#Count words in a part of the file. 
#Return which part they had
@app.task
def doPart(partToDo):
	start_index = ((file_len/nr_cores) * (partToDo-1))
	stop_index = ((file_len/nr_cores) * partToDo)
	if(partToDo == nr_cores):
		stop_index = file_len
	countWords(getText(start_index,stop_index))
	return partToDo




#getText: Get the text from the file that is gonna be checked from n lines.
#Arguements: start - is where you want to start check for text in the array and stop is where you end.
#			must be start < stop
def getText(start, stop):
	text = " "
	skipRow = False
	if(file_array[start]=='\n'):
		skipRow = True
	i = start
	while (i < stop):
		row = file_array[i]
		if (skipRow):
			skipRow = False
		else:
			skipRow = True
			json_obj = json.loads(row)		
			if (validText(json_obj)):
				text = text + json_obj['text']
		i = i + 1
	return text

#validText: Check if the text should be counter or if its a retweet of an old one
#Arguments: text - must be json object of correct type
#return true if text is valid. False otherwise
def validText(text):
	#'retweeted_status' if that exist in the json object its a retweet otherwiese not
	if ('retweeted_status' not in text):
		return True 
	else:
		return False

#countWords: Count and update list_of_words depending of the occurence of words
#Arguments: text - string of text that should be counted
#side effect: Update counters
def countWords(text):
	global counters
	for word in list_of_words:
		n = text.count(word)
		counters[word] = counters.get(word) + n
	global result
	result = json.dumps(counters) #TODO fix so it can be multiple results list to check to nr of cores.
	


#REST API
app = Flask(__name__)


@app.route('/result', methods=['GET'])
def getCounters():
	return getResult()

@app.route('/start', methods=['GET'])
def doStart():
	start()

@app.route('/status', methods=['GET'])
def doGetStatus():
	return getStatus()

	

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)