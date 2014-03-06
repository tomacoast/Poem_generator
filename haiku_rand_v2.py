import random
words = [("Weston", 2), ("is", 1), ("and", 1), ("yellow-bellied", 4), ("tomato", 3), ("limeade", 2), ("Skittles", 2), ("who", 1), ("greet", 1),
 ("meet", 1), ("meat", 1), ("the", 1), ("dancer", 2), ("dances", 2), ("spaghetti", 3), ("hallow", 2), ("thy", 1), ("name", 1), ("repeat", 2),
 ("school", 1), ("lover", 2), ("love", 1), ("serendipity", 5), ("lady", 2), ("animal", 3), ("discover", 3), ("whom", 1), ("if", 1), ("go", 1),
 ("beyond", 2)]

theFile = "wordsEn.txt"

def grabEnglish(filename):
    f = open(filename)
    english = []
    for line in f:
        english.append(line.strip())
    f.close()
    return english

def createPoetry(argument):
    haiku = []
    for i in range(2):
        totsyl = 0
        line = []
        while (totsyl < 5):
            rand = random.randint(0,len(argument)) -1
            if (argument[rand][1]+totsyl <= 5):
                line.append(argument[rand])
                totsyl = totsyl + argument[rand][1]
        haiku.append(line)
    line = []
    totsyl = 0
    while (totsyl < 7):
            rand = random.randint(0,len(argument)) -1
            if (argument[rand][1]+totsyl <= 7):
                line.append(argument[rand])
                totsyl = totsyl + argument[rand][1]
    haiku.insert(1,line)
    for j in haiku:
        lin = ""
        for k in j:
            lin = lin + " " + k[0]
        print lin
    return haiku

createPoetry(words)
#print grabEnglish(theFile)
