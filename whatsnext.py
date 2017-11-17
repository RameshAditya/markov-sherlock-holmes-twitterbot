import re
import random
from datetime import datetime
import time as time
#Basic string declarations
alphabets='’abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
punctuations='\'(",;)”“'
final_output=''

#Declaration of dictionary 'follow' -- stores what string(value) follows another string(key)
follow={}

#Function to return the current time in milliseconds

def millis():
    return int(round(time.time() * 1000))

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
        if i in punctuations:
            continue
        if i==' ' or i=='.':                                                #if currently at a space
            if len(buf)>0 and buf!=' ' and buf!='':                         #if buffer string is a valid word
                tok.append(buf)                                             #append to token list
            if i=='.':
                tok.append('.')
            buf=''                                                          #reassign buf as empty
        elif i in alphabets:                                                #else if its an alphabet
            buf+=i                                                          #concatenate to buffer string
    tokens=tok
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
    
    for i in range(len(tokens)):                                            #Iterate over tokens
        if i+n<len(tokens):
            for j in range(0,n):
                follow[' '.join(tokens[i+j:i+n])]={}                        #initialize follow's keys

    for i in range(len(tokens)):                                            #Re-iterate over tokens
        if i+n<len(tokens):                                                 #if n-tokens ahead of current point
            for j in range(0,n):
                follow[' '.join(tokens[i+j:i+n])][tokens[i+n]]=0            #initialize dictionary value to zero
    
    for i in range(len(tokens)):                                            #Over all tokens
        if i+n<len(tokens):                                                 #if n-tokens ahead
            for j in range(0,n):
                follow[' '.join(tokens[i+j:i+n])][tokens[i+n]]+=1           #increment frequency of occurrences
    
    
def transition(string,n=1,depth=1,limit=50):
    global final_output
    if depth>limit:
        final_output+='. '
        return
    if string in follow:
        follow_words=list(follow[string].keys())
        follow_occur=list(follow[string].values())
        
        cum_probs=[0]
        cum_probs.append(follow_occur[0])

        for i in range(1,len(follow_words)):
            cum_probs.append(cum_probs[i-1]+follow_occur[i])
        
        random_ind=millis() % len(follow_words)
        ind=0
        for i in range(1,len(follow_words)+1):
            if random_ind>=cum_probs[i-1] and random_ind<=cum_probs[i]:
                ind=i-1
                break
        final_output+=follow_words[ind]+' '

        ct=0
        i=0

        while i<(len(string)):
            if ' '.join(string.split(" ")[i:])+follow_words[ind] in list(follow.keys()):
                ct=1
                break
            i+=1
        transition(' '.join(string.split(" ")[i:])+follow_words[ind],n,depth+1,limit)
    else:
        transition(list(follow.keys())[random.randint(0,len(list(follow.keys()))-1)],n,1,limit)

def run():
    final_output=''
    n=int(input("Enter size of histogram: "))
    depth_limit=int(input('Enter recursive depth: '))
    construct(n)
    transition(list(follow.keys())[random.randint(0,len(follow.keys())-1)],n,1,depth_limit)
    

run()
