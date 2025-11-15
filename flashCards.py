import csv, random, time, os, sys
#from gtts import gTTS


#features to add:

setup = {
  #This is where to draw the cards from. If you want to define an alternate path where the csv files are, uncomment the second line and fill it in
  "flash_card_path":os.path.dirname(os.path.abspath(sys.argv[0])),
  #"flash_card_path":"C:/Users/Coolb/oneDrive/Desktop/All code/flashes",
  
  #This is the chance for cards you already know to be shown again compaired to the words you don't know. The default is 10% (written as 10)
  "chance_for_known_cards":10,
  
  #Selects whether you want to see the front or back of the card
  "show_back_card":True,
  
  #This is what percent you increase the score when submitting your rating
  "card_modifier":30,
  
  #This is the card modifier if you are in the gimme mode
  "gimme_modifier":10,
  
  #This is how long you are given in timed mode
  "time_to_answer":1.5
}

def getPercentOfThrough(flash):
  c = 0
  for i in flash:
    c += i[2]
  print ("you have gotten", 10*(c/len(flash)), "percent of the way through")

  
def printFlashes(flash):
  for i in range(0,len(flash)):
    printer = "#" + str(((indexes[i]) if (isGimme) else (i))+1) + ": " + (flash[i][1]) + ", " + str(flash[i][0]) + " is at " + str(flash[i][2])
    print(printer)

def getCSV():
  try:
    with open(flashCardFile, 'r', newline='', encoding="utf8") as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      allFlash = list(spamreader)
  except FileNotFoundError:
    print(FileNotFoundError)
    time.sleep(2)
  try:
    #rounds all scores
    for i in range(0,len(allFlash)):
      allFlash[i][2] = round(float(allFlash[i][2]),3)
  except:
    #if scores don't exist, add scores
    for i in range(0,len(allFlash)):
      if (len(allFlash[i]) == 2):
        allFlash[i].append(0)
  return allFlash

def changeAllScores(changeBy):
  allFlash = getCSV()
  #averages the score and the input times the card modifier
  for l in range(0,len(allFlash)):
    allFlash[l][2] = float(allFlash[l][2]) + changeBy
    if (allFlash[l][2] > 10.0):
      allFlash[l][2] = 10.0
    elif (allFlash[l][2] < 0.0):
      allFlash[l][2] = 0.0
  #allows people to get to 10 if they input a number higher than it
  with open(flashCardFile, 'w', newline='', encoding="utf8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    for i in range(0,len(allFlash)):
      spamwriter.writerow([allFlash[i][0],allFlash[i][1],allFlash[i][2]])

def write(selection,flash):
  if(isGimme):
    selection = indexes[selection]
  inp = input("how easy was that out of 4?")
  if(inp):
    allFlash = getCSV()
    #averages the score and the input times the card modifier
    change = (float(inp)-1)*11/3
    allFlash[selection][2] = float(allFlash[selection][2])*(1-cardModifier) + cardModifier * change
    #allows people to get to 10 if they input a number higher than it
    if (allFlash[selection][2] > 10.0):
      allFlash[selection][2] = 10.0
    elif (allFlash[selection][2] < 0.0):
      allFlash[selection][2] = 0.0
    with open(flashCardFile, 'w', newline='', encoding="utf8") as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',')
      for i in range(0,len(allFlash)):
        spamwriter.writerow([allFlash[i][0],allFlash[i][1],allFlash[i][2]])


def select(flash):
  #adds all scores onto a number line, picks a point on it, then uses that number
  c = 0
  for i in range(0,len(flash)-1):
    c = c + (knownCardChance-flash[i][2])
  sel = random.uniform(0,c-0.05)
  i = 0
  while (True):
    try:
      if (sel < (knownCardChance-flash[i][2])):
        return i
      sel = sel - (knownCardChance-flash[i][2])
      i = i + 1
    except:
      print("error on line 98, going past end of file")
      print(sel, ", ", i)
      c = 0
      for i in range(0,len(flash)-1):
        c = c + (knownCardChance-flash[i][2])
      sel = random.uniform(0,c-0.05)
      i = 0
  return 0;



def getLowestIndexes(list,amount):
  list_tmp = list.copy()
  list_sorted = list.copy()
  list_sorted.sort()
  list_index = []
  for x in list_sorted:
    list_index.insert(0,list_tmp.index(x))
    list_tmp[list_tmp.index(x)] = -1
  return(list_index[len(list_index)-amount:len(list_index)])

