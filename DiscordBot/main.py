# Welcome nerds, this is the source code of my bot
# The public version wont show Tokens nor user ID's
# Files for those will still exist but wont store data

# Imports

from datetime import timedelta
from importlib.util import decode_source
from itertools import count
from sys import prefix
import discord
from discord import colour
from discord import user
from discord.ext import commands
import random
from discord.ext.commands.bot import Bot
from dotenv import load_dotenv
import os
import praw

# Definitions

intents = discord.Intents().all()
client = commands.Bot(command_prefix="s!", intents=intents, help_command=None)
reddit = praw.Reddit(client_id="redditclient", client_secret="redditclientsecret", user_agent="clientname")

p = ["Ping!", "Pong!"]
ans = ["yes", "nah", "there might be a chance"]

# Commands

@client.command(aliases=["pong"])
async def ping(ctx):
    await ctx.send(f":ping_pong:{random.choice(p)}, pinged the closest server with a latency of, {(round)(client.latency * 100)}ms")

@client.command()
async def servers(ctx):
  servers = list(client.guilds)
  await ctx.send(f"i am connected to {str(len(servers))} guilds, add me to your server using the s!add command")

@client.command()
async def math(ctx, operation:str):
    await ctx.reply(eval(operation))

@client.command()
async def add(ctx):
  e = discord.Embed(title="click to add me to your server", url="https://discord.com/oauth2/authorize?client_id=881938660495339601&permissions=8&scope=bot", colour=0xB00B69)
  await ctx.send(embed=e)

@client.command()
async def help(ctx):
  e =  discord.Embed(title="Not a therapist but heres a list of commands", url="https://github.com/lilslatt42/spbot/blob/main/commands", colour=0xfc9889)
  await ctx.send(embed=e)

@client.command(aliases=["av"])
async def avatar(ctx, u: discord.Member=None):
  if u == None: u = ctx.author
  av = u.avatar_url
  e = discord.Embed(title=f"**{u.display_name}**'s avatar", colour=0xfc9889)
  e.set_image(url=av)
  await ctx.send(embed=e)

@client.command()
async def whois(ctx, member : discord.Member=None):
    if member == None: member = ctx.author

    created = member.created_at.strftime(f"%A, %B %d %Y at about %H:%M %p")
    joined = member.joined_at.strftime(f"%A, %B %d %Y at about %H:%M %p")
    roles = member.roles
    roles = ' '.join(a.mention for a in roles[::-1] if not a.name == '@everyone')

    line1 = f"Joined discord at: {created}"
    line2 = f"Joined server at: {joined}"
    line3 = f"Roles: {roles}"
    line4 = f"ID and Display Name: {member.id}/{member.display_name}"

    embed = discord.Embed(
        title=f"Info:",
        description=f"{line1}\n\n{line2}\n\n{line3}\n\n{line4}",
        color=0xfc9889
    )
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)

    await ctx.send(embed=embed)

@client.command()
async def say(ctx, *, agrs):
  await ctx.message.delete()
  await ctx.send(agrs)

@client.command()
async def test(ctx):
  await ctx.send(decode_source)

@client.command()
async def members(ctx):
  mc = ctx.guild.member_count
  e = discord.Embed(title=f"{ctx.guild.name} currently has:", description=f"**{mc} members** invite some more members to boost that number up", colour=0xfc9889)
  e.set_thumbnail(url=ctx.guild.icon_url)
  await ctx.send(embed=e)

@client.command()
async def git(ctx):
  e = discord.Embed(title="Open source is so cool", url="https://github.com/lilslatt42/spbot/", colour=0xfc9889)
  await ctx.send(embed=e)

@client.command(name="8ball")
async def _8ball(ctx):
  await ctx.send(random.choice(ans))

@client.command()
async def info(ctx):
  servers = list(client.guilds)
  e = discord.Embed(title= "SPBT information", url="https://github.com/lilslatt42/spbot/blob/main/README.md", colour=0xfc9889)
  e.set_author(name=client.user.name, icon_url=client.user.avatar_url)
  e.description = "Basic open source discord bot, not much I can really do that makes me special but check out the help command"
  e.add_field(name="Servers running in", value=f"{str(len(servers))}", inline=False)
  await ctx.send(embed=e)

@client.command()
async def kick(ctx, u: discord.Member=None):
  await ctx.send(f"kicked **{u.mention}**, user ID: **{u.id}**")
  await u.send(f"you were kicked because of reason")

@client.command()
async def dice(ctx):
  dice = random.randint(1, 6)
  await ctx.send(dice)

@client.command()
async def rr(ctx):
  u = ctx.author.name
  rr = [f"{u}'s brains are all over the wall\n\ngetting the maid to clean them", "click, close but you live", "clack, so close but you live"]
  await ctx.send(random.choice(rr))

@client.command()
async def rad(ctx, num1 : float):
  answer = num1 ** 0.5

  ans_em = discord.Embed(title = 'Radical', description = f'Question: Radical of {num1}\n\nAnswer: {answer}', colour = 0xfc9889)
  
  await ctx.send(embed = ans_em)

@client.command()
async def meme(ctx):
  sub_submissions = reddit.subreddit('memes').hot()
  post_to_pick = random.randint(1, 120)
  for i in range(0, post_to_pick):
      submission = next(x for x in sub_submissions if not x.stickied)
  e = discord.Embed(title=f'Requested by {ctx.author}', description=f'{submission.title}', color=0xfc9889)
  e.set_image(url=submission.url)
  await ctx.send(embed=e)  

# Nsfw Commands

@client.command()
@commands.is_nsfw()
async def nsfw(ctx):
  sub_submissions = reddit.subreddit('nsfw').hot()
  post_to_pick = random.randint(1, 120)
  for i in range(0, post_to_pick):
      submission = next(x for x in sub_submissions if not x.stickied)
  e = discord.Embed(title=f'Requested by {ctx.author}', description=f'{submission.title}', color=0xfc9889)
  e.set_image(url=submission.url)
  await ctx.send(embed=e)

@client.command()
@commands.is_nsfw()
async def ngif(ctx):
  sub_submissions = reddit.subreddit('NSFW_GIF').hot()
  post_to_pick = random.randint(1, 120)
  for i in range(0, post_to_pick):
      submission = next(x for x in sub_submissions if not x.stickied)
  await ctx.send(submission.url)

# Client Events


# Command Error Handling

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
      e = discord.Embed(title=":x: ERROR :x:", description="You're missing the required permissions to run this command :thinking:", colour=0xfc9889)
      await ctx.send(embed=e)
    if isinstance(error, commands.MissingRequiredArgument):
      e = discord.Embed(title=":x: ERROR :x:", description="Im missing the required argument to pass that command", colour=0xfc9889)
      await ctx.send(embed=e)
    if isinstance(error, commands.CommandInvokeError):
      e = discord.Embed(title=":x: ERROR :x:", description="Improper use of command, did you try to devide 0 by 0?", colour=0xfc9889)
      await ctx.send(embed=e)
    if isinstance(error, commands.NSFWChannelRequired):
      e = discord.Embed(title=":x: ERROR :x:", url="https://support.discord.com/hc/en-us/articles/115000084051-NSFW-channels-and-content", description="This command must be used in a NSFW channel", colour=0xfc9889)
      await ctx.send(embed=e)

# Run the bot

load_dotenv()
client.run(os.getenv("joe"))
