import discord
from discord.ext import commands
from datetime import datetime

f = open("TOKEN", "r") # open the TOKEN file
token = f.read() # read all the data from it and assign it to token

r_votes = 0 # total amount of votes for robot
z_votes = 0 # total amount of votes for zorro
l_votes = 0 # total amount of votes for lobby
t_votes = 0 # total amount of votes


uv = [] # list of users who have voted

startup_time = datetime.utcnow() # the UTC time when this script starts

bot = commands.Bot(command_prefix=":") # creates the actual bot with the prefix of :

@bot.event
async def on_ready(): # called once when the bot starts up
    print("Votka ready!") # print a message to console, lets you know when the bot is on
    print(startup_time.strftime("%c")) # prints the time it started up

@bot.command(name="v") # creates a command of the name v
async def v(ctx, choice): # voting command, usage :v <choice>, which in this case is 1, 2, or 3
    global z_votes, l_votes, t_votes, r_votes # global these variables to make sure I'm using the right ones
    a = ctx.author # turns "ctx.author.send" to "a.send"
    vlc = bot.get_channel(792637369600966676) # the specific channel that the voting data ("Someone voted for Lobby!")
    if a in uv: # if the command author (a) is in the list of users who have voted
        await a.send("you already voted, silly!") # send them a message telling them they already voted
        return # return nothing, skip the rest of the function
    
    if choice.toLower() in ["1", "2", "3", "z", "l", "r"]: # if the choice is either a one, two, or three (correct options)
        uv.append(a) # add this person to the list of people who have voted
        if choice == "1" or choice == "z": # if they chose 1 (Zorro)
            await a.send("Logged your vote for **Zorro**.") # tell them their vote is counted
            await vlc.send("Someone voted for **Zorro**!") # tell the #votes channel someone voted for zorro
            z_votes += 1 # add one to zorro's votes
        elif choice == "2" or choice == "l": # if they chose 2 (Lobby)
            await a.send("Logged your vote for **Lobby**.") # tell them their vote is counted
            await vlc.send("Someone voted for **Lobby**!") # tell the #votes channel someone voted for lobby
            l_votes += 1 # add one to lobby's votes
        elif choice == "3" or choice == "r": # if they chose 3 (Robot)
            await a.send("Logged your vote for **Robot**.") # tell them their vote is counted
            await vlc.send("Someone voted for **Robot**!") # tell the #votes channel someone voted for robot
            r_votes += 1 # add one to robot's votes
            
        t_votes += 1 # add one to the total vote, since this is valid vote  
    else: # if the person did not cast a 1, 2, or 3
        await a.send("That is not a valid option!") # tell them they can't pick that candidate
        return # exit the function


@bot.command(name="d") # creates a command of the name d
async def d(ctx): # display command, usage :d
    voting_embed = discord.Embed(title="Director Election", description="Elect our new director!", color=10494192) # create the embed
    voting_embed.add_field(name="Choice 1: ", value="Zorro, `:v 1` or `:v z`") # add zorro
    voting_embed.add_field(name="Choice 2: ", value="Lobby, `:v 2` or `:v l`") # add lobby
    voting_embed.add_field(name="Choice 3: ", value="Robot, `v: 3` or `:v r`") # add robot
    # this function just displays who is running and how to vote for them
    await ctx.send(embed=voting_embed) # send the embed in the chat that requested it

@bot.command(name="t") # creates a command of the name t
async def t(ctx): # total command, usage ;t
    global z_votes, l_votes, t_votes, r_votes, startup_time # make sure I am using the right vars
    time = datetime.utcnow() # the time when this command is called
    # https://strftime.org/ formatting data from here
    e = discord.Embed(title="Votes Tally", description=f"As of {time.strftime('%c')} UTC\nLast restarted on {startup_time.strftime('%c')} UTC", color=10494192) # create the embed
    # time.strftime("%c") tells python to represent the time according to the "c" formatting option, same for startup_time.strftime
    e.add_field(name="Votes for Zorro: ", value=str(z_votes), inline=False) # add zorro's votes
    e.add_field(name="Votes for Lobby: ", value=str(l_votes), inline=False) # add lobby's votes
    e.add_field(name="Votes for Robot: ", value=str(r_votes), inline=False) # add robot's votes
    e.add_field(name="Total Votes: ", value=str(t_votes), inline=False) # add the total votes

    await ctx.send(embed=e) # send the table

bot.run(token) # allows the bot to run and function