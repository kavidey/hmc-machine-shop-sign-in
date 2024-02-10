# imports and stuff
from server import *  # imports all the functions written in the server python file
import getpass  # this lib allows me to hide user input in the terminal, so it only shows the names and not the ID nums

if __name__ == '__main__':
    # load the Google sheet
    print("accessing database...")
    data = get_google_sheet()
    print("data loaded!")
    print("Swipe ID cards now:")

    # input output stuff
    while True:
        studentIdNum = getpass.getpass(prompt="")
        studentIdNum = studentIdNum[2:-2]
        result, name = check_user_id(str(studentIdNum), data)  # this func returns two variables
        if result:
            print(name + " is cleared to enter the shop!")
        else:
            print("This user is not cleared to enter the shop!")


