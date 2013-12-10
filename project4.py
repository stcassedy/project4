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
#a_an="a/an" # it needs to be one or the other in the correct circumstance

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
          'alien','mammal','idiot','dog','cat']

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
    #if nouns.count([single,plural]) == 0:
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
    added = True
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

        if key == thing and KB.get(key)[0].count(what_thing_is) > 0:
            added = False
            
        #adds what_thing_is if thing is already in the knowledge base
        if key == thing and KB.get(key)[0].count(what_thing_is) == 0:
            KB.get(key)[0].append(what_thing_is)
            append_sublist(sublist_is,KB.get(key)[0])
            append_sublist(sublist_adj,KB.get(key)[1])
            append_sublist(sublist_verb,KB.get(key)[2])
            append_sublist(sublist_prep,KB.get(key)[3])
            append_sublist(sublist_poss,KB.get(key)[4])
            
        #updates everything that is a thing with thing's information
        if KB.get(key)[0].count(thing) > 0:
            KB.get(key)[0].append(what_thing_is)
            append_sublist(sublist_is,KB.get(key)[0])
            append_sublist(sublist_adj,KB.get(key)[1])
            append_sublist(sublist_verb,KB.get(key)[2])
            append_sublist(sublist_prep,KB.get(key)[3])
            append_sublist(sublist_poss,KB.get(key)[4])
    
    #returns if KB was updated or not
    return added

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
# if it doesn't know the plural it will add an S
# if it doesn't know the singular it will remove the last letter
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
    for noun in nounList: # for each noun in list passed in
        for pair in nouns: # for each pair of nouns (sing, plur) in KB
            if pair[check] == noun:
                c_list.append(pair[index])
                break
            # if no plural/singular was found
            elif pair == nouns[len(nouns)-1]:
                # add an S to the end
                if inType == 'S':
                    c_list.append(noun+'s')
                # remove the last letter (assumed to be s)
                else:
                    c_list.append(noun[0:len(noun)-1])
    # return the list
    return c_list

# A function that prints a list to std.out
def print_list(inList):
    for index in range(0, len(inList)):
        if index == len(inList)-1:
            print(inList[index])
        else:
            print(inList[index], end =" ")

# A function that removes punctuation marks
def remove_punc(word):
    newWord = word
    for index in range(0,len(word)):
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

'''
def pickRandomRelatedQuestion(){
    rand= random.randint(0,3)
    if(rand==0): relatedToIsQuestion(x_value, y_value):
    if(rand==1):relatedToIsQuestion()
    if(rand==2):relatedToIsQuestion()
    if(rand==3):relatedToIsQuestion()

    }
    '''
#reply for isQuestion 

def checkIsQuestion(name, a_an, aThing):
    
    check=False
    values=[]
    if name in individual:
        values= KB[name][0]
    if(values is not None):
        
        for ele in values:
            if aThing == ele:
                check=True
                aThing2 = aThing+'.'
                return [name,'is',a_an ,aThing2]
# if kb doesn't have the fact, ask a related query
    if (check==False):  
        # 50/50 chance to give related query or respond I am unsure
        rand= random.randint(0,1)
        if(rand==0):
            return relatedToIsQuestion(name,a_an,aThing)
        else:
            return ['I', 'am', 'unsure']
        


  

########################################################
#reply for who question

def checkWhoQuestion(is_are,a_an,word):
    count=0
    ct=0
    output=[]
    temp_reselt='';
    correct_answer=[]
    properties=[]
    for name, value in KB.items():
       
        #properties=value[0]
        if word in value[0]:
            if name in individual:
                correct_answer.append(name)
                #print(correct_answer)
                count+=1

    if(count !=0):
        if(count ==1):
            # if there are several answers for who is a Y, we just pick the first one
            if(is_are=='are'):
                output= [correct_answer.pop(0)]
                word2 = word+'.'
                return [output[0],'is','a',word2]
            else:
                output= [correct_answer.pop(0)]
                word2 = word+'.'
                return [output[0],'is',a_an,word2]
        else:
            # if there are several answers for who is a Y, we just pick the first one
            if(is_are=='is'):
                output= [correct_answer.pop(0)]
                word2 = word+'.'
                return [output[0],'is',a_an,word2]
                
            while(ct !=count):
                if(ct == count-1):
                    temp_reselt+=( ' and ' )
                    #output.append( ' and ' )
                    temp_reselt+=correct_answer.pop(0)
                    #output.append(correct_answer.pop(0))
                else:
                    temp_reselt+=( ', ' )
                    #output.append(', ')
                    temp_reselt+=correct_answer.pop(0)
                    #output.append(correct_answer.pop(0))
                ct+=1
                
            temp_reselt+=' are '+ word+'s.'
            
            output=temp_reselt.split(',')
            return  output  
