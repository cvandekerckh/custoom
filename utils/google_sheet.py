import argparse
import logging
import os
import pickle as pkl
import time

import numpy as np
import pandas as pd

import gspread
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


logger = logging.getLogger(__name__)


# This file creates a google sheet
# from the summary document generate by factor overview
# Note : cannot be run in docker since gspread not available

HOME_DIR = os.path.expanduser('~')
CLIENT_SECRET_FILE = os.path.join(HOME_DIR, 'client_secret.json')
CREDENTIALS_DIR = os.path.join(HOME_DIR, '.credentials')
OAUTH_TOKEN_PATH = os.path.join(CREDENTIALS_DIR,
                                'sheets.googleapis.com-python-quickstart.json')

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
]
APPLICATION_NAME = 'Google Sheets API'
DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'


def setup_credentials():
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Authenticated oauth2client.client.OAuth2Credentials object.
    """
    flags, _ = argparse.ArgumentParser(parents=[tools.argparser]).parse_known_args()
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)
    store = Storage(OAUTH_TOKEN_PATH)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        tools.run_flow(flow, store, flags)
        print('Storing credentials to %s', OAUTH_TOKEN_PATH)
    return credentials


def get_credentials():
    """Get valid user credentials from storage.

    If nothing has been stored, throw a `ValueError`.

    Returns:
        Authenticated oauth2client.client.OAuth2Credentials object.
    """
    store = Storage(OAUTH_TOKEN_PATH)
    credentials = store.get()
    if not credentials or credentials.invalid:
        raise ValueError('Credentials not set up yet! Follow the README for instructions.')
    return credentials


def get_worksheets(sheet_reference):
    flag = False
    while not flag:
        try:
            credentials = setup_credentials()
            gc = gspread.authorize(credentials)
            sp = gc.open_by_key(sheet_reference)
            return sp.worksheets()
        except gspread.exceptions.APIError as e:
            if e.response.status_code==429:
                print("Sleeping a bit... it is good for health")
                time.sleep(60)
            else:
                print(e)
                raise


def read_spreadsheet(sheet_reference, tab_name):
    flag = False
    while not flag:
        try:
            credentials = setup_credentials()
            gc = gspread.authorize(credentials)
            sp = gc.open_by_key(sheet_reference)
            ws_desc = sp.worksheet(tab_name)
            data = ws_desc.get_all_values()
            headers = data.pop(0)
            df = pd.DataFrame(data, columns=headers)
            flag=True
        except gspread.exceptions.APIError as e:
            if e.response.status_code==429:
                print("Sleeping a bit... it is good for health")
                time.sleep(60)
            else:
                print(e)
                raise


    return df


def numberToLetters(q):
    q = q - 1
    result = ''
    while q >= 0:
        remain = q % 26
        result = chr(remain+65) + result
        q = q//26 - 1
    return result


def empty_update(sp, ws):
    ws_id = ws.id
    sp.batch_update(
        {
            "requests": [
                {
                    "updateCells": {
                        "range": {
                            "sheetId": ws_id,
                        },
                        "fields": "*",
                    },
                },
            ],
        },
    )


def df_to_sheet(
    df,
    ws,
    sp,
    ptr=(1,1),
    header=True,
    check_entries=[],
    coin_entry=None,
):

    # COIN ENTRY
    if coin_entry:
        ws.update_acell(f'A{ptr[0]}', coin_entry)

    # HEADER
    if header:
        # columns names
        columns = df.columns.values.tolist()
        # selection of the range that will be updated
        y_start = numberToLetters(2+ptr[1])
        x_start = ptr[0]
        y_end = numberToLetters(len(columns)+1+ptr[1])
        x_end = ptr[0]
        cell_list = ws.range(f'{y_start}{x_start}:{y_end}{x_end}')
        # modifying the values in the range
        for cell in cell_list:
            val = columns[cell.col-2-ptr[1]]
            cell.value = val

        # update in batch
        ws.update_cells(cell_list)

    # INDEX
    # row names
    indices = df.index.tolist()
    # selection of the range that will be updated
    y_start = numberToLetters(1+ptr[1])
    x_start = ptr[0]+1
    y_end = numberToLetters(1+ptr[1])
    x_end = len(indices)+ptr[0]
    cell_list = ws.range(f'{y_start}{x_start}:{y_end}{x_end}')
    # modifying the values in the range
    for cell in cell_list:
        val = indices[cell.row-1-ptr[0]]
        cell.value = val
    # update in batch
    ws.update_cells(cell_list)

    # VALUE

    # number of lines and columns
    num_lines, num_columns = df.shape
    # selection of the range that will be updated
    y_start = numberToLetters(2+ptr[1])
    x_start = ptr[0]+1
    y_end = numberToLetters(num_columns+1+ptr[1])
    x_end = num_lines+ptr[0]
    cell_list = ws.range(f'{y_start}{x_start}:{y_end}{x_end}')
    # modifying the values in the range
    for cell in cell_list:
        val = df.iloc[cell.row-1-ptr[0], cell.col-2-ptr[1]]
        if isinstance(val, (int, float)):
            # note that we round all numbers
            val = float(round(val, 4))
        cell.value = val
    # update in batch
    ws.update_cells(cell_list)


def prepare_sheet(sheet_reference, tab_name):
    credentials = setup_credentials()
    gc = gspread.authorize(credentials)
    sp = gc.open_by_key(sheet_reference)
    ws = sp.worksheet(tab_name)
    return ws, sp


def clear_sheets(spreadsheets):
    for sheet_reference in spreadsheets:
        tab_names = spreadsheets[sheet_reference]
        for tab_name in tab_names:
            clear_sheet(sheet_reference, tab_name)


def clear_sheet(sheet_reference, tab_name):
    flag = False
    while not flag:
        try:
            credentials = setup_credentials()
            gc = gspread.authorize(credentials)
            sp = gc.open_by_key(sheet_reference)
            ws = sp.worksheet(tab_name)
            empty_update(sp, ws)
            flag=True
        except gspread.exceptions.APIError as e:
            if e.response.status_code==429:
                print("Sleeping a bit... it is good for health")
                time.sleep(60)
            else:
                print(e)
                raise


def push_df_to_sheet(df, sheet_reference, tab_name, ptr=(1,0)):
    flag = False
    while not flag:
        try:
            df = prepare_for_google_sheet(df)
            ws, sp = prepare_sheet(sheet_reference, tab_name)
            df_to_sheet(df, ws, sp, ptr=ptr)
            flag=True
        except gspread.exceptions.APIError as e:
            if e.response.status_code==429:
                print("Sleeping a bit... it is good for health")
                time.sleep(60)
            else:
                print(e)
                raise


def prepare_for_google_sheet(df, fillna=0.0):
    # Google sheets does not accept bools, ints and NaNs
    for col in df:
        if df.loc[:,col].dtype == np.int64:
            df.loc[:,col] = df.loc[:,col].astype(np.float64)
        elif df[col].dtype == np.bool:
            df.loc[:,col] = df.loc[:,col].astype(str)
        elif df[col].dtype != np.float64:
            df.loc[:,col] = df.loc[:,col].astype(str)
    df = df.fillna(fillna)
    return df


def push_file_to_sheet(filename, sheet_reference, tab_name):
    flag = False
    while not flag:
        try:
            ws, sp = prepare_sheet(sheet_reference, tab_name)
            df = pd.read_csv(filename, index_col=0)
            df = prepare_for_google_sheet(df)
            df_to_sheet(df, ws, sp)
            flag=True
        except gspread.exceptions.APIError as e:
            if e.response.status_code==429:
                print("Sleeping a bit... it is good for health")
                time.sleep(60)
            else:
                print(e)
                raise


def db_to_sheet(table, con, sheet_reference, tab_name, index_col="id"):
    df = pd.read_sql(table, con)
    df = df.set_index(index_col)
    df = df.tail(50)
    clear_sheet(sheet_reference, tab_name)
    push_df_to_sheet(df, sheet_reference, tab_name, ptr=(1,0))

