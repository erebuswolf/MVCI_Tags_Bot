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
import nest_asyncio
nest_asyncio.apply()

import re

import yaml
with open('Auth.yml', 'r') as file:
    auth = yaml.safe_load(file)


async def twintSwearch(query, limit):
    c = twint.Config()

    c.Limit = limit
    c.Custom["tweet"] = ["id","username"]
    c.Search = query
    c.Store_object = True
    c.Filter_retweets = True
    c.Retries_count = 60
    c.Since = "2019-02-26"
    c.Debug = True
    c.Backoff_exponent = 5
    c.Min_wait_time = 10
    c.Max_empty_return = 10
    #c.Store_csv = True
    #c.Output = "tweets.csv"
    #c.Format = "ID {id} | URL {urls[0]}"
    print(c.Limit)

    twint.run.Search(c)

    tweets = twint.output.tweets_list

    print("did the thing....")

    for i in range(len(tweets)):
        print(f"{tweets[i].id} | {tweets[i].username}" )
        print(f"https://twitter.com/{tweets[i].username}/status/{tweets[i].id}")
    print (len(tweets))
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
        id = re.search('/status/(\d+)', messages[i].content).group(1)
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
    await fixup_channel(528055603608682526,"#mvci_art",500,500)
    #await fixup_channel(528055766633152513,"#mvci_cma",500,500)
    

client.run(TOKEN)