from notion.client import NotionClient
from notion.collection import NotionDate
from time import strftime
from datetime import datetime, date,timedelta
from twilio.rest import Client


# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2="[YOUR TOKEN V2 (FROM COOKIES)]")

# Your Account Sid and Auth Token from twilio account
account_sid = "[TWILIO ACCOUT SID]"
auth_token = "[TWILIO AUTH TOKEN]"
myPhoneNumber = "[YOUR PHONE NUMBER (+33x xx xx xx xx for France)]"
twilioPhoneNumber = "[TWILIO PHONE NUMBER]"

twilioClient = Client(account_sid, auth_token)

# Access a database using the URL of the database page or the inline block
cvListeTotale = client.get_collection_view("[LINK TO MAIN DATABASE WITH ALL TASK TO DO]")
cvListeUrgente = client.get_collection_view("[LINK TO URGENT DATABASE]")
cvListeFinies = client.get_collection_view("[LINK TO THE DATABASE WITH ALL DONE TASK]")

def switchRowFromDatabase(toDatabase,row):
    print("switchRowFromDataBase")
    rowToAdd = toDatabase.collection.add_row()
    rowToAdd.Matière = row.Matière
    rowToAdd.Sujet = row.Sujet
    rowToAdd.Done = row.Done
    rowToAdd.Date = row.Date
    deleteRow(row)

def deleteRow(row):
    row.remove()

def checkAndMoveUrgentTask():
    dateToday = datetime.today()
    for row in cvListeTotale.collection.get_rows():

        dateTaskNotion = datetime.strptime(row.Date.start.strftime("%Y-%m-%d"),"%Y-%m-%d") 
        dateMinusTwoDays = dateTaskNotion + timedelta(days=-2)

        if dateToday > dateMinusTwoDays:
            switchRowFromDatabase(cvListeUrgente,row)
            sendSms(row.Matière,row.Sujet,dateTaskNotion)

def sendSms(matiere,sujet,date):
    sujetMessage = f"RAPPEL : Rendu à faire en {matiere}. Sujet : \"{sujet}\" pour le {date}"
    message = twilioClient.messages.create(body=sujetMessage, from_=twilioPhoneNumber, to=myPhoneNumber)

def checkAndMoveDoneTask():
    for row in cvListeTotale.collection.get_rows():
        if(row.Done == True):
            switchRowFromDatabase(cvListeFinies,row)

if __name__ == "__main__":
    checkAndMoveUrgentTask()
    checkAndMoveDoneTask()

