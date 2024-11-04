import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import os
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Define the scope for the API request
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Path to the service account key file (JSON)
service_account_file = os.getenv['GOOGLE_APPLICATION_CREDENTIALS']

# The ID of the spreadsheet and the range of data to read
spreadsheet_id = '1s_2X45SpcQCqwkoM3BjqIxtZYtoVYhpDVw9chsC1PiE'

def etl():
    # Authenticate using service account
    creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    
    # Build the service object for the Sheets API
    service = build('sheets', 'v4', credentials=creds)
    
    # Call the Sheets API to get the data
    sheet = service.spreadsheets()
    sheet_names = sheet.get(spreadsheetId=spreadsheet_id).execute().get('sheets', [])
    
    for sheet_name in sheet_names:
        sheet_name = sheet_name['properties']['title']
        sheet_data = sheet.values().get(spreadsheetId = spreadsheet_id, range = sheet_name).execute()
        sheet_data = sheet_data.get('values', [])
        sheet_data = pd.DataFrame(sheet_data)
        sheet_data.columns = sheet_data.iloc[0]
        sheet_data = sheet_data[1:]
        if sheet_name == 'customers1':
            sheet_data['gender'] = sheet_data['gender'].map({'M':1, 'F':0})

            # na_processing = customer[['gender','income']]
            imputer = KNNImputer(n_neighbors = 5)

            sheet_data['gender'] = imputer.fit_transform(sheet_data[['gender']])
            sheet_data['income'] = imputer.fit_transform(sheet_data[['income']])
            sheet_data.to_csv(f"s3://reward-offer/dim_{sheet_name}.csv", index=False)
        else:
            sheet_data.to_csv(f"s3://reward-offer/dim_{sheet_name}.csv", index=False)

etl()