import random
import requests
from xml.dom import minidom
import json

theFile = "wordsEn.txt"

def grabEnglish(filename):
    f = open(filename)
    english = []
    for line in f:
        english.append(line.strip())
    f.close()
    return english

def getSyllables(word):
	url = 'http://rhymebrain.com/talk?function=getWordInfo&word=' + word
	r = requests.get(url)
	j = json.loads(r.text)
	return int(j['syllables'])

def createPoetry(argument):
    haiku = []
    for i in range(2):
        totsyl = 0
        line = []
        while (totsyl < 5):
            rand = random.randint(0,len(argument)) -1
            if (getSyllables(argument[rand])+totsyl <= 5):
                line.append(argument[rand])
                totsyl = totsyl + getSyllables(argument[rand])
        haiku.append(line)
    line = []
    totsyl = 0
    while (totsyl < 7):
            rand = random.randint(0,len(argument)) -1
            if (getSyllables(argument[rand])+totsyl <= 7):
                line.append(argument[rand])
                totsyl = totsyl + getSyllables(argument[rand])
    haiku.insert(1,line)
    for j in haiku:
        lin = ""
        for k in j:
            lin = lin + " " + k#[0]
        print lin
    return haiku

#print getSyllables("antipersperant")
createPoetry(grabEnglish(theFile))
#print grabEnglish(theFile)
