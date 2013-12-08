#!/bin/python3

""" DOCUMENTATION
Group: Nelson Chen, Jean Chen, Steve Cassedy, Sophal Chhay

To run the program, double click the file.
If using IDLE, while the program window is up,
press F5 or go to run -> Run Module

"""

# imports
import sys
import collections
import random

# ------------------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------------------

# counter to keep track of how many facts/queries were given
output = 0
fact_key = 0 # keeps track of which base fact (key) the AI is on
fact_value = 0 # keeps track of which super fact (value) the AI is on
flag_confused = False 
clarify_count = 0 # keeps track of how many attempts were made to clarify

# remembers the last thing it said to other AI
prev_output = []

# questions already asked
askedWhoQ=[]
askedIsQ= []
askedWhatQ= []
a_an="a/an"

################################################################################
'''
How the KB works so far:

The knowledge base currently can handle verbs, adjectives, and prepositions.

I did not create lists for "not" something. I figure that we can save
information in the KB as "not human", "not animal", etc.

It is easy in python to parse strings so checking for "not" wouldn't be
difficult. We can do this differently if we choose to do so.

For adverbs, I think it would be easiest to save them with their respective
verbs, so a sample verb is "moved quickly".

I am not sure the best way to handle prepositions or possessions yet. I made
space for them in the KB for the mean time.

The lists for possible options should be useful for generating questions.

The initial KB info is from my last project and open for change.

'''

###############################################################################
#                     Creates Lists and KB for Program

#list of possible names
individual = ['Steve','Gandalf','Chewbacca','Daxter','Fido','Nelly']

#list of possible things
category = ['human','animal','wizard','wookie','ottsel',
          'alien','mammal','idiot','dog','cat','humans',                    
          'animals', 'wizards','wookies','ottsels','aliens',
          'mammals','idiots','dogs','cats']

# nouns knowledge base format is a list of a list.  Inner list is of
# the form [singular, plural]. I.E [[person, people], [foot, feet] ...]
nouns = [['human','humans'],['animal','animals'],['wizard','wizards'],
           ['wookie','wookies'],['ottsel','ottsels'],['alien','aliens'],
           ['mammal','mammals'],['idiot','idiots'],['dog','dogs'],
           ['cat','cats']]

#list of adjectives
Adjectives = []

#list of possible verbs
Verbs = []

#list of possible verbs
Adverbs = []

#list of possible prepositions
Prepositions = []

#list of the knowledge base
#[thing,list of what thing is,list of what is not]
KB = {}
KB['Steve'] = [['human','idiot','animal','mammal'],[],[],[],[]]
KB['Gandalf'] = [['wizard'],[],[],[],[]]
KB['Chewbacca'] = [['wookie','alien','animal'],[],[],[],[]]
KB['Daxter'] = [['ottsel','idiot','mammal','animal'],[],[],[],[]]
KB['Nelly'] = [['cat','animal','mammal'],[],[],[],[]]
KB['Fido'] = [['dog','animal'],[],[],[],[]]
KB['human'] = [['animal','mammal'],[],[],[],[]]
KB['ottsel'] = [['animal','mammal'],[],[],[],[]]
KB['cat'] = [['animal','mammal'],[],[],[],[]]
KB['dog'] = [['animal'],[],[],[],[]]
KB['wookie'] = [['animal','alien'],[],[],[],[]]
KB['alien'] = [['animal'],[],[],[],[]]
KB['mammal'] = [['animal'],[],[],[],[]]
KB['wizard'] = [[],[],[],[],[]]
KB['idiot'] = [[],[],[],[],[]]
KB['animal'] = [[],[],[],[],[]]






###############################################################################
#                        Functions for Updating the KB

def update_names(name):
    '''
    appends new name to names list
    '''
    if individual.count(name) == 0:
        individual.append(name)

def update_categories(thing):
    '''
    appends new thing to things list
    '''
    if category.count(thing) == 0:
        category.append(thing)

def update_plurals(single,plural):
    '''
    appends new item to the plural list
    '''
    if nouns.count([single,plural]) == 0:
        nouns.append([single,plural])

def update_adjectives(adj):
    '''
    appends new adjective to adjectives list
    '''
    if Adjectives.count(adj) == 0:
        Adjectives.append(adj)

def update_verbs(verb):
    '''
    appends new verb to verbs list
    '''
    if Verbs.count(verb) == 0:
        Verbs.append(verb)

