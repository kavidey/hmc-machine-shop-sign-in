# imports and stuff
import pygsheets
import datetime
import dateutil.parser
import atexit

# defining constants and stuff
SPREADSHEET_KEY = "1tbupPMYpxyRwSO7UIOGVxNreyMRhvirPiG8QTPskf4w"  # the key in the url of the spreadsheet
ID_WORKSHEET_NAME = "Form Responses 1"  # the name of the worksheet in the spreadsheet
LOG_WORKSHEET_NAME = "Log" # This is unused
SERVICE_FILE = "service_file.json"  # filename of client secret

# Spreadsheet Column Mappings
DATE_COL = 0
SCORE_COL = 2
NAME_COL = 4
ID_COL = 5

# Minimum Passing Score (must be >= 60)
MIN_PASSING_SCORE = 60


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
    # Scan all rows except for the first 3 which are header rows
    for row in data[3:]:
        # Check if the row matches the user
        if row[ID_COL] and (row[ID_COL] in userID):
            # Calculate what the user stored on the quiz
            # row[SCORE_COL] is a string in the form "XX / 64"
            # We split it into ["XX", "/", "64"], then get the first item: "XX" and convert that into an integer
            quiz_score = int(row[SCORE_COL].split()[0])
            # Check if the user passed the quiz
            if quiz_score >= MIN_PASSING_SCORE:
                # Check if the date that the user passed the quiz is within the last year
                if dateutil.parser.parse(row[DATE_COL]) > datetime.datetime.now()-datetime.timedelta(days=365):
                    return True, row[NAME_COL]
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




