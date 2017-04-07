#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy 
import json
from secrets import consumer_key, consumer_secret, access_token, access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def write(profile, F):
    with open('followers-%s.json'%(profile), "w") as fil:
        str_ = json.dumps(F, indent=4, sort_keys=True,
              separators=(',', ':'), ensure_ascii=False)
        fil.write(str_.encode("utf-8"))

def followers(profile):
    F = {}
    page_count = 0
    for user in tweepy.Cursor(api.followers, id=profile, count=200).pages():
        page_count += 1
        print 'Getting page %d for %s followers' % (page_count, profile)
        for f in user:
            t = {
                "screen_name": f.name, \
                "created_at": str(f.created_at), \
                "n statuses": f.statuses_count, \
                "egg": f.default_profile_image, \
                "profile length": len(f.description), \
                "followers": f.followers_count, \
                "friends": f.friends_count, 
                }

            F[f.id] = t
        if len(F) > 10000:
            break
    return F


for profile in [
    "EmmanuelMacron", "MLP_officiel", "JLMelenchon", "FrancoisFillon", \
    "benoithamon",  "PhilippePoutou", "n_arthaud", \
    "UPR_Asselineau", "dupontaignan",\
    "JCheminade", "jeanlassalle"]:

    write(profile, followers(profile))