def update_adverbs(adv):
    '''
    appends new adverb to adverbs list
    '''
    if Adverbs.count(adv) == 0:
        Adverbs.append(adv)

def update_prepositions(prep):
    '''
    appends new perpositions to prepositions list
    '''
    if Prepositions.count(prep) == 0:
        Prepositions.append(prep)

def append_sublist(sublist,original_list):
    '''
    appends a sublist to another list (no repeats)
    '''
    for i in sublist:
        if original_list.count(i) == 0:
            original_list.append(i)

def update_KB_is(thing, what_thing_is):
    '''
    updates the knowledge base when thing is what_thing_is
    
    '''
    #gets sublist of what_thing_is
    found_thing = False
    sublist_is = []
    sublist_adj = []
    sublist_verb = []
    sublist_prep = []
    sublist_poss = []
    if what_thing_is in KB:
        sublist_is = KB.get(what_thing_is)[0]
        sublist_adj = KB.get(what_thing_is)[1]
        sublist_verb = KB.get(what_thing_is)[2]
        sublist_prep = KB.get(what_thing_is)[3]
        sublist_poss = KB.get(what_thing_is)[4]
            
    #adds new item to KB
    if not (thing in KB):
        KB[thing] = [[thing],[],[],[],[]]
    
    #appends related information with new information
    for key in KB.keys():
        if key == thing and KB.get(key)[0].count(what_thing_is) == 0:
            KB.get(key)[0].append(what_thing_is)
            append_sublist(sublist_is,KB.get(key)[0])
            append_sublist(sublist_adj,KB.get(key)[1])
            append_sublist(sublist_verb,KB.get(key)[2])
            append_sublist(sublist_prep,KB.get(key)[3])
            append_sublist(sublist_poss,KB.get(key)[4])
        if KB.get(key)[0].count(thing) > 0:
            print(KB.get(key)[0])
            KB.get(key)[0].append(what_thing_is)
            append_sublist(sublist_is,KB.get(key)[0])
            append_sublist(sublist_adj,KB.get(key)[1])
            append_sublist(sublist_verb,KB.get(key)[2])
            append_sublist(sublist_prep,KB.get(key)[3])
            append_sublist(sublist_poss,KB.get(key)[4])

def update_KB_adj(thing,adj):
    '''
    adds adjectives to KB
    '''
    #adds adj to thing and everything that is a thing
    for key in KB.keys():
        if key == thing and KB.get(key)[1].count(adj) == 0:
            KB.get(key)[1].append(adj)
        if KB.get(key)[0].count(thing) > 0 and KB.get(key)[1].count(adj) == 0:
            KB.get(key)[1].append(adj)

    #adds thing if new to KB
    if not (thing in KB):
        KB[thing] = [[],[adj],[],[],[]]

def update_KB_verb(thing,verb):
    '''
    adds verbs to KB
    '''
    #adds verb to thing and everything that is a thing
    for key in KB.keys():
        if key == thing and KB.get(key)[2].count(verb) == 0:
            KB.get(key)[2].append(verb)
        if KB.get(key)[0].count(thing) > 0 and KB.get(key)[2].count(verb) == 0:
            KB.get(key)[2].append(verb)

    #adds thing if new to KB
    if not (thing in KB):
        KB[thing] = [[],[],[verb],[],[]]

def update_KB_prep(thing,prep):
    '''
    adds prepositions to KB
    '''
    #adds prep to thing and everything that is a thing
    for key in KB.keys():
        if key == thing and KB.get(key)[3].count(prep) == 0:
            KB.get(key)[3].append(prep)
        if KB.get(key)[0].count(thing) > 0 and KB.get(key)[3].count(prep) == 0:
            KB.get(key)[3].append(prep)

    #adds thing if new to KB
    if not (thing in KB):
        KB[thing] = [[],[],[],[prep],[]]

def update_KB_poss(thing,poss):
    '''
    adds possessions to KB
    '''
    #adds poss to thing and everything that is a thing
    for key in KB.keys():
        if key == thing and KB.get(key)[4].count(poss) == 0:
            KB.get(key)[4].append(poss)
        if KB.get(key)[0].count(thing) > 0 and KB.get(key)[4].count(poss) == 0:
            KB.get(key)[4].append(poss)

    #adds thing if new to KB
    if not (thing in KB):
        KB[thing] = [[],[],[],[],[poss]]





