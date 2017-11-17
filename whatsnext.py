import re
import random
from datetime import datetime
import time as time
import tweepy
import csv

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


#Twitter tweepy stuff
auth=tweepy.OAuthHandler('YyOFVAjYklqyXXXXXXXXX','XXXXXXXXXXXXXXXXXXXXXXxqIiPkrXWhbQMrDDYfJB')
auth.set_access_token('9249194698XXXXXXXXXXXXXXXXXXXXXf','RXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXHnPNBppR0UbheKf')

api=tweepy.API(auth)


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
    tokens=tokenize('A:/markov.txt')                                        #obtain tokens
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


#Function to transition from one token to the next token

def transition(string,order=1,depth=1,limit=50):                                #Parameters
    global final_output                                                         #Declare use of global string final_output
    if depth>limit:
        final_output+='. '                                                      #End recursion if limit is exceeded
        return
    if string in follow:                                                        #If the given string is a key in follow{}
        follow_words=list(follow[string].keys())                                #Obtain the next possible words
        follow_occur=list(follow[string].values())                              #Obtain the probabilites of the next possible words
        
        cum_probs=[0]                                                           #Declare list 'cum_probs': cumulative probabilities
        cum_probs.append(follow_occur[0])                                       #Append probability of first next token


        #Basically, we're appending likelihoods of next occurrences, and taking a random number and finding
        #which segment it falls within, and picking the corresponding production.
        #This method ensures that our next token is probabilistically likely to be more meaningful.
        for i in range(1,len(follow_words)):                                    
            cum_probs.append(cum_probs[i-1]+follow_occur[i])                    #Generate cumulative probs

        
        random_ind=millis() % len(follow_words)                                 #Generate random number using system time
        ind=0                                                                   #Declare final index
        for i in range(1,len(follow_words)+1):                                  #Iterate over all following words
            if random_ind>=cum_probs[i-1] and random_ind<=cum_probs[i]:         #If the bucket has been found where the random number lies in
                ind=i-1                                                         #Select the corresponding following token
                break
        final_output+=follow_words[ind]+' '                                     #Concatenate it to final string

                                                                                #Time to move on to next token of given order
        transition(' '.join(string.split(" ")[i:])+follow_words[ind],order,depth+1,limit)

                                                                                #If current token does not exist, exception handle
    else:
        transition(list(follow.keys())[millis() % len(follow.keys())],order,1,limit)

#Function to execute the above functions

def run():
    final_output=''                                                             #Final string
    #n=int(input("Enter order: "))                                               #Obtain order of histogram
    n=1
    depth_limit=500
    #depth_limit=int(input('Enter maximum depth of recursion: '))                #Obtain depth limit of recursion
    construct(n)                                                                #Invoke construction function
    transition(list(follow.keys())[millis() % len(follow.keys())],n,1,depth_limit) #Begin recursive descent


#Function to generate the actual tweets

def whats_next():
    run()                                                                       #Invoke run function
    ans=''
    ans+=final_output[0].upper()
    ans+=final_output[1:min(219,max(60,final_output.index('.')+1))]
    if ans[len(ans)-1]==' ' and ans[len(ans)-1]!='.':
        ans+='...'
    else:
        ans+='-'
    api.update_status(ans)
whats_next()
