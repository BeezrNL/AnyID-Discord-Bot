import discord
from discord.ext import commands
from configparser import ConfigParser

import scholarFile, scholarList, tokenData, scholarData

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
botInfo = config_object["DISCORD"]

#General bot info
description = "AnyID - A Python Discord bot by AxieID.com providing information for and about it's scholars playing Axie Infinity"
bot = commands.Bot(command_prefix = ">", description = description)
bot.remove_command('help') # allows help command to be overwritten

@bot.event
async def on_ready():
    print(f'{bot.user.name} has joined the server!')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help for commands"))

@bot.event 
async def on_disconnect():
    print(f'{bot.user.name} has left the server!')

@bot.command(name ='help')
async def help_command(ctx, command=None):
    print("User [ "+str(ctx.author)+" ] used >help")

    embedMsg = discord.Embed(title="Commands of the AnyID scholar bot", description=" \n Below are the commands you can use.", color=0xf5f542)
    embedMsg.add_field(name=">when", value=">when shows you when your SLP can be claimed.", inline=False)
    embedMsg.add_field(name=">earn", value=">earn shows you a detailed report of your SLP earnings.", inline=False)
    #embedMsg.add_field(name=">mmr", value=">mmr shows you a detailed report of your PvP results.", inline=False)
    embedMsg.add_field(name=">slp", value=">slp shows you details about the SLP token.", inline=False)
    #embedMsg.add_field(name=">fee", value=">fee shows you a link to current transaction fee's on Ethereum.", inline=False)
    #embedMsg.add_field(name=">arena", value=">fee shows a bracket of rewards per MMR rating in Arena.", inline=False)
    #embedMsg.add_field(name=">ladder", value="[Admin Only] sorted list of scholars based on mmr rating. ", inline=False)
    
    embedMsg.add_field(name=">scholarAdd", value="[Admin Only] add scholar to bot. use as: >addScholar [DiscordID] [ScholarWallet]", inline=False)
    embedMsg.add_field(name=">scholarRemove", value="[Admin Only] remove scholar from bot. use as: >removeScholar [DiscordID]", inline=False)

    await ctx.channel.send(embed=embedMsg)

## Adding new scholar
@bot.command(name ='scholarAdd')
async def scholaradd_command(ctx, *, arg):
    """Add new scholar"""
    print("User [ "+str(ctx.author)+" ] used >scholarAdd")
    if ctx.message.author.guild_permissions.administrator:
        newScholarInfo = arg.split(" ")
        discordID = newScholarInfo[0]
        filename = newScholarInfo[1].replace("ronin:","0x")

        scholarFile.createScholarFile(filename)
        scholarList.addToScholarList(discordID, filename)
    
        embedMsg = discord.Embed(title="Scholar management", description="Adding new scholar", color=0x39fc03)
        embedMsg.add_field(name="Status", value="Success.", inline=False)           
    else:
        embedMsg = discord.Embed(title="Scholar management", description="Adding new scholar", color=0xeb3434)
        embedMsg.add_field(name="Status", value="Failed! Access denied.", inline=False)

    await ctx.channel.send(embed=embedMsg)

## Remove existing scholar
@bot.command(name ='scholarRemove')
async def scholarremove_command(ctx, arg):
    """Remove scholar"""
    print("User [ "+str(ctx.author)+" ] used >scholarRemove")
    if ctx.message.author.guild_permissions.administrator:
        discordID = arg
        isRemoved = scholarList.removeFromScholarList(discordID)

        if isRemoved:
            embedMsg = discord.Embed(title="Scholar management", description="Removing scholar", color=0x39fc03)
            embedMsg.add_field(name="Status", value="Success!", inline=False)
        else:
            embedMsg = discord.Embed(title="Scholar management", description="Removing scholar", color=0xeb3434)
            embedMsg.add_field(name="Status", value="Failed! Scholar not found.", inline=False)           
    else:
        embedMsg = discord.Embed(title="Scholar management", description="Removing scholar", color=0xeb3434)
        embedMsg.add_field(name="Status", value="Failed! Access denied.", inline=False)

    await ctx.channel.send(embed=embedMsg)

## Show earning report for scholar
@bot.command(name ='earn')
async def earn_command(ctx):
    """Show scholar when slp can be claimed"""
    print("User [ "+str(ctx.author)+" ] used >earn")

    #Create reply
    embedMsg,file = scholarData.createEarnReport(ctx.author, ctx.message.author.id)
    await ctx.channel.send(embed = embedMsg, file=file)

## Show when SLP can be claimed
@bot.command(name ='when')
async def when_command(ctx):
    """Show scholar when slp can be claimed"""
    print("User [ "+str(ctx.author)+" ] used >when")

    #Create reply
    embedMsg = scholarData.getClaimDate(ctx.author, ctx.message.author.id)
    await ctx.channel.send(embed = embedMsg)

## Show SLP token data
@bot.command(name ='slp')
async def slp_command(ctx):
    """SLP Token information"""
    print("User [ "+str(ctx.author)+" ] used >slp")

    #Create reply
    embedMsg, file = tokenData.drawSlpChart()
    await ctx.channel.send(embed = embedMsg, file=file)

bot.run(botInfo["TOKEN"])