###############################################################################



# ------------------------------------------------------------------------------
# General all purpose helper functions that help with all functions.
# ------------------------------------------------------------------------------

# a helper function that converts a list of nouns to its counter-part
# inType is if the nounList is plural 'P' or singular 'S'
def convert(nounList, inType):
    if inType == 'S':
        index = 1
        check = 0
    elif inType == 'P':
        index = 0
        check = 1
    else: #should never be here, for debugging purposes only
        print("error, parameter 2 incorrect format")
        sys.exit()
    # list to return
    c_list = []
    # check all the known nouns
    for noun in nounList:
        for pair in nouns:
            if pair[pairIndex] == noun:
                c_list.append(pair[index])
                break
    # return the list
    return c_list

# A function that prints a list to std.out
def print_list(inList):
    for index in range(0, len(inList) - 1):
        if index == len(inList)-1:
            print(inList[index])
        else:
            print(inList[index], end =" ")

# A function that removes punctuation marks
def remove_punc(word):
    newWord = word
    for index in range(0,len(word)-1):
        letter = word[index]
        if letter == '!' or letter == '?' or letter == ',' or letter == '.':
            newWord = word[0:index]
            break
    return newWord






# ------------------------------------------------------------------------------
# These functions deal with inference and answering questions.
# If an answer is not known, then the AI can ask a question related to the
# question it was asked, if it can make the connection (I.E for "who is a dog?"
# if it does not know, it can look through the database and pick a random
# person or thing) or it can respond with "I am not sure"
# ------------------------------------------------------------------------------

###########################################################

#reply for isQuestion 

def checkIsQuestion(rand_name, word, a_an):
    check=False
    values=[]
    values= KB.get(rand_name)
    if(values is not None):
        for ele in values:
            if word == ele:
                check=True
                print(rand_name,"is",a_an ,word,'.')
# if kb doesn't have the fact, ask a related query
    if (check==False):  

    #asked a related questions 
        relatedToIsQuestion(rand_name, word)

########################################################
#reply for who question

def checkWhoQuestion(word):
    check=False
    count=0
    ct=0
    output=''
    correct_answer=[]
    for name, value in KB.items():
        if word in value:
            correct_answer.append(name)     
            count+=1

    if(count !=0):
        if(count ==1):
              
                output= correct_answer.pop(0)
                print(output,'is a',word,'.')
        else:
            while(ct !=count):
                if(ct == count-1):
                    output+=' and '
                    output +=correct_answer.pop(0)
                else:
                    output +=' '
                    output += correct_answer.pop(0)
                ct+=1
            word+='s'
            print(output,'are',word,'.')         
# if kb doesn't have the fact, ask a related query
    if(output==''):
       #asked related query (create is question)
        relatedToWhoQuestion(word)
   
########################################################

# A function that answers questions of the form "what is X"
def checkWhatQuestion(aThing):
    # variable to hold the properties of aThing
    properties = None
    # stores the index of the key
    index = 0
    # variable to store our response to the what is X question
    response = []
    # if this person or thing is known
    if aThing in individual:
        properties = KB[aThing]
    # if AI does not know what X is
    if properties == None:
        # we can have a 50% chance to say not sure or ask related question
        # if time permits
        response = ['I', 'am', 'unsure']
    else:
        global fact_value
        # the first list in properties is what X is
        values = properties[0]
        # give one of the things that X is that hasn't be given yet
        xIs = None
        # if we're giving facts about X, then just give the next fact
        if index == fact_key:
            xIs = values[fact_value]
            # updates global counter
            fact_value += 1
        # else give the last fact about X
        else:
            xIs = values[len(values)-1]
        # updates previous output
        response = [aThing, 'is', 'a', xIs]
    return response

# A function that answers questions of the form "Are X Y"
def checkAreQuestion(aThing, inCategory):
    # stores the response in a variable
    response = []
    # look for X in the list of keys
    properties = None
    # if this category is known
    if aThing in category:
        properties = KB[aThing]
    # If X is not in the database
    if properties == None:
        # 50% chance to say unsure or give related query/fact
        response = ['I', 'am', 'unsure']
    else:
        # stores list of what X is
        values = properties[0]
        # check if X has Y in its property list
        if inCategory in values:
            response = [aThing, 'are', category]
        else:
            # 50% chance to say unsure or give related query/fact
            response = ['I', 'am', 'unsure']
    return response




