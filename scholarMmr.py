import json
import requests
import discord
import scholarSlp, scholarHistory
from quickchart import QuickChart

#Function to get scholar data from skymavis
def getScholarData(walletAdress):
    """Retrieve data from specific wallet from Sky Mavis API"""

    getScholarData = "https://game-api.skymavis.com/game-api/leaderboard?client_id="+ walletAdress +"&offset=0&limit=0" #should be put in config.ini
    callScholarData = requests.get(getScholarData)
    scholarDataBinary = callScholarData.content
    scholarData = json.loads(scholarDataBinary)

    return scholarData

#function to creat earning report
def createMmrReport(author, discordID):

    walletAddress = scholarSlp.getScholarWalletAdress(discordID)
    scholarData = getScholarData(walletAddress)

    #Mapping from getScholarData
    rank = scholarData['items'][1]['rank']
    rating = scholarData['items'][1]['elo']
    win = scholarData['items'][1]['win_total']
    draw = scholarData['items'][1]['draw_total']
    lose = scholarData['items'][1]['lose_total']
    totalPlayed = win + draw + lose

    #Prepare the data
    scholarEarningHistory = scholarHistory.getScholarMmrHistory(walletAddress)

    labels = []
    mmrElo = []
    i = 0
    while i < 15:
        labels.append(scholarEarningHistory[i]["date"])
        mmrElo.append(scholarEarningHistory[i]["mmr"])
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
                "backgroundColor": 'rgba(35, 90, 155, 0.5)',
                "borderColor": 'rgb(35, 90, 155)',
                "data": mmrElo,
                "label": 'MMR',
                "fill": 'start',
            },
            ],
        },
        "options": {
            "title": {
            "text": 'MMR past days',
            "display": "true",
            },
        },
    }
    # Write a file
    qc.to_file("tmp/mymmr.png")

    #Create embedded message
    embedMsg = discord.Embed(title="MMR report of "+str(author), description=" \n Mmr report of "+str(author), color=0x39fc03)
    embedMsg.add_field(name="MMR", value=str(rating), inline=False)
    embedMsg.add_field(name="Rank", value=str(rank), inline=False)
    
    embedMsg.add_field(name="Wins", value=str(win), inline=True)
    embedMsg.add_field(name="Draws", value=str(draw), inline=True)
    embedMsg.add_field(name="Losses", value=str(lose), inline=True)

    file = discord.File("tmp/mymmr.png", filename="image.png")
    embedMsg.set_image(url="attachment://image.png")
    return embedMsg, file