# if kb doesn't have the fact, ask a related query
    if(output==[]):
       # 50/50 chance to ask question or reply i am unsure
       rand= random.randint(0,1)
       if(rand==0):
            return relatedToWhoQuestion(a_an,word)
       else:
            return ['I', 'am', 'unsure']
       
   
########################################################

# A function that answers questions of the form "what is/are X"
# This function only returns one thing (rather than multiple)
# Need to implement this when time permits
def checkWhatQuestion(aThing):
    # variable to hold the properties of aThing
    properties = None
    # variable to store our response to the what is X question
    response = []
    # if this person or thing is known
    if aThing in individual:
        properties = KB[aThing]
    # if this category is known
    elif aThing in category:
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
        # Check if we're giving facts about X, then just give the next fact
        keys = sorted(KB.keys())
        if aThing == keys[fact_key]:
            xIs = values[fact_value]
            # updates global counter
            fact_value += 1
        # else give the last fact about X
        else:
            xIs = values[len(values)-1]
        # updates response base on if X is an individual or category
        if aThing in individual:
            response = [aThing, 'is', 'a', xIs]
        else:
            # converts noun to plural
            plural = convert([xIs],'S')
            response = [aThing, 'are', plural[0]]
    return response

# A function that answers questions of the form "Are X Y"
def checkAreQuestion(aThing, inCategory):
    # stores the response in a variable
    response = []
    # switches X and Y from plural to singular
    singular = convert([aThing, inCategory], 'P')
    # look for X in the list of keys
    properties = None
    # if this category (X) is known
    if singular[0] in category:
        properties = KB[singular[0]]
    # If X is not in the database
    if properties == None:
        # 50% chance to say unsure or give related query/fact
        response = ['I', 'am', 'unsure']
    else:
        # stores list of what X is
        values = properties[0]
        # check if X has Y in its property list
        if singular[1] in values:
            response = [aThing, 'are', inCategory]
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

# note if recieving fact is should ask a follow up question
# like who is a Y (which it does not)

def relatedToIsQuestion(x_value,a_an, y_value):
    rand= random.randint(0,1)
    if(rand==0):
        word = x_value+'?'
        if(x_value in individual):
            #askedWhoQ.append(x_value)
            return ['Who', 'is', a_an, word]
        else:
            #askedWhatQ.append(x_value)
            return ['What', 'is', word]
    else:
        word = y_value+'?'
        if(y_value in category):
            #askedWhatQ.append(y_value)
            return ['What', 'is', a_an, word]            
        else:
            #askedWhoQ.append(y_value)
            return ['Who','is',a_an, word]
            
            
############related who-questions##########
# A function that asks a related question to "who is a/an Y"
# The AI will take a guess, so it will ask "is X a/an Y"
# where X is a randomly chosen specific person or thing

def relatedToWhoQuestion(a_an,a_object): 
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

    word = a_object+'?'
    return ['Is', rand_name, 'a',word]
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

    word = aThing+'?'
    return ['Is', rand_name, 'a/an',word]
    askedIsQ.append(currQuest)
    
# A function that asks a related question to "are X Ys"
# or if it recieves a fact of the form X are Ys

# Note when asking about a related fact, check if X is an individual or category
# if X is an individual it should ask is X a/an Ys
# if X is a category it should ask are X Ys
# but this asks a question we know the answer to... just ask what is Y?
def relatedAreQuestion(aThing2):
    word = aThing2+'?'
    #askedWhatQ.append(aThing)
    return ['What', 'are', word]
    #rand= random.randint(0,1)
    #if(rand==0):
    #    word = aThing+'?'
    #    return ['What', 'are', word]
    #    askedWhatQ.append(aThing)
    #else:
    #    word = aThing2+'?'
    #    return ['What','are',word]
    #    askedWhatQ.append(aThing2)

