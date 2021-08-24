import os.path
from datetime import datetime
import json

def createScholarFile(filename):
    file_exists = os.path.isfile("scholars/"+filename+".json")
    if not file_exists:
        currentDate = datetime.today().strftime('%Y-%m-%d')

        addScholarData = [{"date": currentDate, "total_slp": 0, "mmr":0}]
        addScholarDataJson = json.dumps(addScholarData)

        f=open("scholars/"+ filename +".json","w+")
        f.write(addScholarDataJson)
        f.close()
    
    return True

def deleteScholarFile(filename):
    if os.path.exists("scholars/"+filename+".json"):
        os.remove("scholars/"+filename+".json")
    else:
        print("file not found!")