# ------------------------------------------------------------------------------
# These functions deal with asking questions
# ------------------------------------------------------------------------------

############ related is-question ###################
# A function that asks a related question to is X a/an Y
# The AI will ask for clarification if it doesnt know.
# If it doesnt know who X is, it will ask what is X
# if it doesnt know what Y is, it will ask who is a Y

def relatedToIsQuestion(x_value, y_value):
    rand= random.randint(0,1)
    if(rand==0):
        if(x_value in individual):
            print("Who is ", a_an, x_value,'?')
            askedWhoQ.append(x_value)
        else:
            print('What is', x_value,'?')
            askedWhatQ.append(x_value)
    else:
        if(y_value in category):
            print('What is',a_an, y_value,'?')
            askedWhatQ.append(x_value)
        else:
            print('Who is',a_an, y_value,'?')
            askedWhoQ.append(y_value)
            
############related who-questions##########
# A function that asks a related question to "who is a/an Y"
# The AI will take a guess, so it will ask "is X a/an Y"
# where X is a randomly chosen specific person or thing

def relatedToWhoQuestion(a_object, a_an): 
    rand= random.randint(0,len(individual)-1)
   
    #pick a random number from individual
    rand_name= individual[rand]

  
# check whether word is already asked or not
    currQuest= (rand_name,a_object)
    flag= currQuest in askedIsQ

# if yes, get a another random word
    while(flag==True):
       rand= random.randint(0,len(individual)-1)
       #pick a random number from individual
       rand_name= individual[rand]

       # check whether word is already asked or not
       currQuest= (rand_name, a_object)
       flag= currQuest in askedIsQ

    print('Is', rand_name, 'a/an',a_object,'?')
    askedIsQ.append(currQuest)


# A function that asks a related question to "what is X"
# The AI will take a guess, so it will ask "is X a Y?"
# where Y is random chosen higher category than X
def relatedWhatQuestion(aThing):
    rand= random.randint(0,len(category)-1)
   
    #pick a random number from category
    rand_name= category[rand]

  
# check whether word is already asked or not
    currQuest= (rand_name,aThing)
    flag= currQuest in askedIsQ

# if yes, get a another random word
    while(flag==True):
       rand= random.randint(0,len(category)-1)
        #pick a random number from category
       rand_name= category[rand]
        # check whether word is already asked or not
       currQuest= (rand_name, aThing)
       flag= currQuest in askedIsQ

    print('Is', rand_name, 'a/an',aThing,'?')
    askedIsQ.append(currQuest)
# A function that asks a related question to "are X Ys"
def relatedAreQuestion(aThing, aThing2):

    rand= random.randint(0,1)
    if(rand==0):
            print("What are ", aThing,'?')
            askedWhatQ.append(aThing)
    else:
            print('What are',aThing2,'?')
            askedWhatQ.append(aThing2)
        

    	


# ------------------------------------------------------------------------------
# These functions deal with storing knowledge into the database
# Once a fact is stored, the AI should respond with a related question.
# I.E "Dogs are cute" => "what are dogs."  Note that the AI would only need to
# ask about dogs in this case since this fact is of the form X are Y.  It would
# be hard to answer what is an animal or what is cute.
# If a fact is already known, the AI will either give a new fact or query with
# an equal chance of either one happening.
# ------------------------------------------------------------------------------

# gives a fact that the AI knows
def giveFact():
    global fact_value
    global fact_key
    global prev_output
    # gets all the keys from the database
    keys = KB.keys()
    # check which key we are on
    key = keys[fact_key]
    # get properties of the thing we're looking at
    properties = KB[key]
    values = properties[0] # list of what person/category is, is in 1st index
    # determine if the key is a person or category
    if key in Individual:
        # If its a person
        # >>>> NEED TO CHECK WHETHER TO USE A/AN <<<<<<<
        print(key + ' is' + ' a ' + values[fact_value])
        # update global counter
        prev_output = [key, 'is', 'a', values[fact_value]]
    else:
        # If its a general category
        # >>>> NEED TO CHECK WHETHER TO USE A/AN <<<<<<<
        print(key + ' are ' + values[fact_value])
        # update what previous output was
        prev_output = [key, 'are', values[fact_value]]
    # update global variables
    fact_value += 1
    # if end of list
    if fact_value > len(values)-1:
        # reset value counter
        fact_value = 0
        fact_key += 1
        # if at the end of DB
        if fact_key > len(keys)-1:
            fact_key = 0 # start from very beginning

