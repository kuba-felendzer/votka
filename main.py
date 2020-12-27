import discord
from discord.ext import commands
from datetime import datetime

f = open("TOKEN", "r")
token = f.read()

z_votes = 0
l_votes = 0
t_votes = 0
r_votes = 0

uv = []
voting = False


bot = commands.Bot(command_prefix=":")


# @bot.event
# async def on_message(message):
    # if voting:
        # if
    # pass

@bot.command(name="v")
async def v(ctx, choice):
    global z_votes, l_votes, t_votes, r_votes
    voting = True
    a = ctx.author
    vlc = bot.get_channel(792637369600966676)
    if a in uv:
        await a.send("you already voted, silly!")
        return
    
    if choice in "123":
        uv.append(a)
        if choice == "1": 
            await a.send("Logged your vote for **Zorro**.")
            await vlc.send("Someone voted for **Zorro**!")
            z_votes += 1
            t_votes += 1
        elif choice == "2": 
            await a.send("Logged your vote for **Lobby**.")
            await vlc.send("Someone voted for **Lobby**!")
            l_votes += 1
            t_votes += 1
        elif choice == "3": 
            await a.send("Logged your vote for **Robot**.")
            await vlc.send("Someone voted for **Robot**!")
            r_votes += 1
            t_votes += 1

        
    else:
        await a.send("That is not a valid option!")
        return


@bot.command(name="d")
async def d(ctx):
    voting_embed = discord.Embed(title="Director Election", description="Elect our new director!", color=0x00ff00)
    voting_embed.add_field(name="Choice 1: ", value="Zorro")
    voting_embed.add_field(name="Choice 2: ", value="Lobby")
    voting_embed.add_field(name="Choice 3: ", value="Robot")

    await ctx.send(embed=voting_embed)

@bot.command(name="t")
async def t(ctx):
    global z_votes, l_votes, t_votes, r_votes
    time = datetime.utcnow()
    e = discord.Embed(title="Votes Tally", description=f"As of UTC {time}")
    e.add_field(name="Votes for Zorro: ", value=str(z_votes), inline=False)
    e.add_field(name="Votes for Lobby: ", value=str(l_votes), inline=False)
    e.add_field(name="Votes for Robot: ", value=str(r_votes), inline=False)
    e.add_field(name="Total Votes: ", value=str(t_votes), inline=False)

    await ctx.send(embed=e)

bot.run(token)