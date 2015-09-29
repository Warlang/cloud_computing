#with open('twitter_tweets.txt') as f:  #
#    lines = f.readline()

import json

#Attributes
#f = open('twitter_tweets.txt') #Open file stream
list_of_words = ['han','hon','den','det','denna','denne','hen'] #List of words to check for
counters = {'han':0 , 'hon': 0, 'den':0, 'det':0, 'denna':0, 'denne':0, 'hen':0} #Count each words in 



#getText: Get the text from the file that is gonna be checked from n lines.
#Arguements: n - N must be an positive integer. Higer number n give more text to check
def getText():
	text = " "
	skipRow = False
	with open("twitter_tweets.txt") as f:
		for row in f:
			if (skipRow):
				skipRow = False
			else:
				skipRow = True
				json_obj = json.loads(row)		
				if (validText(json_obj)):
					text = text + json_obj['text']
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
	for word in list_of_words:
		n = text.count(word)
		counters[word] = counters.get(word) + n


#Main
#What happens if you try to read more than exist in the file?
text = getText()
countWords(text)

print counters
result = json.dumps(counters)
print result


#Exempel for a original tweet--
# "retweeted":false

#Exempel to en tweet--
# "text":"Vem var det som sa att det inte skulle bli n\u00e5gon sommar efter den varma april? #fb"