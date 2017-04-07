#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 @josquindebaz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import tweepy 
import re
import json

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

with open('fakes.json', 'r') as jsonFile:
    listeFakes = json.loads(jsonFile.read())

def saveFKjson(liste):
    with open('fakes.json', 'w') as outfile:
        str_ = json.dumps(liste,
                          indent=4, sort_keys=True,
                          separators=(',', ':'), ensure_ascii=False)
        outfile.write(str_.encode('utf-8'))

def is_central(status, central = "@GrowthHackFR"):
    if re.search(central, status):
        return 1
    else:
        return 0

def is_domestic(status):
    """ return True if status is domestic """
    if not re.search("^RT ", status):
        if not re.search("http", status):
            return True
        else:
            return False
    return False

def domestic_user(status):
    """False if at least one status is domestic"""
    if True in map(lambda x: is_domestic(x.text), status):
        return False 
    return True

def hasurl(descr):
    """ return True if url in profile """
    return 'url' in R.user.entities.keys()

def user_descr(user, N = 0):
    return  {"name": user.screen_name, \
                "following": user.friends_count,\
                "followers": user.followers_count,\
                "tweets": user.statuses_count,\
                "creation": str(user.created_at),\
                "GH20": N, \
                "description": user.description, \
                "image": user.profile_image_url }

def sources(TL):
    d = {}
    for T in TL:
        source = T.source
        if source in d.keys():
            d[source] += 1
        else:
            d[source] = 1
    return d

seed = api.user_timeline("GrowthHackFR", count=200)
done = []
for T in seed[0:]:
    if (T.retweet):
        N = T.retweet_count
        RS  = api.retweets(T.id)
        for R in RS[0:]:

            """if already in fake list"""
            if str(R.user.id) in listeFakes.keys() or R.user.id in done:
                print R.user.screen_name, "already done"

            else:
                done.append(R.user.id)

                """ if more friends thant followers """
                if (float(R.user.friends_count) / R.user.followers_count) < 1.5:

                    TL = api.user_timeline(R.user.id, count=200)

                    """ if 1 or 2 sources only """
                    Dsources = sources(TL)   
                    if len( Dsources ) == 2:
                        print Dsources

                        """ if domestic tweets """
                        if domestic_user(TL):

                            """ if more than 10 GrowthHack """
                            N = sum(map(lambda x: is_central(x.text), TL)) 
                            if N > 10:

                                """ if no url in profile """
                                if not hasurl(R.user.entities):
                                    print "adding fake", R.user.id, user_descr(R.user, N)
                                    listeFakes[R.user.id] = user_descr(R.user, N)
                                    saveFKjson(listeFakes)
                                else:
                                    print "has url", R.user.id,\
                                        user_descr(R.user, N), R.user.entities["url"]


                            else:
                                print "weak N", R.user.id, user_descr(R.user, \
                                    N), float(N) / R.user.statuses_count

                        else:
                            print "domestic", R.user.id, user_descr(R.user, N)


