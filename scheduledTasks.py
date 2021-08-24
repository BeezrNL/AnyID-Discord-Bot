## THIS FILE RUNS EVERY DAY AT MIDNIGHT AS A SCHEDULED TASK TO CALCULATE SLP EARNINGS 
# !!! SHOULD ALWAY RUN AT END OF DAY !!!
import json
from datetime import datetime
import scholarData

currentDate = datetime.today().strftime('%Y-%m-%d')

#Load list of scholars
scholarList = {}
with open('scholars/scholars.json') as f:
    jsonContent = f.read()
    scholarList = json.loads(jsonContent)

for scholar in scholarList:

    currentScholarData = scholarData.getScholarData(scholar["wallet_adress"])
    totalSlp = currentScholarData["total"]

    with open("scholars/"+ scholar["wallet_adress"] +".json", "r+") as file:   
        newScholarData = {"date": currentDate, "total_slp": totalSlp}
        # First we load existing data into a dict.
        file_data = json.load(file)
        file_data.append(newScholarData)
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
