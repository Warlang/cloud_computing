from flask import Flask
import json
import subprocess
import sys
import time
import urllib2
from tasks import oneFileCounts


#	--- Attributes ---
final_result = None
parts_result = []


#	--- Functions ---
def main():
	num_files = 19
	url = "http://smog.uppmax.uu.se:8080/swift/v1/tweets/tweets_"
	#loop 0-19 to queue tasks
	for i in range(0, num_files+1):
		part = oneFileCounts.delay(url + str(i))
		parts_result.append(part)





def combineResults():
	counters = {'han':0 , 'hon': 0, 'den':0, 'det':0, 'denna':0, 'denne':0, 'hen':0} #Count each words in
	list_of_words = ['han','hon','den','det','denna','denne','hen'] #List of words to check for 
	for element in parts_result:
		if (element.ready() == False)
			return "Not done. Try again later."

	for element in parts_result:
		for word in list_of_words:
			counters[word] = counters.get(word) + element.get(word)
	global final_result
	final_result = json.dumps(counters)
	return final_result





#REST API
apps = Flask(__name__)


@apps.route('/result', methods=['GET'])
def getResult():
	return combineResults()

@apps.route('/start', methods=['GET'])
def start():
	main()	
	return "Processes are now running."

	

if __name__ == '__main__':
    
    apps.run(host='0.0.0.0',debug=True)