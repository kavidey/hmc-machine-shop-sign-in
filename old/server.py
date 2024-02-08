# imports and stuff
import pygsheets
import datetime
import dateutil.parser
import atexit

# defining constants and stuff
SPREADSHEET_KEY = "1wsgUJq9N3m3OEQtRQ08um80dt9giS_gtsw3J_wKfm-4"  # the key in the url of the spreadsheet
ID_WORKSHEET_NAME = "Raw"  # the name of the worksheet in the spreadsheet
LOG_WORKSHEET_NAME = "Log"
SERVICE_FILE = "service_file.shop.json"  # filename of client secret

DATE_COL = 1
ID_COL = 3


def get_google_sheet():
    """
    accesses the Google Drive file using the service file and 'pygsheets' library
    loads them into a 2d array
    :return: a 2d array with the values from the spreadsheet and worksheet specified in server.py
    """
    client = pygsheets.authorize(service_file=SERVICE_FILE)
    spreadsheet = client.open_by_key(SPREADSHEET_KEY)
    worksheet = spreadsheet.worksheet_by_title(ID_WORKSHEET_NAME)
    return worksheet.get_all_values(returnas='matrix')


def check_user_id(userID, data):
    """
    checks to see if the userID is in data 
    :param userID: the student ID that needs to be checked
    :param data: 2d array representing the datasheet
    :return: boolean value stating if userID is in data
    """

    for row in data:
        # the ID values of registered shop users are in the fourth column of the spreadsheet
        if row[ID_COL] == userID:
            if dateutil.parser.parse(row[DATE_COL]) > datetime.datetime.now()-datetime.timedelta(days=365):
                return True, row[0]
    return False, None


def update_log_spreadsheet(data):
    """
    updates the log spreadsheet with all the log data from the current session
    :param data: a list of lists in the format (time, name, userID)
    :return: nothing for this program
    """
    client = pygsheets.authorize(service_file=SERVICE_FILE)
    spreadsheet = client.open_by_key(SPREADSHEET_KEY)
    worksheet = spreadsheet.worksheet_by_title(LOG_WORKSHEET_NAME)
    print(worksheet.get_all_values(returnas='matrix'))