# This helper function adds the fact into the database
# Note: all facts are stored as singular!
def addFact(subClass, superClass):
    added = False # flag to check whether to ask a query at the end
    # Look for the subClass in the KB
    # things is everything the person or thing is
    for name, things in KB.items():
        # if found, check if the superclass is attached to the subclass
        if name == subClass:
            if superClass in things: 
                added = True
                # if fact is known, then give new fact or query
                if random.randint(0,1):
                    # give a fact
                    giveFact()
                else:
                    #randomly create a query
                    temp = random.sample( KB.keys(),1)
                    print("what is "+temp[0]+"?")
            else:
                added = True
                temp = KB[subClass]
                temp.append(superClass)
                KB[subClass] = temp
                print("what is the plural of "+ superClass +"?") #temporary
                # if fact is not known, attach it to the subclass
                # check whether superClass is a noun/adjective, why?
                # give related query (who question related to superclass)
    # if the subClass was not found as the starting as the "key" add to KB
    if not added:
        KB[subClass] = superClass.split() #add it as a list
        print("what is the plural of "+ superClass +"?") #temporary
        # add to KB
        # check whether superClass is a noun/adjective
        # switch to subclass to plural
        # ask what are "subClass" if not known, (maybe say who is a superclass
        # if it knows what the subclass is
        

# This function stores a fact of the form Xs are Ys
# This function is needed because X and Y are plural
# subClass is the lower class (I.E dogs)
# superClass is the general category (I.E animal)
def addFactAre(subClass, superClass):
    # change subClass and superClass into singular nouns
    singList = convert([subClass, superClass], 'P')
    addFact(singList[0], singList[1])


# This function stores fact of the form X is a Y
# This function is needed because Y is singular
# subClass is the lower class (I.E fido)
# superClass is the more general category (I.E Dog in this case)
def addFactIsA(person, superClass):
    # call helper function to add fact into database, no change needed
    addFact(person, superClass)






# ------------------------------------------------------------------------------
# These functions deal with responses that say "I am confused" or "I am unsure"
# If another AI remains confused after a few times, the AI should give it
# a new fact.
# Note: Might need to fix if previous outputs subjects have more than 1 person
# ------------------------------------------------------------------------------

# this function attempts to clarify by outputing related another fact
# when the other AI is confused after hearing a fact. it gives up after 3 tries
def clarify_confused():
    global clarify_count
    # gives a related fact
    # gives the next thing X is on its list of values
    values = KB.get(x)
    y = []
    # Y's location in the input
    if len(prev_output) == 3: # X are Y
        y = prev_output[2]
    else: # X is a Y
        y = prev_output[3]
    # iterate through values of the key
    for index in range(0, len(values)):
        # if this was the value (Y) that was given
        if values[index] == y:
            # allows us to modify global variables
            global fact_key
            global fact_value
            # if there are more things this object is
            if index+1 < len(values): # check boundary:
                #--> requires form changing <--
                print(prev_output[0] + "are" + values[index+1])             
                # set new output
                prev_output = [prev_output[0], 'are', values[index+1]]
                fact_value += 1
            # if there are no more things this object is
            # look for a super class of Y
            else:
                # get values for y
                values2 = KB.get(y)
                # if there are no super class of Y
                if values2 == None:
                    # just give another fact
                    fact_key += 1
                    fact_value = 0
                    giveFact()
                # give a fact about the super class
                else:
                    print(y + "are" + values2[0])
                    # update previously given output
                    prev_output = [y, 'are', values2[0]]
            break # break out of loop
    clarify_count += 1 # increment try counter



