import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from googleapiclient.http import MediaFileUpload
import os
import json


def send_values_to_table(table_name, operation, score, link="", amount=""):
    CREDENTIALS = os.environ["GOOGLE_CREDITIONALS"]
    spreadsheet_id = os.environ.get("spreadsheet_id")
    
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(CREDENTIALS),
        ["https://www.googleapis.com/auth/spreadsheets", 
        "https://www.googleapis.com/auth/drive"]
        )
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build("sheets", "v4", http = httpAuth)


    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=table_name,
        majorDimension="ROWS"
    ).execute()

    values_len = len(values["values"])
    range_values = f"{table_name}!A{values_len + 1}:E{values_len + 1}"

    post = {
        "date": str(datetime.now()),
        "action": operation,
        "client_link": link,
        "amount": amount,
        "score": score
    }



    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": range_values,
                "majorDimension": "ROWS",
                "values": [[post["date"], post["action"], post["client_link"], post["amount"], post["score"]]]},
        ]
        }
    ).execute()
