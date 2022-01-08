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

import yaml
with open('Auth.yml', 'r') as file:
    auth = yaml.safe_load(file)


def twintSwearch(query, limit):
    c = twint.Config()

    c.Limit = limit
    c.Custom["tweet"] = ["id","username"]
    c.Search = query
    c.Store_object = True
    c.Filter_retweets = True
    #c.Store_csv = True
    #c.Output = "tweets.csv"
    #c.Format = "ID {id} | URL {urls[0]}"

    twint.run.Search(c)

    tweets = twint.output.tweets_list

    print("did the thing....")

    for i in range(len(tweets)):
        print(f"{tweets[i].id} | {tweets[i].username}" )
        print(f"https://twitter.com/{tweets[i].username}/status/{tweets[i].id}")

#load_dotenv()
TOKEN = auth['discord_token']
GUILD = auth['guild_name']

client = discord.Client()
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
    ch = client.get_channel(528042078031183875)
    print(ch)
    messages = await ch.history(limit=3).flatten()
    print(messages[0].content)
    
    twintSwearch("#mvci_cma", 20)
    

client.run(TOKEN)