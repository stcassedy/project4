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
facts_given = 0 # counter to keep track of which facts were given

# nouns knowledge base format is a list of a list.  Inner list is of
# the form [singular, plural]. I.E [[person, people], [foot, feet] ...]
nouns = [['dog', 'dogs'], ['animal', 'dogs'],
         ['cat', 'cats'],['mammal', 'mammals'],
         ['student','students'], ['human', 'humans'],
         ['fox', 'foxes'], ['musician', 'musicians']]

# adjective knowledge base
adjectives = []

# questions already asked
askedWhoQ=[]
askedIsQ= []

# knowledge base
fs = dict()

'''
    # all individual's name
    individual = [ ['fido', ''], 'nelly','sally','john', 'kate','mimi','fluffy',
    'lulu','kevin']
    #all category's name
    category = ['dog','animal','cat', 'mammal','student','human','fox','musician']
    
    #individual facts
    fs['fido'] = ['dog','animal']
    fs['nelly'] = ['cat', 'mammal', 'animal']
    fs['sally'] = ['student','human']
    fs['john'] = ['student', 'human']
    fs['kate'] = ['fox', 'animal']
    fs['mimi'] = ['fox','animal']
    fs['fluffy'] = ['cat','mammal','animal']
    fs['lulu'] = ['cat', 'mammal', 'animal']
    fs['kevin'] = ['musician', 'human']
    
    #general facts
    fs['dog'] = ['animal']
    fs['cat'] = ['mammal']
    fs['mammal'] = ['animal']
    fs['student'] = ['human']
    fs['fox'] = ['animal']
    fs['musician']= ['human']
    
    '''
facts = ['fido is an animal','nelly is a cat',
         'sally is a student','a dog is an animal',
         'kevin is a musician','lulu is a cat',
         'cats are fluffy','animals are mammals']

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
    else:
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

# ------------------------------------------------------------------------------
# These functions deal with inference and answering questions.
# If an answer is not known, then the AI can ask a question related to the
# question it was asked, if it can make the connection (I.E for "who is a dog?"
# if it does not know, it can look through the database and pick a random
# person or thing) or it can respond with "I am not sure"
# ------------------------------------------------------------------------------





###########################################################

#reply for isQuestion

def checkIsQuestion(rand_name, word):
    check=False
    values=[]
    values= fs.get(rand_name)
    if(values is not None):
        for ele in values:
            if word == ele:
                check=True
                print(rand_name,'is a/an',word,'.')
	# if kb doesn't have the fact, ask a related query
    if (check==False):
        
        #?????? asked a related questions
        #print('Thanks, I did not know that myself.')
        relatedWhoQuestion(word)

########################################################
#reply for who question

def checkWhoQuestion(word):
    check=False
    count=0
    ct=0
    output=''
    correct_answer=[]
    for name, value in fs.items():
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
        relatedIsQuestion(word)

########################################################





# ------------------------------------------------------------------------------
# These functions deal with asking questions
# Need to think of a way to form questions
# ------------------------------------------------------------------------------

############ related is-question ###################
def relatedIsQuestion(a_object):
    
    rand= random.randint(0,len(individual)-1)
    
    #pick a random number from category
    rand_name= individual[rand]
    
    
    # check whether word is already asked or not
    currQuest= (rand_name,a_object)
    flag= currQuest in askedIsQ
    
    # if yes, get a another random word
    while(flag==True):
        rand= random.randint(0,len(individual)-1)
        
        # check whether word is already asked or not
        currQuest= (rand_name, a_object)
        flag= currQuest in askedIsQ
    
    print('Is', rand_name, 'a/an',a_object,'?')
    askedIsQ.append(currQuest)



############related who-questions##########

def relatedWhoQuestion(a_object):  # or adj ??
    
    # check whether word is already asked or not
    flag= a_object in askedWhoQ
    # if yes, get a another random word
    while(flag==True):
        flag= a_object in askedWhoQ
    
    print('Who is a/an', a_object,'?')
    askedWhoQ.append(a_object)




# ------------------------------------------------------------------------------
# These functions deal with storing knowledge into the database
# Once a fact is stored, the AI should respond with a related question.
# I.E "Dogs are cute" => "what are dogs."  Note that the AI would only need to
# ask about dogs in this case since this fact is of the form X are Y.  It would
# be hard to answer what is an animal or what is cute.
# If a fact is already known, the AI will either give a new fact or query with
# an equal chance of either one happening.
# ------------------------------------------------------------------------------

# This helper function adds the fact into the database
# Note: all facts are stored as singular!
def addFact(subClass, superClass):
    added = False # flag to check whether to ask a query at the end
    # Look for the subClass in the KB
    # things is everything the person or thing is
    for name, things in fs.items():
        # if found, check if the superclass is attached to the subclass
        if name == subClass:
            if superClass in things:
                added = True
                # if fact is known, then give new fact or query
                if random.randint(0,1):
                    #randomly choose a fact
                    print(facts.pop(random.randint(0,len(facts)-1)))
                else:
                    #randomly create a query
                    temp = random.sample( fs.keys(),1)
                    print("what is "+temp[0]+"?")
            else:
                added = True
                temp = fs[subClass]
                temp.append(superClass)
                fs[subClass] = temp
                print("what is the plural of "+ superClass +"?") #temporary
    # if fact is not known, attach it to the subclass
    # check whether superClass is a noun/adjective, why?
    # give related query (who question related to superclass)
    # if the subClass was not found as the starting as the "key" add to KB
    if not added:
        fs[subClass] = superClass.split() #add it as a list
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
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Main function and helper functions that help parse the input
# ------------------------------------------------------------------------------

# A function that handles inputs of length 4
def process_input4(AI_Input):
    # if input is of the form who is a/an Y
    if AI_Input[0] == 'who' and AI_Input[1] == 'is':
        # had to put rest of conditional on a new line
        if AI_Input[2] == 'a' or AI_Input[2] == 'an':
            checkWhoQuestion(AI_Input[3])
        # Print statement here because it skips the other one at
        # end in case of malform input
        else:
            print("I am confused")
    # if input is of the form X is a/an Y
    elif AI_Input[1] == 'is' and (AI_Input[2] == 'a' or AI_Input[2] == 'an'):
        # helper function that adds the fact to KB if not known
        addFact(AI_Input[0], AI_Input[3])
    # if input is of the form is X a/an Y
    elif AI_Input[0] == 'is' and (AI_Input[2]== 'a' or AI_Input[2] == 'an'):
        print("is X a/an Y")
        checkIsQuestion(AI_Input[1], AI_Input[3])
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
        print("X are Ys")
        # Add fact to KB if not known
        addFact(AI_Input[0], AI_Input[2])
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
    AI_Input = line.split()
    length = len(AI_Input)
    if length == 4:  # checks line by length
        process_input4(AI_Input)
    elif length == 3:  # if length of list is 3
        process_input3(AI_Input)
    # all other input will be answered with "I am confused"
    else:
        print("I am confused")

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
# Otherwise, main() will not be called (useful for debugging).
if __name__ == "__main__":
    main()
