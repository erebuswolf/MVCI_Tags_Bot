#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 02:03:39 2022

@author: jesse
"""
# bot.py
#import os

import discord
import twint
#from dotenv import load_dotenv
import asyncio
import nest_asyncio
nest_asyncio.apply()

import re

import yaml
with open('Auth.yml', 'r') as file:
    auth = yaml.safe_load(file)

id_and_hash = {528055603608682526 : "#MVCI_ART",
               528055660907331596 : "#MVCI_BPA",
               528055681018888215 : "#MVCI_BWI",
               528055745149665300 : "#MVCI_CAM",
               528055766633152513 : "#MVCI_CMA",
               528055781216747520 : "#MVCI_CHR",
               528055795867451402 : "#MVCI_CHU",
               528055810639659038 : "#MVCI_DAN",
               528055827349897218 : "#MVCI_DOC",
               528055839714443266 : "#MVCI_DOR",
               528055879631634452 : "#MVCI_FIR",
               528056455014907916 : "#MVCI_FRA",
               528056483158425620 : "#MVCI_GAM",
               528056498581143562 : "#MVCI_GHO",
               528056520483536935 : "#MVCI_HAG",
               528056530554191903 : "#MVCI_HAW",
               528056538695335979 : "#MVCI_HUL",
               528056550108037151 : "#MVCI_IRO",
               528056592000745489 : "#MVCI_JED",
               528056623374139394 : "#MVCI_MON",
               528056640633831454 : "#MVCI_MOR",
               528056651173855263 : "#MVCI_NEM",
               528056657759043594 : "#MVCI_NOV",
               528056679401783297 : "#MVCI_ROC",
               528056692198604802 : "#MVCI_RYU",
               528056720212230154 : "#MVCI_SIG",
               528056739686514688 : "#MVCI_SPE",
               528057303019159582 : "#MVCI_SPI",
               528057323726307374 : "#MVCI_STR",
               528057336863129615 : "#MVCI_THA",
               528057345016594441 : "#MVCI_THO",
               528057353740746776 : "#MVCI_ULT",
               528057362947244044 : "#MVCI_VEN",
               528057377606336522 : "#MVCI_WIN",
               528057390608678912 : "#MVCI_MMX",
               528057404773105664 : "#MVCI_ZER",
               528057443331211293 : "#MVCI_SPA",
               528057463476453377 : "#MVCI_SOU",
               528057484225675276 : "#MVCI_POW",
               528057503142117406 : "#MVCI_REA",
               528057526189686784 : "#MVCI_TIM",
               528057513388670976 : "#MVCI_MIN",}


async def twintSwearch(query, limit):
    c = twint.Config()

    tweets = []

    c.Limit = limit
    c.Custom["tweet"] = ["id","username"]
    c.Search = query
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    c.Filter_retweets = True
    c.Retries_count = 60
    c.Since = "2019-02-26"
    c.Debug = False
    c.Backoff_exponent = 5
    c.Min_wait_time = 10
    c.Max_empty_return = 10
    c.Hide_output = True
    
    #c.Store_csv = True
    #c.Output = "tweets.csv"
    #c.Format = "ID {id} | URL {urls[0]}"

    twint.run.Search(c)

    print(f"Searching Twitter for {query}")

    #for i in range(len(tweets)):
    #    print(f"{tweets[i].id} | {tweets[i].username}" )
    #    print(f"https://twitter.com/{tweets[i].username}/status/{tweets[i].id}")
    print (f"found {len(tweets)} tweets")
    return tweets

#load_dotenv()
TOKEN = auth['discord_token']
GUILD = auth['guild_name']

client = discord.Client()

async def fixup_channel(channel_id, hash_string, disc_history_len, twit_hist_len):
    
    ch = client.get_channel(channel_id)
    print(f"Running on Channel {ch}")
    messages = await ch.history(limit=disc_history_len).flatten()
    
    ids = []
    for i in range(len(messages)):
        if(messages[i].content is not None):
            result = re.search('/status/(\d+)', messages[i].content)
            if (result is not None):
                id = result.group(1)
                ids.append(int(id))
        
    ids.sort()
    for i in range(len(ids)):
        print(ids[i])
        
    
    tweets = await twintSwearch(hash_string, twit_hist_len)
    
    for i in range(len(tweets)):
        if(int(tweets[i].id) in ids):
            print(f"tweet {tweets[i].id} by {tweets[i].username} was already in the list")
        else:
            print(f"tweet {tweets[i].id} by {tweets[i].username} is a new tweet")


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
    key = list(id_and_hash.keys())[3]
    print(f" searching for {key} and {id_and_hash[key]}")
    await fixup_channel(key,id_and_hash[key],500,500)
    
    key = list(id_and_hash.keys())[4]
    print(f" searching for {key} and {id_and_hash[key]}")
    await fixup_channel(key,id_and_hash[key],500,500)
    
    #for i in id_and_hash.keys():
    #    print(f" searching for {i} and {id_and_hash[i]}")
        #await fixup_channel(i,id_and_hash[i],500,500)
    #await fixup_channel(528055766633152513,"#mvci_cma",500,500)
    

client.run(TOKEN)