# A function that takes a guess as to what aThing could be
# this returns a related query
def guessAreQuestion(aThing):
    # get the keys
    keys = list(KB.keys())
    # pick a key that is a category
    key = keys[random.randint(0,len(keys)-1)]
    while not (key in category):
        key = keys[random.randint(0,len(keys))]
    # key needs to be changed to plural since this is an are question
    plural = convert([key], 'S')
    # when a key is found ask if this key is aThing
    word = aThing+'?'
    return ['Are', plural[0], word]
        

    	


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
    keys = sorted(KB.keys())
    key = keys[fact_key]
    # get properties of the thing we're looking at
    properties = KB[key]
    values = properties[0] # list of what person/category is, is in 1st index
    # key can have no properties, if this is the case, a new key must be chosen
    while values == []:
        fact_key += 1
        # if end of list
        if fact_value > len(values)-1:
            # reset value counter
            fact_value = 0
            fact_key += 1
            # if at the end of DB
            if fact_key > len(keys)-1:
                fact_key = 0 # start from very beginning
        # check which key we are on
        key = keys[fact_key]
        # get properties of the thing we're looking at
        properties = KB[key]
        # list of what person/category is, is in 1st index
        values = properties[0]
    # determine if the key is a person or category
    if key in individual:
        # If its a person
        # >>>> NEED TO CHECK WHETHER TO USE A/AN <<<<<<<
        print(key + ' is' + ' a ' + values[fact_value])
        # update global counter
        prev_output = [key, 'is', 'a', values[fact_value]]
    else:
        # swap from singular to plural
        plurals = convert([key, values[fact_value]], 'S')
        # If its a general category
        print(plurals[0] + ' are ' + plurals[1])
        # update what previous output was
        prev_output = [plurals[0], 'are', plurals[1]]
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

# This function stores a fact of the form Xs are Ys
# This function is needed because X and Y are plural
# subClass is the lower class (I.E dogs)
# superClass is the general category (I.E animal)
def addFactAre(subClass, superClass):
    # change subClass and superClass into singular nouns
    # >>>NOTE: need to catch adjectives somehow!
    singList = convert([subClass, superClass], 'P')
    # inserted is true if fact was added
    plural = convert([superClass], 'S')
    return relatedAreQuestion(plural[0])


# This function stores fact of the form X is a Y
# This function is needed because Y is singular
# subClass is the lower class (I.E fido)
# superClass is the more general category (I.E Dog in this case)
def addFactIs(person, superClass):
    # call helper function to add fact into database, no change needed
    inserted = update_KB_is(person, superClass)
    # whether or not a new fact was added, it should ask what are Ys
    # since asking about X can only go in one direction and the other
    # AI might just repeat X is a Y which is something we don't want
    # We could/should ask about plurals here instead
    # convert to plural
    plural = convert([superClass], 'S')
    return relatedAreQuestion(plural[0])





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
    global prev_output
    # variables to hold all the information
    people = []
    categories = []
    # gives a related fact depending on the form of the fact give
    # if fact is of the form X is a Y
    # Note answering what question doesn't give more than one answer
    # so it doesn't have to handle forms that have more than 1 Y at the moment
    if prev_output[1] == 'is' and (prev_output[2]=='a' or prev_output[2]=='an'):
        # give the next fact (which is usually related)
        giveFact()
    # if fact is of the form X are Ys
    elif prev_output[1] == 'are':
        line = prev_output[0].split()
        # check this form has multiple subjects
        if len(line) > 1:
            parseAre(output[0],people,categories)
            # use one of the people from people list
            prev_output = [people[0], 'are', prev_output[2]]
            print_list(prev_output)
        # this form is literally X are Ys
        else:
            giveFact()
            # ask a related are question
            #answer = relatedAreQuestion(prev_output[0],prev_output[2])
            # need this so prev_output doesnt get over written too early
            #prev_output = answer
            #print_list(prev_output)
    clarify_count += 1 # increment try counter