# this function attempts to clarify by outputing another related query
# when the other AI is confused after hearing a fact. it gives up after 3 tries
def clarify_unsure():
    # gives us permission to change global variable
    global clarify_count
    global prev_output
    clarify_count += 1
    # If other AI is unsure who is a/an X, our AI should answer the question
    if prev_output[0] == 'who' and prev_output[1] == 'is':
        # answer the question
        answer = checkWhoQuestion(prev_output[3])
        # if no answer was found
        if answer[0] == 'i' and answer[1] == 'am' and answer[2] == 'unsure':
            # ask a related question
            answer = relatedToWhoQuestion(prev_output[3])
        # give answer
        else:
            # ===== >NEED TO FIX ALL PRINT STATMENTS!!!!! <=================
            print(answer[0] + " is a " + answer[3])
            prev_output = [answer[0], 'is', 'a', answer[3]]
            
    # If other AI is unsure what is X, our AI will answer the question
    elif prev_output[0] == 'what' and prev_output[1] == 'is':
        # answer the question
        answer = checkWhatQuestion(prev_output[3])
        # if no answer was found
        if answer[0] == 'i' and answer[1] == 'am' and answer[2] == 'unsure':
            answer = relatedWhatQuestion(prev_output[3])
        # give answer
        else:
            print(answer[0] + " is a " + answer[3])
            prev_output = [answer[0], answer[1], answer[2], answer[3]]
            
    # If other AI is unsure if X is a Y
    elif prev_output[0] == 'is':
        # answer the question
        answer = checkIsQuestion(prev_output[1], prev_output[3], prev_output[2])
        # if no answer was found
        if answer[0] == 'i' and answer[1] == 'am' and answer[2] == 'unsure':
            # give related question
            relatedToIsQuestion(prev_output[1],prev_output[3])
        # give answer
        else:
            print(answer[0] + " is a " + answer[3])
            prev_output = [answer[0], 'is', 'a', answer[3]]
            
    # If other AI is unsure if X are Y's
    elif prev_output[0] == 'are':
        # answer the question
        answer = checkAreQuestion(prev_output[1], prev_output[2])
        # if no answer was found
        if answer[0] == 'i' and answer[1] == 'am' and answer[2] == 'unsure':
            # give related question
            relatedAreQuestion(prev_output[1], prev_output[2])
        # give answer
        else:
            print(answer[0] + " are " + answer[2])
            prev_output = [answer[0], 'are', answer[2]]
    # program should never get here; need to remove later
    else:
        print("if you are here, then other AI is unsure of a fact")
        clarify_confused()






# ------------------------------------------------------------------------------
# Main function and helper functions that help parse the input
# ------------------------------------------------------------------------------

# A function that process the input depending on new restrictions
# If the program reaches here then either malformed input was recieved
# or input with more than one subject was recieved
# Example form:  Josh is a student and a TA
# Example Form2: Josh and Emily are TAs
def process_input2(line):
    people = []
    categories = []
    new_fact = [] # remembers a new fact that has been added
    # check if line contains is
    if line[1] == 'is' and line[2] == 'a' and ('and' in line):
        # there should only be one subject
        people.append(line[0])
        # iterate through line list and get all categories
        for index in range(3, len(line)):
            # if this word is 'a' do nothing
            if line[index] == 'a':
                continue #do nothing
            # if this word is 'and', we only have one more category to add
            elif line[index] == 'and':
                # remove the period if it contains it
                word = remove_punc(line[index+2])
                # the location of this category in the list is 2 spaces ahead
                categories.append(word)
                break
            # any other word is added as a category
            else:
                # removed the comma if it contains it
                word = remove_punc(line[index])
                categories.append(word)
        # after everything has been added, add all these facts to DB
        # directly, so it doesnt give a response
        for index in range(0, len(categories)-1):
            inserted = addFact(people[0], categories[index])
            # if fact was not known, then it was inserted
            if inserted:
                new_fact = [people[0], categories[index]]
        # give a related query to a new fact that has been added
        relatedToIsQuestion(new_fact[0], new_fact[1])

    # if line has an 'are' in it (josh and emily are TAs)
    elif line[len(line)-2] == 'are' and ('and' in line):
        # there are more than one subject but only one category
        # stores all the people into the list of people
        for index in range(0,len(line)-1):
            # if this part of the line says 'and
            if line[index] == 'and':
                # add the last person to the list (which is the next word)
                people.append(line[index+1])
                break # stop looking for people
            else:
                # remove any puncations associated with the name
                person = remove_punc(line[index])
                people.append(line[index])
        # stores the category into the list
        categories.append(line[len(line)-1])
        # add all the facts into DB
        for index in range(0,len(people)-1):
            inserted = addFact(people[index],categories[0])
            if inserted:
                new_fact = [people[index], categories[0]]
        # give a related query to the new fact that has been added
        relatedAreQuesion(new_fact[0], new_fact[1])

    # all other input are considered malform input
    else:
        global prev_output
        prev_output = ['i', 'am', 'confused']
        print("I am confused")
                