def setFile():
  #this adds scores to CSV files
  allFlash = getCSV()
  with open(flashCardFile, 'w', newline='', encoding="utf8") as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',')
      for i in range(0,len(allFlash)):
        spamwriter.writerow([allFlash[i][0],allFlash[i][1],allFlash[i][2]])

def mystery():
  allFlash = getCSV()
  for i in range(0,len(allFlash)):
    try:
      if (allFlash[i][0].index("（") == 0):
        allFlash[i][0] = allFlash[i][0][1:len(allFlash[i][0])]
    except:
      var = 1
  with open(flashCardFile, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    for i in range(0,len(allFlash)):
      spamwriter.writerow([allFlash[i][0],allFlash[i][1],allFlash[i][2]])
      
#setting up variables
knownCardChance = 10/(1-setup["chance_for_known_cards"]/100)
showBackCard = setup["show_back_card"]
correct_files = []
for i in os.listdir(setup['flash_card_path']):
  if (i[-4:] == ".csv"):
    correct_files.append(i)
print("enter the index of the file you'd like from the list of")
print(correct_files)
flashCardFile = setup['flash_card_path'] + "/" + correct_files[int(input())]
print(flashCardFile)
cardModifier = setup["card_modifier"]/100
isGimme = False
allFlash = getCSV()
timeToAns = setup["time_to_answer"]


while (True):
  decision = int(input("Glad to see you back! Input a 0 to begin, a 1 to check progress, a 2 for a gimme, a 3 to set up a new file, a 4 to give two words to keep with you, a 5 to pick out a few random words, a 6 to change all scores by an amount."))
  if (decision == 0):
    difficulty = int(input("How difficult in percent?"))
    flash = allFlash[0:int(len(allFlash) * difficulty/100)]
    break
  elif (decision == 1):
    getPercentOfThrough(allFlash)
    printFlashes(allFlash)
  elif (decision == 2 or decision == 4):
    isGimme = True
    cardModifier = setup["gimme_modifier"]/100
    if (decision == 2):
      difficulty = int(input("How difficult in percent?"))
      amount = int(input("How many cards would you like to gimme?"))
    else:
      difficulty = 100
      amount = 2
    flashChoices = allFlash[0:int(len(allFlash) * difficulty/100)]
    flashPrios = []
    for i in range(0,len(flashChoices)):
      flashPrios.append(flashChoices[i][2])
    indexes = getLowestIndexes(flashPrios,amount)
    flash = []
    for i in range(0,len(indexes)):
      flash.append(flashChoices[indexes[i]])
    printFlashes(flash)
    if (decision == 4):
      exit()
    break
  elif (decision == 3):
    setFile()
  elif (decision == 5):
    difficulty = int(input("How difficult in percent?"))
    amount = int(input("How many cards would you like?"))
    flash = allFlash[0:int(len(allFlash) * difficulty/100)]
    for i in range(0,amount):
      selection = random.randint(0,len(flash))
      print(flash[selection][0] + ", " + flash[selection][1])
    exit()
  elif (decision == 6):
    changeAllScores(float(input("change by how much?")))
  # elif (decision == 7):
  #   difficulty = int(input("How difficult in percent?"))
  #   flash = allFlash[0:int(len(allFlash) * difficulty/100)]
  #   while(True):
  #     selection = select(flash)
  #     if (showBackCard):
  #       myObj = gTTS(text = flash[selection][1], lang = "ja")
  #       myObj.save("read.mp3")
  #       os.system("start read.mp3")
  #       input()
  #       print(flash[selection][1])
  #       print(flash[selection][0])
  #     else:
  #       myObj = gTTS(text = flash[selection][0], lang = "ja")
  #       myObj.save("read.mp3")
  #       os.system("start read.mp3")
  #       input()
  #       print(flash[selection][0])
  #       print(flash[selection][1])
  #     write(selection,flash)
while(True):
  selection = select(flash)
  if (showBackCard):
    print(flash[selection][1])
    input()
    #time.sleep(timeToAns)
    print(flash[selection][0])
  else:
    print(flash[selection][0])
    input()
    #time.sleep(timeToAns)
    print(flash[selection][1])
  write(selection,flash)

#trash

    #try:
      #print(flash[selection][0][0:int(flash[selection][0].index("（"))])
    #except:
      