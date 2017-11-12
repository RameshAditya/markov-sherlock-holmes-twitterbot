import re
import random
from datetime import datetime
#FIX RANDOM FUNCTION
#READJUST WEIGHTS AFTER PRINTING
alphabets='’abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
punctuations='\'(",.;)”“'

def tokenize(training_set_dir):
    tok=[]
    buf=''
    training_set=''
    with open(training_set_dir,'r') as f:
        for words in f:
            if len(words)>0:
                training_set+=words
    #Tokenizing
    for i in training_set:
        if i==' ':
            if len(buf)>0 and buf!=' ' and buf!='':
                tok.append(buf)
            buf=''
        elif i in alphabets:
            buf+=i
        elif i in punctuations:
            tok.append(buf)
            buf=''
            if i=='”':
                tok.append(i+'\n')
            else:
                tok.append(i)
        else:
            continue
    tokens=[]
    for i in tok:
        if i!='' and i!='”' and i!='“' and i!='”\n':
            tokens.append(i)
    return tokens
follow={}
def construct(n=1):   #n sized histogram
    global follow
    tokens=tokenize(input('Enter training set directory: '))
    keys=[]
    for i in range(len(tokens)-n+1):
        keys.append(' '.join(tokens[i:i+n]))
    keys=list(set(keys))
    dictogram={}
    for i in keys:
        dictogram[i]=tokens.count(i)
    
    for i in range(len(tokens)):
        follow[tokens[i]]={}

    for i in range(len(tokens)):
        if i+n<len(tokens):
            follow[tokens[i]][' '.join(tokens[i+1:i+n])]=0
    
    for i in range(len(tokens)):
        if i+n<len(tokens):
            follow[tokens[i]][' '.join(tokens[i+1:i+n])]+=1 #Change 2nd [i+1] to [i+2] for 2-histogram here and in prev loop

    follow['--START--']={}
    follow['--START--']=follow['.']
    follow['.']['--END--']=50

def transition(string,n=1,depth=1,limit=50):
    #if string not in follow:
     #   print('\n-X-\n')
      #  return
    if depth>limit and string in follow: #Added commit
        print('.')
      #  ct+=1
        return
    if string in follow:
        '''
        if string in '\'(",.;)”“':
            print('',end='')
        
        else:
            print('',end='')
        '''
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

        '''
        if follow_words[ind] in '\'(",.;)”“':
            print(follow_words[ind],end=' ')
        else:
            print(follow_words[ind],end=' ')
        '''

        print(follow_words[ind],end=' ')
        #print('\n',str(follow[string].keys()).split(", ")[2].strip('\''))
        transition(follow_words[ind],n,depth+1,limit)
    else:
        transition('.',n,depth+1,limit)

def main():
    print("Enter size of histogram: ",end='')
    n=int(input())
    n+=1
    depth_limit=int(input('Enter recursive depth: '))
    construct(n)
    transition('.',n,1,depth_limit)

main()
