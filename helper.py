#!/usr/bin/env python3
import discord
import asyncio
import os

BOT_TOKEN = os.environ['DISCORDBOT']

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msg = 'Hello <@' + str(message.author.id) + '>. You said: "{0}". Here is your avatar: \n{1}'.format(message.content, str(message.author.avatar_url))
    mes = await client.send_message(message.channel, msg)

    # if message.content.startswith('!hello'):
    #    msg = 'Hello {0.author.mention}'.format(message
    #    await client.send_message(message.channel, msg)


spam_message_min = 10
async def spam_test():
    await client.wait_until_ready()
    channel = discord.Object(id='148797597358751744')
    while not client.is_closed:
        print("Message!")
        await client.send_message(channel, "Hello everyone!")
        await asyncio.sleep(60*spam_message_min)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(spam_test())
client.run(BOT_TOKEN)
