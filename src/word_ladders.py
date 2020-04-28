#Word Ladders is a word game where a player tries to get from one word, the "start word" to another, the "goal
#word" in as few steps as possible. In each step, the player must either add one letter to the word from
#the previous step, or take away one letter, and then rearrange the letters to make a new word.

#import time
import sys
#startWord = sys.argv[1]
#targetWord = sys.argv[2]

startWord = "apple"
targetWord = "pear"
# print(startWord)
# print(targetWord)

#start = time.time()
queue=[]
path=[]

#---------------------------classes-------------------------------
class Node(object):
    visited = False
    parent = []
    actions =[] #child nodes
    #pathCost = 1
    name = ""

class Problem(object):
    initialState = ""
    #pathCost = 0
    targetState = ""


#---------------------------functions-----------------------------
#Recursive depth limited search
def DLS(node, problem, limit):
    #goal test
    if node.name == problem.targetState:
        printOutput(node)
        return "success"
    elif limit<=0: #limit test
        return "cutoff"
    else:
        cutoff = False
        node.visited = True;
        if len(node.actions)<=0:
            node.actions = createChildNodes(node)
        for child in node.actions:
            if child.visited == False:
                if child not in queue:
                    queue.insert(0, child)
            if len(queue) >0:
                next = queue.pop(0)
                result = DLS(next, problem, limit-1)
                if result == "cutoff":
                    cutoff = True
                elif result != "failure":
                    return result
        if cutoff == True:
            return "cutoff"
        else:
            return "failure"

#Iterative deepening search
def IDS(node, problem):
    # start = time.time()
    for depthLimit in range(100000):
        setVisitedFalse(node)
        result = DLS(node, problem, depthLimit)
        # end = time.time()
        # differece = end - start
        # print("depth: " + str(depthLimit))
        # print(str(differece) + "s")
        # print(str(differece / 60.0) + "m")
        if result != "cutoff":
            return result

def createChildNodes(node):
    childs =[]
    for word in wordLengthList[len(node.name)-1]:
        if (wordsHaveSameLetters(node.name, word, len(node.name)-1 ) == True):
            childNode = Node()
            childNode.name = word
            childNode.parent = node
            childs.append(childNode)
    for word in wordLengthList[len(node.name)+1]:
        if(wordsHaveSameLetters(node.name, word,len(node.name))==True):
            childNode = Node()
            childNode.name = word
            childNode.parent = node
            childs.append(childNode)
    #print("")
    return childs

def wordsHaveSameLetters(parentWord, childWord, nrLettersToBeSame):
    nrSameLetters =0
    for character in parentWord:
        if character in childWord:
            nrSameLetters=nrSameLetters+1
            childWord = childWord.replace(character,'',1)
            #str.replace(childWord, character, 1)
    if nrSameLetters >=(nrLettersToBeSame):
        return True
    else:
        return False

def setVisitedFalse(node):
    node.visited = False
    for child in node.actions:
        setVisitedFalse(child)

def printOutput(targetNode):
    path.append(targetNode.name)
    if targetNode.parent != []:
        printOutput(targetNode.parent)
    else:
        file = open("output.txt", "w")
        for step in reversed(path):
            print(step)
            file.write(step + "\n")
        file.close()


#-----------------------main-------------------------------

#read word List
wordList = open("../data/wordList.txt",'r').read().split('\n')
#without blank lines
wordList = [name for name in wordList if name]
#sort wordlist by Lengths
wordList = sorted(wordList, key=len)
#get shortest and Longest words
minWordLength = len(wordList[0])
maxWordLength = len(wordList[-1])

#reduce word list
rightCharacters =""
tempStartWord = startWord
for character in targetWord:
        if character in tempStartWord:
            #nrSameLetters=nrSameLetters+1
            rightCharacters = rightCharacters +character
            tempStartWord = tempStartWord.replace(character,'',1)

reducedWordList=[]
for word in wordList:
    tempWord = word
    nrRightWords=0
    for character in rightCharacters:
        if character in tempWord:
            # nrSameLetters=nrSameLetters+1
            nrRightWords = nrRightWords + 1
            tempWord = tempWord.replace(character, '', 1)
    if nrRightWords>=len(rightCharacters):
        reducedWordList.append(word)


# creat wordLengthList (words with lengths 3 are located in wordLengthList[3])
wordLengthList = [[]] * (maxWordLength + 1)
for words in reducedWordList: #much faster (especially if start and target word contains similar characters)
#for words in wordList:
    if wordLengthList[len(words)] == []:
        wordLengthList[len(words)] = [words]
    else:
        wordLengthList[len(words)].extend([words])


#---create start node and problem
t_root = Node()
t_root.name = startWord
problem = Problem()
problem.initialState = startWord
problem.targetState = targetWord

#start searching
#---Iterative deepening search
result = IDS(t_root, problem)