# A function that handles inputs of length 4
def process_input4(AI_Input):
    # if input is of the form who is a/an Y
    if AI_Input[0] == 'who' and AI_Input[1] == 'is':
        # had to put rest of conditional on a new line
        if AI_Input[2] == 'a' or AI_Input[2] == 'an':
            answer = checkWhoQuestion(AI_Input[3])
        # Print statement here because it skips the other one at
        # end in case of malform input
        else:
            print("I am confused")
    # if input is of the form X is a/an Y
    elif AI_Input[1] == 'is' and (AI_Input[2] == 'a' or AI_Input[2] == 'an'):
        # helper function that adds the fact to KB if not known
        addFactIs(AI_Input[0], AI_Input[3])
    # if input is of the form is X a/an Y
    elif AI_Input[0] == 'is' and (AI_Input[2]== 'a' or AI_Input[2] == 'an'):
        #print("is X a/an Y")
        checkIsQuestion(AI_Input[1], AI_Input[3], AI_Input[2])
    # print confused if input of length 4 is malformed
    else:
        print("I am confused")

# A function that handles inputs of length 3
def process_input3(AI_Input):
    # if input is of the form what is X
    if AI_Input[0] == 'what' and AI_Input[1] == 'is':
        print("what is X")
    # if input is of the form are X Ys
    elif AI_Input[0] == 'are':
        print("are X Ys")
    # if input is of the form X are Y
    elif AI_Input[1] == 'are':
        print("Xs are Ys")
        # Add fact to KB if not known
        addFactAre(AI_Input[0], AI_Input[2])
    # if input is "I am leaving."
    elif AI_Input[0] == 'I' and AI_Input[1] == 'am' and AI_Input[2] == 'leaving':
        print("I am leaving")
        sys.exit() # exit program (Need a better way)
    # print confused for outer if statement
    else:
        print("I am confused")

# A function that calls the appropriate functions according to the input and
# determines what it is being told/asked
def process_input(line):
    """ Inputs are of two categories. One category is a fact and of the form:
        1) X is a Y
        2) X are Ys

        The other category is a query and takes these forms:
        3) is X a/an Y
        4) are X Ys
        5) who is a/an Y
        6) what is X (where X is someone/something specific, I.E Fido)

        If an input of the form "I am leaving." is recieved then program
        should terminate. All other inputs that are not facts or queries
        should be handled with 'I am confused' """

    # parse the line and check what is being asked or told
    input1 = line.split()
    length = len(input1)
    # allows us to change global variables
    global clarify_count
    global flag_confused
    # Note: our process_input is incorrect since subjects can be 2 or more people
    if length == 4:  # checks line by length
        # resets confused counter in case the other AI was confused
        # on previous input
        flag_confused = False
        clarify_count = 0
        # process inputs of length 4
        process_input4(input1)
        
    # if length of list is 3
    elif length == 3:
        # if input is "I am unsure"
        if input1[0] == 'I' and input1[1] == 'am' and input1[2] == 'unsure':
            if clarify_count == 3:
                # give up and give another fact
                giveFact()
                clarify_count = 0 # reset counter
            else:
                clarify_unsure()
        # if input is "I am confused"
        elif input1[0] == 'I' and input1[1]== 'am' and input1[2]== 'confused':
            if clarify_count == 3:
                # give up and give another fact
                giveFact()
                clarify_count = 0 # reset counter
            else:
                clarify_confused()
        else:
            # resets confused counter in case the other AI was confused
            # on previous input
            flag_confused = False
            clarify_count = 0
            # process inputs of length 3
            process_input3(input1)
        
    # all other input will need to be checked if malformed or
    # if there is more than one subject in the line
    else:
        flag_confused = False
        clarify_counter = 0
        process_input2(input1)

# the main function
def main():

    """ The main loop of your program. """

    global output # tells program to use global variable
    # start by give a fact
    print("fido is a dog") # fact holder
    output += 1 # increment output counter
    # process each line from standard input
    for line in sys.stdin:
        process_input(line)

        output += 1 # increment output counter
        # terminate program when at least 20 outputs are given
        if output > 20:
            print("I am leaving.")
            break

    
# This executes main() if project4.py was executed at the shell.
# Otherwise, main() will not be called (useful for debugging)..
if __name__ == "__main__":
    main()
