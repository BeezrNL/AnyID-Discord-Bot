from datetime import timedelta,date
import json
import requests
import discord
from quickchart import QuickChart


def getSlpPrice(currency):
    #Get SLP price in USD from coingecko
    getSlpPrice = "https://api.coingecko.com/api/v3/coins/markets?vs_currency="+currency+"&ids=smooth-love-potion"
    slpPriceData = requests.get(getSlpPrice)
    slpPriceBinary = slpPriceData.content
    slpPrice = json.loads(slpPriceBinary)
    slpValue = slpPrice[0]['current_price']

    return slpValue

def getCirculatingSlp():
    getTotalSLP = "https://explorer.roninchain.com/api/token/0xa8754b9fa15fc18bb59458815510e40a12cd2014"
    totalSlpData = requests.get(getTotalSLP)
    totalSlpBinary = totalSlpData.content
    totalSlp = json.loads(totalSlpBinary)

    return totalSlp["total_supply"]

def drawSlpChart():

    #Get SLP price in USD from coingecko
    getSlpSupply = "https://www.axieworld.com/api/charts/slp-issuance"
    slpSupplyData = requests.get(getSlpSupply)
    slpSupplyBinary = slpSupplyData.content
    slpSupply = json.loads(slpSupplyBinary)

    #Prepare the data
    chartData = []
    daysBack = 8
    i = 1
    while i < daysBack:
        if i > 1:
            dayDate = date.today() - timedelta(days=i-1)
        else:
            dayDate = date.today()
        dayData = {
            "day" : dayDate,
            "minted" : round(slpSupply["data"]["minted"][-i] / 1000000, 1),
            "burned" : round(slpSupply["data"]["burned"][-i] / 1000000, 1)
        }
        chartData.append(dayData)
        i += 1
    
    #Draw the SLP burned vs minted chart
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": [chartData[6]["day"], chartData[5]["day"], chartData[4]["day"], chartData[3]["day"], chartData[2]["day"], chartData[1]["day"],chartData[0]["day"]],
            "datasets": [{
                "label": 'Minted',
                "backgroundColor": 'rgb(245, 158, 27)',
                "stack": 'Stack 0',
                "data": [chartData[6]["minted"], chartData[5]["minted"], chartData[4]["minted"], chartData[3]["minted"], chartData[2]["minted"], chartData[1]["minted"], chartData[0]["minted"]],
            },
            {
                "label": 'Burned',
                "backgroundColor": 'rgb(35, 90, 155)',
                "stack": 'Stack 1',
                "data": [chartData[6]["burned"], chartData[5]["burned"], chartData[4]["burned"], chartData[3]["burned"], chartData[2]["burned"], chartData[1]["burned"], chartData[0]["burned"]],
            },
            ]
        },
        "options": {
            "plugins": {
                "datalabels": {
                    "anchor": 'end',
                    "align": 'top',
                    "color": '#fff',
                    "backgroundColor": 'rgba(54, 57, 63, 1.0)' 
                },
            },
            "title": {
                "display": "true",
                "text": "SLP minted vs burned (in millions)",
            },
            "tooltips": {
                "mode": "index",
                "intersect": "false",
            },
            "responsive": "true",
        },
    }
    #Save file to chart to show in discord response message
    qc.to_file("tmp/slpMintedVsBurned.png")
    
    # #total SLP supply
    totalSlpIngame = getCirculatingSlp()

    embedMsg = discord.Embed(title="SLP data", description=" \n Usefull SLP data like prices and minted vs burned SLP.", color=0x39fc03)
    embedMsg.add_field(name="Total circulating SLP supply", value=totalSlpIngame, inline=False)
    embedMsg.add_field(name="SLP/USD", value=getSlpPrice("usd"), inline=True)
    embedMsg.add_field(name="SLP/EUR", value=getSlpPrice("eur"), inline=True)
    embedMsg.add_field(name="SLP/PHP", value=getSlpPrice("php"), inline=True)
    file = discord.File("tmp/slpMintedVsBurned.png", filename="image.png")
    embedMsg.set_image(url="attachment://image.png")
    
    #return embedMsg, file
    return embedMsg, file