# this function attempts to clarify by outputing another related query
# when the other AI is confused after hearing a fact. it gives up after 3 tries
def clarify_unsure():
    # gives us permission to change global variable
    global clarify_count
    global prev_output
    clarify_count += 1
    # If other AI is unsure who is a/an X, our AI should answer the question
    if prev_output[0] == 'Who' and prev_output[1] == 'is':
        # answer the question
        answer = checkWhoQuestion(prev_output[1], prev_output[2],prev_output[3])
        # if no answer was found
        if answer[0] == 'I' and answer[1] == 'am' and answer[2] == 'unsure':
            # ask a related question
            answer = relatedToWhoQuestion(prev_output[2],prev_output[3])
        # print response
        print_list(answer)
        prev_output = answer
        prev_output[len(prev_output)-1] = remove_punc(prev_output[len(prev_output)-1])
        
            
    # If other AI is unsure what is/are X, our AI will answer the question
    elif prev_output[0]=='What'and(prev_output[1]=='is'or prev_output[1]=='are'):
        # answer the question
        answer = checkWhatQuestion(prev_output[2])
        # if no answer was found
        if answer[0] == 'I' and answer[1] == 'am' and answer[2] == 'unsure':
            answer = guessAreQuestion(prev_output[2])
        # print response
        print_list(answer)
        prev_output = answer
        prev_output[len(prev_output)-1] = remove_punc(prev_output[len(prev_output)-1])
            
    # If other AI is unsure if X is a Y
    elif prev_output[0]=='Is': #and (prev_output[2]=='a' or prev_output[2]=='an'):
        # answer the question
        answer = checkIsQuestion(prev_output[1], prev_output[2],prev_output[3])
        # if no answer was found
        if answer[0] == 'I' and answer[1] == 'am' and answer[2] == 'unsure':
            # give related question
            answer = relatedToIsQuestion(prev_output[1],prev_output[3])
        # print response
        print_list(answer)
        prev_output = answer
        prev_output[len(prev_output)-1] = remove_punc(prev_output[len(prev_output)-1])
            
    # If other AI is unsure if X are Y's
    elif prev_output[0] == 'Are':
        # answer the question
        answer = checkAreQuestion(prev_output[1], prev_output[2])
        # if no answer was found
        if answer[0] == 'I' and answer[1] == 'am' and answer[2] == 'unsure':
            # give related question
            answer = guessAreQuestion(prev_output[2])
        # print response
        print_list(answer)
        prev_output = answer
        prev_output[len(prev_output)-1] = remove_punc(prev_output[len(prev_output)-1])
        
    # if you are here, then other AI is unsure of a fact
    else:
        clarify_confused()






# ------------------------------------------------------------------------------
# Main function and helper functions that help parse the input
# ------------------------------------------------------------------------------

# a function that parses the the line and stores the nouns/people/things
# into a list that is passed by a parameter.
# people is a list of people or things with names
# categories are the general categories of things (I.E. dog)
# this is for inputs of the form X is a Y and Z (or Y, Z, and V (etc))
def parseIs(line, people, categories):
    # there should only be one subject
    people.append(line[0])
    # iterate through line list and get all categories
    for index in range(3, len(line)):
        # if this word is 'a' do nothing
        if line[index] == 'a':
            continue #do nothing
        # if this word is 'and', we only have one more category to add
        elif line[index] == 'and':
            # the location of this category in the list is 2 spaces ahead
            categories.append(word)
            break
        # any other word is added as a category
        else:
            # removed the comma if it contains it
            word = remove_punc(line[index])
            categories.append(word)

# a function that parses the the line and stores the nouns/people/things
# into a list that is passed by a parameter.
# people is a list of people or things with names
# categories are the general categories of things (I.E. dog)
# this is for inputs of the form X is a Y and Z (or Y, Z, and V (etc))
def parseAre(line, people, categories):
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
            people.append(person)
    # stores the category into the list
    categories.append(line[len(line)-1])
    

