#!/usr/bin/env python3
import discord
import lib.params as pm
import asyncio
import random
import os

ANNOYING = pm.get_annoy()

BOT_TOKEN = os.environ['DISCORDBOT']

client = discord.Client()

spam_message_min = 10
async def spam_test():
    await client.wait_until_ready()
    channel = discord.Object(id='148797597358751744')

    # Runs while client is live and ANNOYING is True
    while not client.is_closed and ANNOYING:
        print(":)")
        await client.send_message(channel, "Helperbot Online!")
        await client.send_message(channel, "Ask any questions, NOW!")

        await asyncio.sleep(60*spam_message_min)


@client.event
async def on_message(message):
    if message.content.startswith('$help'):
        await client.send_message(channel, ('Alright, <@' +
                                  str(message.author.id) +
                                  '>! I PMed you some help!'))
        await client.send_message(message.author,
                                  'Fetching Help Library...')
        await asyncio.sleep(3)
        await client.edit_message(msg, 'Help Text Coming Soon')


@client.event
async def on_message(message):
    """
        Command List:
        [*] "$guess": Allows user to guess a "randomly" generated 1 to 10
            digit.
    """
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if ANNOYING:
        msg = ('Howdy <@{}>. You said: "{}". Here is your email: \n{}'
               .format(str(message.author.id), message.content,
                       str(message.author.avatar_url)))
        mes = await client.send_message(message.channel, msg)

    # GUESSING GAME ("$guess")
    if message.content.startswith('$guess'):
        await client.send_message(message.channel, ('Guess a number between' +
                                  ' 1 to 10 (Answer within 5 seconds)'))

        def guess_check(m):
            m = m.content
            start_string = '<@{}>'.format(client.user.id)
            if not m.startswith(start_string):
                return False
            else:
                m = m[len(start_string):]
                m.strip(' ')
                return m.isdigit()

        guess = await client.wait_for_message(timeout=5.0,
                                              author=message.author,
                                              check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = ('Sorry <@{}> , you took too long. It was {}.'
                   .format(str(message.author.id), answer))
            await client.send_message(message.channel, fmt)
            return
        if int(guess.content) == answer:
            fmt = ('You are right, <@{}>!').format(str(message.author.id))
            await client.send_message(message.channel, fmt)
        else:
            fmt = ('Sorry, <@{}>. It is actually {}.'
                   .format(str(message.author.id), answer))
            await client.send_message(message.channel, fmt)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(spam_test())
client.run(BOT_TOKEN)
