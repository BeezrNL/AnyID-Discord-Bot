import json

#function to get scholar slp earning history
def getScholarEarningHistory(walletAddress):
    with open("scholars/"+ walletAddress +".json", "r") as getScholarEarnings:
        scholarEarningContent = getScholarEarnings.read()
        scholarEarning = json.loads(scholarEarningContent)
    return scholarEarning

#function to get scholar slp earning history
def getScholarMmrHistory(walletAddress):
    with open("scholars/"+ walletAddress +".json", "r") as getScholarMmr:
        getScholarMmrContent = getScholarMmr.read()
        scholarMmr = json.loads(getScholarMmrContent)
    return scholarMmr