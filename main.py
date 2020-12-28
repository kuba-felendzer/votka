import discord
from discord.ext import commands
from datetime import datetime

f = open("TESTTOKEN", "r")
token = f.read()

r_votes = 0 # total amount of votes for robot
z_votes = 0 # total amount of votes for zorro
l_votes = 0 # total amount of votes for lobby
t_votes = 0 # total amount of votes
i_votes = 0 # total amount of votes for random

# CANDIDATES:
# Lobby, Zorro, Robot, Random

uv = [] # list of users who have voted

startup_time = datetime.utcnow() # the UTC time when this script starts

bot = commands.Bot(command_prefix=":")

class Candidate:
    
    def __init__(self, id, name, vc):
        self.id = id
        self.name = name
        self.vc = vc

gamers = [Candidate("1", "Zorro", z_votes), Candidate("2", "Lobby", l_votes), Candidate("3", "Robot", r_votes), Candidate("4", "Random", i_votes)]

@bot.event
async def on_ready():
    print("VotkaT ready!")
    print(startup_time.strftime("%c"))

@bot.command(name="v") # creates a command of the name v
async def v(ctx, choice): # voting command, usage :v <choice>, which in this case is 1, 2, or 3
    global z_votes, l_votes, t_votes, r_votes, i_votes, gamers # global these variables to make sure I'm using the right ones
    a = ctx.author # turns "ctx.author.send" to "a.send"
    vlc = bot.get_channel(792633683440959498) # the specific channel that the voting data ("Someone voted for Lobby!")
    
    if choice.lower() in ["1", "2", "3", "4"]: # if the choice is either a one, two, or three (correct options)
        if a in uv: # if the command author (a) is in the list of users who have voted
            await ctx.send("you already voted, silly!") # send them a message telling them they already voted
            return # return nothing, skip the rest of the function
        uv.append(a)
        for cand in gamers:
            if cand.id == choice:
                cand.vc += 1
                t_votes += 1
                # output
                await a.send(f"You successfully voted for **{cand.name}**!")
                await vlc.send(f"**{cand.name}** has recieved one more vote!")
                await t(ctx)
    else: # if the person did not cast a 1, 2, or 3
        await ctx.send("That is not a valid option!") # tell them they can't pick that candidate
        return # exit the function


@bot.command(name="d") # creates a command of the name d
async def d(ctx): # display command, usage :d
    global gamers
    voting_embed = discord.Embed(title="Director Election", description="Elect our new director!", color=10494192) # create the embed
    for c in gamers:
        voting_embed.add_field(name=f"Choice {c.id}: ", value=f"{c.name}, `:v {c.id}`")

    await ctx.send(embed=voting_embed) # send the embed in the chat that requested it

@bot.command(name="t") # creates a command of the name t
async def t(ctx): # total command, usage ;t
    global gamers, startup_time # make sure I am using the right vars
    time = datetime.utcnow() # the time when this command is called
    # https://strftime.org/ formatting data from here
    e = discord.Embed(title="Votes Tally", description=f"As of {time.strftime('%c')} UTC\nLast restarted on {startup_time.strftime('%c')} UTC", color=10494192) # create the embed
    # time.strftime("%c") tells python to represent the time according to the "c" formatting option, same for startup_time.strftime
    for c in gamers:
        e.add_field(name=f"Votes for {c.name}: ", value=str(c.vc), inline=False)

    e.add_field(name="Total Votes: ", value=str(t_votes), inline=False) # add the total votes
    await ctx.send(embed=e)

bot.run(token)