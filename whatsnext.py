import re
import random
from datetime import datetime
#NOTE:
#FIX RANDOM FUNCTION
#READJUST WEIGHTS AFTER PRINTING
#ADD BACKWARD N TOKENIZATION TOO

#Basic string declarations
alphabets='’abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
punctuations='\'(",.;)”“'

#Declaration of dictionary 'follow' -- stores what string(value) follows another string(key)
follow={}

#Function to tokenize the training set -- takes in a parameter, the directory of the txt file.
#Returns a list of tokens extracted from training set
def tokenize(training_set_dir):
    tok=[]                                                                  #initialize temporary token list
    buf=''                                                                  #initialize buffer string
    training_set=''                                                         #initialize string to store read in text
    with open(training_set_dir,'r') as f:                                   #open file
        for words in f:                                                     #iterate over file
            if len(words)>0:                                                #if its a valid word
                training_set+=words                                         #append it to training set string
    
    for i in training_set:                                                  #iterate over training set string
        if i==' ':                                                          #if currently at a space
            if len(buf)>0 and buf!=' ' and buf!='':                         #if buffer string is a valid word
                tok.append(buf)                                             #append to token list
            buf=''                                                          #reassign buf as empty
        elif i in alphabets:                                                #else if its an alphabet
            buf+=i                                                          #concatenate to buffer string
        elif i in punctuations:                                             #else if its a punctuation
            tok.append(buf)                                                 #append to token list
            buf=''                                                          #reset buf
            if i=='”':                                                      #if its a closing quote
                tok.append(i+'\n')                                          #add new line symbol after it
            else:
                tok.append(i)                                               #else dont
        else:
            continue                                                        #else go to next word
    tokens=[]                                                               #initialize final token list
    for i in tok:                                                           #iterate over temporary token list
        if i!='' and i!='”' and i!='“' and i!='”\n':                        #if its a valid string
            tokens.append(i)                                                #append to final tokens
    return tokens                                                           #return tokens



#Function to construct the n-token follow dictionary
#returns a dictionary storing which words follow which words and how many times they do so
def construct(n=1):                                                         #look n-tokens ahead
    global follow                                                           #reference the global dictionary for internal use
    tokens=tokenize(input('Enter training set directory: '))                #obtain tokens
    keys=[]                                                                 #init keys of follow
    for i in range(len(tokens)-n+1):                                        #generate keys
        keys.append(' '.join(tokens[i:i+n]))
    keys=list(set(keys))                                                    #make keys unique
    
    #dictogram={}                                                           #init dict to store number of occurrences of keys
    #for i in keys:                                                         #in hindsight, this dictionary 'dictogram' isnt used.
    #    dictogram[i]=tokens.count(i)                                       #REDUNDANT
    
    for i in range(len(tokens)):                                            #Iterate over tokens
        follow[tokens[i]]={}                                                #initialize follow's keys

    for i in range(len(tokens)):                                            #Re-iterate over tokens
        if i+n<len(tokens):                                                 #if n-tokens ahead of current point
            follow[tokens[i]][' '.join(tokens[i+1:i+n])]=0                  #initialize dictionary value to zero
    
    for i in range(len(tokens)):                                            #Over all tokens
        if i+n<len(tokens):                                                 #if n-tokens ahead
            follow[tokens[i]][' '.join(tokens[i+1:i+n])]+=1                 #increment frequency of occurrences

    follow['--START--']={}                                                  #Assign starting point same as follow of full stop
    follow['--START--']=follow['.']
    follow['.']['--END--']=50                                               #Weight the probability of ending the statement higher

def transition(string,n=1,depth=1,limit=50):
    if depth>limit and string in follow:
        print('.')
        return
    if string in follow:
        follow_words=list(follow[string].keys())
        follow_occur=list(follow[string].values())
        
        cum_probs=[follow_occur[0]/sum(follow_occur)]
        for i in range(1,len(follow_occur)):
            cum_probs.append(cum_probs[i-1]+ follow_occur[i]/sum(follow_occur))
        cum_probs.append(1)
        random_ind=random.randint(0,len(follow[string].keys())-1)
        random_ind/=sum(follow_occur)
        ind=0
        for i in range(len(cum_probs)-1):
            if random_ind>=cum_probs[i] and random_ind<cum_probs[i+1]:
                ind=i
                break

        print(follow_words[ind],end=' ')
        transition(follow_words[ind],n,depth+1,limit)
    else:
        transition('.',n,depth+1,limit)

def run():
    n=int(input("Enter size of histogram: "))
    n+=1
    depth_limit=int(input('Enter recursive depth: '))
    construct(n)
    transition('.',n,1,depth_limit)

#run()
