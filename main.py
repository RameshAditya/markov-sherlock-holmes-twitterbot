import re
import random
from datetime import datetime
#training_set='Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. They were the last people you’d expect to be involved in anything strange or mysterious, because they just didn’t hold with such nonsense.Mr. Dursley was the director of a firm called Grunnings, which made drills. He was a big, beefy man with hardly any neck, although he did have a very large mustache. Mrs. Dursley was thin and blonde and had nearly twice the usual amount of neck, which came in very useful as she spent so much of her time craning over garden fences, spying on the neighbors. Dursleys had a small son called Dudley and in their opinion there was no finer boy anywhere. Dursleys had everything they wanted, but they also had a secret, and their greatest fear was that somebody would discover it. the boy who lived past in broad daylight, though people down in the street did; they pointed and gazed open-mouthed as owl after owl sped overhead. Most of them had never seen an owl even at night time. Mr. Dursley, however, had a perfectly normal, owl-free morning. He yelled at five different people. He made several important telephone calls and shouted a bit more. He was in a very good mood until lunchtime, when he thought he’d stretch his legs and walk across the road to buy himself a bun from the bakery. He’d forgotten all about the people in cloaks until he passed a group of them next to the baker’s. He eyed them angrily as he passed. He didn’t know why, but they made him uneasy.   Is bunch were whispering excitedly, too, and he couldn’t see a single collecting tin. It was on his way back past them, clutching a large doughnut in a bag, that he caught a few words of what they were saying. “Potters, that’s right, that’s what I heard —” “— yes, their son, Harry —” Mr. Dursley stopped dead. Fear flooded him. He looked back at the whisperers as if he wanted to say something to them, but thought better of it. He dashed back across the road, hurried up to his office, snapped at his secretary not to disturb him, seized his telephone, and had almost finished dialling his home number when he changed his mind. He put the receiver back down and stroked his mustache, thinking. no, he was being stupid. Potter wasn’t such an unusual name. He was sure there were lots of people called Potter who had a son called Harry. Come to think of it, he wasn’t even sure his nephew was called Harry. He’d never even seen the boy. Mrs. Dursley came into the living room carrying two cups of tea. It was no good. He’d have to say something to her. He cleared his throat nervously. “Er — Petunia, dear — you haven’t heard from your sister lately, have you?” As he had expected, Mrs. Dursley looked shocked and angry. After all, they normally pretended she didn’t have a sister. “No,” she said sharply. “Why?” “Funny stuff on the news,” Mr. Dursley mumbled. “Owls. shooting stars. and there were a lot of funny-looking people in town today.” “So?” snapped Mrs. Dursley. “Well, I just thought. maybe. it was something to do with. you know. her crowd.” Mrs. Dursley sipped her tea through pursed lips. Mr. Dursley wondered whether he dared tell her he’d heard the name “Potter.” He decided he didn’t dare. Instead he said, as casually as he could, “Their son — he’d be about Dudley’s age now, wouldn’t he?” “I suppose so,” said Mrs. Dursley stiffly. “What’s his name again? Howard, isn’t it?” “Harry. Nasty, common name, if you ask me.” “Oh, yes,” said Mr. Dursley, his heart sinking horribly. “Yes, I quite agree.”'
training_set='WikiLeaks is an international non-profit organisation that publishes secret information, news leaks, and classified media provided by anonymous sources.'
alphabets='’abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
punctuations='\'(",.;)”“'

tok=[]
buf=''

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
        tok.append(i)
    else:
        continue
tokens=[]
for i in tok:
    if i!='':
        tokens.append(i)


keys=list(set(tokens))
dictogram={}
for i in keys:
    dictogram[i]=tokens.count(i)
follow={}
for i in range(len(tokens)):
    follow[tokens[i]]={}

for i in range(len(tokens)):
    if i+2<len(tokens):
        follow[tokens[i]][(tokens[i+1],tokens[i+1])]=0
    
for i in range(len(tokens)):
    if i+2<len(tokens):
        follow[tokens[i]][(tokens[i+1],tokens[i+1])]+=1 #Change 2nd [i+1] to [i+2] for 2-histogram here and in prev loop

follow['--START--']={}
follow['--START--']=follow['.']
follow['.']['--END--']=20

ct=0
def printf(string):
    global ct
    if ct==3:
        print('----')
        return
    if string[0] not in follow:
        print('-')
        
        return
    #elif '.' in follow[string].keys(): #Added commit
     #   print('.')
      #  ct+=1
    if True: #elif len(list(follow[string].keys()))>1:
        follow_words=list(follow[string[0]].keys())
        follow_occur=list(follow[string[0]].values())
        
        cum_probs=[follow_occur[0]/sum(follow_occur)]
        for i in range(1,len(follow_occur)):
            cum_probs.append(cum_probs[i-1]+ follow_occur[i]/sum(follow_occur))
        
        random_ind=random.randint(0,len(follow[string[0]].keys())-1)
        random_ind/=sum(follow_occur)
        ind=0
        for i in range(len(cum_probs)-1):
            if random_ind>=cum_probs[i] and random_ind<cum_probs[i+1]:
                ind=i
        
        print(follow_words[ind][0],end=' ')
        #print('\n',str(follow[string].keys()).split(", ")[2].strip('\''))
        printf(follow_words[ind])
