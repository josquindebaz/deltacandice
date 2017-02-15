#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy 
import re
import json

#ids of tweets you want to check
queue = {'todo': ["830808934772523009", "831092048354824192"], \
     'done' : []}

#you keys for twitter API
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def searchTWperso(text):
    if not re.search("^RT ", text):
        if not re.search("http", text):
           return True
        else:
           return False
    return False

def filtre_user(STS):
    if True in map(lambda x: searchTWperso(x.text), STS):
        return True 
    return False
        
def searchlink(T):
    if T.entities["urls"]:
        if re.search("growthhackingfrance",
                T.entities['urls'][0][u'expanded_url']):
            if (T.id not in queue['done']) and (T.id not in queue['todo']):
                pass
            return True
        else:
            return False
    else:
        return False

D = {}

while (queue['todo']):
    T_id = queue['todo'].pop()
    queue['done'].append(T_id)

    #RT of the tweet
    RT = api.retweets(T_id, 100)
    for T in RT:

        STS = api.user_timeline(T.user.id)

        #if user has no domestic tweet
        if not filtre_user(STS):

            if (T.user.url):
                pass

            #if user has no url in profile
            else:

                #how many link to growthhackingfrance in the last 20 tweets
                N = sum(map(searchlink, STS)) 

                #if at least 2 
                if N > 1:
                    D[T.user.id] = {"name": T.user.screen_name, \
                        "following": T.user.friends_count,\
                        "followers": T.user.followers_count,\
                        "tweets": T.user.statuses_count,\
                        "creation": str(T.user.created_at),\
                        "GH20": N, \
                        "description": T.user.description, \
                        "image": T.user.profile_image_url }

                    print(D[T.user.id])

with open('fakes.json', 'w') as outfile:
    str_ = json.dumps(D,
                      indent=4, sort_keys=True,
                      separators=(',', ':'), ensure_ascii=False)
    outfile.write(str_.encode('utf-8'))


