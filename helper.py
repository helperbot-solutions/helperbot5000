#!/usr/bin/env python3
import discord
from discord.ext import commands
import lib.params as pm
import asyncio
import random
import os

try:
    ANNOYING = pm.get_annoy()
except KeyError:
    ANNOYING = False


BOT_TOKEN = os.environ['DISCORDBOT']

description = """A helper bot!"""

client = commands.Bot(command_prefix='$', description=description)


async def presence_set():
    await client.wait_until_ready()
    await client.change_presence(game=discord.Game
                                 (name="with the Discord API"))


@client.event
async def on_ready():
    print('Annoying: {}'.format(ANNOYING))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def youtube_video_link_give(check_words, video_link, message):
    if any(s in message.content.lower() for s in check_words):
        msg = ("Where you looking for this? " + video_link)
        await client.send_message(message.channel, msg)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if ANNOYING:
        msg = ('Howdy <@{}>. You said: "{}". Here is your email: \n{}'
               .format(str(message.author.id), message.content,
                       str(message.author.avatar_url)))
        mes = await client.send_message(message.channel, msg)

    # Send a link to the "Click Noice" video when the word 'noice' is mentioned
    youtube_link = "https://www.youtube.com/watch?v=3WAOxKOmR90"
    await youtube_video_link_give(('noice', 'nice', 'noiice', 'noicce'),
                                  youtube_link, message)

    # Send a link to the "Yeah Boi" video when the word 'yeah' or 'boi'/'boy'
    # is mentioned
    youtube_link = "https://www.youtube.com/watch?v=fvtQYsckLxk&t=1m5s"
    await youtube_video_link_give(('yeah', 'yeh', 'boi', 'boy'), youtube_link,
                                  message)

    # Send a link to the "Time to Stop" video when the word 'stop' or 'time' is
    # mentioned
    youtube_link = "https://www.youtube.com/watch?v=2k0SmqbBIpQ"
    await youtube_video_link_give(('stop',), youtube_link,
                                  message)

    await client.process_commands(message)


@client.command(pass_context=True, name='annoy')
async def set_annoying(ctx, annoy: bool):
    """Sets if the bot is annoying."""
    global ANNOYING
    author = ctx.message.author
    if not isinstance(annoy, bool):
        await client.say(("<@{}>, ERROR: Input has to be a boolean."
                          .format(author.id)))
        return

    ANNOYING = annoy
    await client.say(("<@{}>, the Annoying value has been set to {}."
                      .format(author.id, annoy)))


@client.command(pass_context=True)
async def guess(ctx):
    """Allows user to guess a "randomly" generated 1 to 10 digit."""
    author = ctx.message.author

    await client.say(
        ('<@{}> Guess a number between 1 to 10 (Answer within 5 seconds)' +
         ' [Make sure to mention me!]')
        .format(author.id))

    start_string = '<@{}>'.format(str(client.user.id))

    def format_response(m):
        m = m.strip(' ')
        m = m[len(start_string):].strip(' ')
        return m

    def guess_check(m):
        m = m.content.strip(' ')

        if m.startswith(start_string):
            m = format_response(m)
            return m.isdigit()
        else:
            return False

    guess = await client.wait_for_message(timeout=5.0, author=author,
                                          check=guess_check)

    answer = random.randint(1, 10)
    if guess is None:
        fmt = ('Sorry <@{}> , you took too long. It was {}.'
               .format(str(author.id), answer))
        await client.say(fmt)
        return

    guess_text = format_response(guess.content)
    if int(guess_text) == answer:
        fmt = ('You are right, <@{}>!').format(str(author.id))
        await client.say(fmt)
    else:
        fmt = ('Sorry, <@{}>. It is actually {}.'
               .format(str(author.id), answer))
        await client.say(fmt)


# Remove default help command:
client.remove_command('help')


# Custom help command:
@client.command(pass_context=True, name='help')
async def _help(ctx):
    author = ctx.message.author

    await client.say('Alright, <@{}>! I PMed you some help!'
                     .format(str(author.id)))
    msg = await client.send_message(author, 'Fetching Help Library...')
    await asyncio.sleep(3)
    await client.edit_message(msg, 'Help Text Coming Soon')


client.loop.create_task(presence_set())
client.run(BOT_TOKEN)