# A function that process the input depending on new restrictions
# If the program reaches here then either malformed input was recieved
# or input with more than one subject was recieved
# breaks on trick inputs (I.E using is/a/and/are as names will cause confusion)
# Example form:  Josh is a student and a TA
# Example Form2: Josh and Emily are TAs
def process_input2(line):
    people = []
    categories = []
    query = [] # question that will be asked about a fact recieved
    new_fact = [] # remembers a new fact that has been added
    # check if line contains is
    if line[1] == 'is' and line[2] == 'a' and ('and' in line):
        parseIs(line, people, categories)
        # after everything has been added, add all these facts to DB
        # directly, so it doesnt give a response
        for index in range(0, len(categories)-1):
            inserted = update_KB_is(people[0], categories[index])
            # if fact was not known, then it was inserted
            if inserted:
                new_fact = [people[0], categories[index]]
        # if no new facts were given, then ask a question about an old fact
        plural = convert([categories[0]], 'S')
        new_fact = [people[0], plural[0]]
        # give a related query to a new fact that has been added
        query = relatedAreQuestion(new_fact[1])

    # if line has an 'are' in it (josh and emily are TAs)
    elif line[len(line)-2] == 'are' and ('and' in line):
        # there are more than one subject but only one category
        parseAre(line, people, categories)
        # add all the facts into DB
        for index in range(0,len(people)-1):
            inserted = update_KB_is(people[index],categories[0])
            if inserted:
                new_fact = [people[index], categories[0]]
        # give a related query to the new fact that has been added
        query = relatedAreQuestion(new_fact[1])

    # all other input are considered malform input
    else:
        query = ['i', 'am', 'confused']
    # update prev_output and print query
    global prev_output
    prev_output = query
    print_list(query)
                

# A function that handles inputs of length 4
def process_input4(AI_Input):
    global prev_output
    response = []
    # if input is of the form who is a/an Y
    if AI_Input[0] == 'Who' and AI_Input[1] == 'is':
        # had to put rest of conditional on a new line
        if AI_Input[2] == 'a' or AI_Input[2] == 'an':
            response = checkWhoQuestion(AI_Input[1],AI_Input[2],AI_Input[3])
        # Print statement here because it skips the other one at
        # end in case of malform input
        else:
            response = ['I', 'am', 'confused']
    # if input is of the form X is a/an Y
    elif AI_Input[1] == 'is' and (AI_Input[2] == 'a' or AI_Input[2] == 'an'):
        # helper function that adds the fact to KB if not known
        response = addFactIs(AI_Input[0], AI_Input[3])
    # if input is of the form is X a/an Y
    elif AI_Input[0] == 'Is' and (AI_Input[2]== 'a' or AI_Input[2] == 'an'):
        response = checkIsQuestion(AI_Input[1],AI_Input[2], AI_Input[3])
    # print confused if input of length 4 is malformed
    else:
        response = ['I', 'am', 'confused']
    prev_output = response
    print_list(response)

# A function that handles inputs of length 3
def process_input3(AI_Input):
    global prev_output
    response = []
    # if input is of the form what is/are X
    if AI_Input[0] == 'What':
        # if form is what is X
        if AI_Input[1] == 'is':
            response = checkWhatQuestion(AI_Input[2])
        # if form is what are X
        elif AI_Input[1] == 'are':
            # switch from plural to singular
            singular = convert([AI_Input[2]], 'P')
            response = checkWhatQuestion(singular[0])
        # form is malformed
        else:
            response = ['I', 'am', 'confused']
    # if input is of the form Who are Xs
    elif AI_Input[0] == 'Who' and AI_Input[1] == 'are':
        # convert X to a singular
        singular = convert([AI_Input[2]], 'P')
        response = checkWhoQuestion(AI_Input[1],'',singular[0])
    # if input is of the form are X Ys
    elif AI_Input[0] == 'Are':
        response = checkAreQuestion(AI_Input[1], AI_Input[2])
    # if input is of the form X are Y
    elif AI_Input[1] == 'are':
        # Add fact to KB if not known
        response = addFactAre(AI_Input[0], AI_Input[2])
    # if input is "I am leaving."
    elif AI_Input[0] == 'I' and AI_Input[1] == 'am' and AI_Input[2] == 'leaving':
        print("I am leaving")
        sys.exit() # exit program (Need a better way)
    # print confused for outer if statement
    else:
        response = ['I', 'am', 'confused']
    prev_output = response
    print_list(response)
    response[len(response)-1] = remove_punc(response[len(response)-1])

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
    # removes puncuation from last word
    input1[len(input1)-1] = remove_punc(input1[len(input1)-1])
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
    giveFact()
    output += 1 # increment output counter
    # process each line from standard input
    for line in sys.stdin:
        process_input(line)
        output += 1 # increment output counter

        # test to make sure prev_output is updating correctly
        print("printing previous to make sure its updating")
        print_list(prev_output)
        
        # terminate program when at least 20 outputs are given
        if output > 20:
            print("I am leaving.")
            break
    
# This executes main() if project4.py was executed at the shell.
# Otherwise, main() will not be called (useful for debugging)..
if __name__ == "__main__":
    main()
