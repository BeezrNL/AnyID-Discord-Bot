import requests
import json
from datetime import datetime, timedelta
import discord
import tokenData
from quickchart import QuickChart

import scholarHistory

#These functions lack errorhandling

#Function to get scholarwallet
def getScholarWalletAdress(discordID):
    """Get scholar walletaddress based on discordID"""
    
    scholarList = {}
    with open('scholars/scholars.json') as f:
        jsonContent = f.read()
        scholarList = json.loads(jsonContent)

    #look for message.author in scholars list
    for x in scholarList:
        if x["discord_id"] == str(discordID):
            wallet = x["wallet_adress"]
            break

    return wallet

#Function to get scholar data from skymavis
def getScholarData(walletAdress):
    """Retrieve data from specific wallet from Sky Mavis API"""

    getScholarData = "https://game-api.skymavis.com/game-api/clients/"+ walletAdress +"/items/1" #should be put in config.ini
    callScholarData = requests.get(getScholarData)
    scholarDataBinary = callScholarData.content
    scholarData = json.loads(scholarDataBinary)

    return scholarData

#function to get claim date
def getClaimDate(author, discordID):
    """Calculate when SLP from author can be claimed"""

    walletAdress = getScholarWalletAdress(discordID)
    scholarData = getScholarData(walletAdress)

    #Calculate pay-out date
    timestamp = scholarData['last_claimed_item_at']
    lastClaim = datetime.fromtimestamp(timestamp)
    claimDate = lastClaim + timedelta(days=14)

    embedMsg = discord.Embed(title="SLP claim date", description="Date when SLP can be claimed for "+ str(author), color=0x39fc03)
    embedMsg.add_field(name="Claim date", value=claimDate, inline=False)

    return embedMsg



#function to creat earning report
def createEarnReport(author, discordID):

    walletAddress = getScholarWalletAdress(discordID)
    scholarData = getScholarData(walletAddress)

    #Mapping from getScholarData
    totalSlp = scholarData["total"]
    lastClaimedTimestamp = scholarData['last_claimed_item_at']
    
    #Calculate average SLP/day
    lastClaimedDate = datetime.fromtimestamp(lastClaimedTimestamp)
    now = datetime.now()
    days = (now - lastClaimedDate).days

    if days == 0:
        days = 1
    if totalSlp == 0:
        totalSlp = 1

    #Calulated fields
    avgSlpDay = round(totalSlp / days, 1)
    slpValueInUsd = round(tokenData.getSlpPrice("usd") * totalSlp, 2)
    slpValueInEur = round(tokenData.getSlpPrice("eur") * totalSlp, 2)
    slpValueInPhp = round(tokenData.getSlpPrice("php") * totalSlp, 2)

    #Prepare the data
    scholarEarningHistory = scholarHistory.getScholarEarningHistory(walletAddress)

    labels = []
    slpEarned = []
    i = 0
    while i < 15:
        labels.append(scholarEarningHistory[i]["date"])
        slpEarned.append(scholarEarningHistory[i]["total_slp"])
        i += 1
        
    #Draw chart
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": 'line',
        "data": {
            "labels": labels,
            "datasets": [
            {
                "backgroundColor": 'rgba(245, 158, 27, 0.5)',
                "borderColor": 'rgb(245, 158, 27)',
                "data": slpEarned,
                "label": 'SLP',
                "fill": 'start',
            },
            ],
        },
        "options": {
            "title": {
            "text": 'SLP earned past days',
            "display": "true",
            },
        },
    }
    # Write a file
    qc.to_file("tmp/myslp.png")

    if totalSlp - scholarEarningHistory[-1]["total_slp"] > 0:
        earnedToday = totalSlp - scholarEarningHistory[-1]["total_slp"]
    else:
        earnedToday = 0

    if scholarEarningHistory[-1]["total_slp"] - scholarEarningHistory[-2]["total_slp"] > 0:    
        earnedYesterday = scholarEarningHistory[-1]["total_slp"] - scholarEarningHistory[-2]["total_slp"]
    else:
        earnedToday = 0

    #Create embedded message
    embedMsg = discord.Embed(title="Earning report of "+str(author), description=" \n The values below is the total amount earned. As per terms you will receive 50% of the total SLP farmed.", color=0x39fc03)
    embedMsg.add_field(name="Total SLP since last payout", value=str(totalSlp)+" SLP", inline=False)
    
    embedMsg.add_field(name="Total SLP in USD", value=str(slpValueInUsd) +" USD ", inline=True)
    embedMsg.add_field(name="Total SLP in EUR", value=str(slpValueInEur) +" EUR ", inline=True)
    embedMsg.add_field(name="Total SLP in PHP", value=str(slpValueInPhp) +" PHP ", inline=True)

    embedMsg.add_field(name="Earned today", value=str(earnedToday) + " SLP", inline=True)
    embedMsg.add_field(name="Earned yesterday", value=str(earnedYesterday) + " SLP", inline=True)
    embedMsg.add_field(name="Average SLP/day", value=str(avgSlpDay) + " SLP ", inline=True)

    file = discord.File("tmp/myslp.png", filename="image.png")
    embedMsg.set_image(url="attachment://image.png")
    return embedMsg, file
