import json
import scholarFile

#Add new scholar to scholarlist.json
def addToScholarList(discordID, walletAdress):
    with open("scholars/scholars.json", "r+") as file:
        scholarData = {
            "discord_id" : discordID,
            "wallet_adress" : walletAdress
        }
        # First we load existing data into a dict.
        file_data = json.load(file)
        file_data.append(scholarData)
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
    
    return True

#Add new scholar to scholarlist.json
def removeFromScholarList(discordID):
    scholarFound = False
    with open("scholars/scholars.json", "r") as file:
        
        jsonContent = file.read()
        scholarList = json.loads(jsonContent)

        for i in range(len(scholarList)):

            if scholarList[i]["discord_id"] == discordID:
                #remove wallet json file
                scholarFile.deleteScholarFile(scholarList[i]["wallet_adress"])
                #remove from list
                scholarList.pop(i)
                scholarFound = True
                break
    if scholarFound:
        with open('scholars/scholars.json', 'w') as data_file:
            data = json.dump(scholarList, data_file)
        return True
    else:
        return False