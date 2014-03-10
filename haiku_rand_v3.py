import random
import requests
from xml.dom import minidom
import json
import tweepy
import webbrowser
import time
import sqlite3
import re

theFile = "wordsEn.txt"

def setupTwitter():
	auth = tweepy.OAuthHandler('3SGGosU9UWedvBbFgVnkYQ', '9C48yPix0fcfWGUjD42gVb1wvdtc0vgypgwLSfi5eG0')
	webbrowser.open(auth.get_authorization_url())
	verifier = raw_input('key?:')
	auth.get_access_token(verifier)
	key = auth.access_token.key
	secret = auth.access_token.secret
	return tweepy.API(auth)

def tweet(message, api):
	if api == None:
		raise Exception('need to call setupTwitter()')
	else:
		api.update_status(message)

def grabEnglish(filename):
    f = open(filename)
    english = []
    for line in f:
        english.append(line.strip())
    f.close()
    return english
    
def remember(word, syllables, wordType):
    conn = sqlite3.connect("wordbase.db")
    c = conn.cursor()
    testWord = (word,)
    c.execute('SELECT * FROM words WHERE Word =?', [word])
    if (c.fetchone() == None):
        c.execute('INSERT INTO words VALUES(%r, %s, %r)'%(word, syllables, str(wordType)))
        conn.commit()
    print c.fetchone()

def getType(word):
    try:
        url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/' + word + '?key=462334a9-867b-4ce1-b34e-ab97c3e3afc0'
        r = requests.get(url)
        m = minidom.parseString(r.text.encode('ascii', 'ignore'))
        wordType = m.getElementsByTagName('entry')[0].getElementsByTagName('fl')[0].toxml()
        wordType = re.sub('<[A-Za-z\/][^>]*>', '', wordType)
    except Exception, e:
        wordType = 0
    return wordType

def getSyllables(word):
    conn = sqlite3.connect("wordbase.db")
    c = conn.cursor()
    c.execute('SELECT * FROM words WHERE Word =?', [word])
    syllables = 0
    temp = c.fetchone()
    if (temp == None):
        url = 'http://rhymebrain.com/talk?function=getWordInfo&word=' + word
        try:
            r = requests.get(url)
            j = json.loads(r.text)
            wordType = getType(word)
            if (wordType != 0):
                remember(word, int(j['syllables']), wordType)
                syllables = int(j['syllables'])
            else:
                syllables = 0
        except requests.exceptions.RequestException, e:
            syllables = 0
    else:
        syllables = temp[1]
    return syllables

def haikuToString(haiku):
	x = ""
	for j in haiku:
		lin = ""
		for k in j:
		    lin = lin + " " + k#[0]
		x = x + lin + "\n"
	return x

def createPoetry(argument):
    haiku = []
    for i in range(2):
        totsyl = 0
        line = []
        while (totsyl < 5):
            rand = random.randint(0,len(argument)) -1
            if (getSyllables(argument[rand])+totsyl <= 5 and getSyllables(argument[rand]) > 0):
                line.append(argument[rand])
                totsyl = totsyl + getSyllables(argument[rand])
        haiku.append(line)
    line = []
    totsyl = 0
    while (totsyl < 7):
            rand = random.randint(0,len(argument)) -1
            if (getSyllables(argument[rand])+totsyl <= 7 and getSyllables(argument[rand]) > 0):
                line.append(argument[rand])
                totsyl = totsyl + getSyllables(argument[rand])
    haiku.insert(1,line)
    return haiku

api = setupTwitter()
while(True):
    print 'NEW POST-'
    haiku = haikuToString(createPoetry(grabEnglish(theFile)))
    print haiku
    tweet(haiku, api)
    time.sleep(60*60*12) #time in seconds, 12hr posts
