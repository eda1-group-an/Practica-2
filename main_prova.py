import logging
import datetime
import os
from mail_manager import utils
from mail_manager.database import Database, DatabaseConfiguration
from mail_manager.email import Email
from mail_manager.exceptions import MailManagerException


email_extension = ".txt"
email_dir = "EmailDB"
email_id = "message1"


def check_for_data(content):

    data = ["Message-ID:","From:","To:","Subject:","Date:"]
    body = [[]]
    text = []
    filled = [None,None,None,None,None]
    changed = False

    for linea in content:
        split = linea.split()
        if (sum(1 for i in range(len(filled)) if filled[i] == None) != 0 and not changed):
            for i in range(len(data)): 
                if data[i] == split[0]:
                    split = split[1:]
                    filled[i] =  " ".join(split)
                    break

        elif split == [] and not changed:
            changed = True

        else:
            split.append(body)
            if split != []:
                body +="\n"

    for line in body:
        text.append(line)
    filled.append(text)
    return filled
def choose_email(email_ids):
    """
    Shows the emails contained in the database and asks the user to choose one

    :param email_ids: list of email ids
    :return: the email id chosen by the user
    """

    email_id = None
    if not email_ids:
        print("There are no emails in the database yet.")

    else:
        print("The database contains the following emails:")
        for idx, name in enumerate(email_ids):
            print("  {}. {}".format(idx + 1, name))

        cancel = False
        while not cancel and not email_id:
            option = read_int_option("Choose an email: (0 to cancel)\n", 0, len(email_ids) + 1)
            if option:
                email_id = email_ids[option - 1]

            elif option == 0:
                cancel = True
                print("Operation cancelled!")

            else:
                print("Invalid option, try again.")

    return email_id

def show_email(db):
    """
    This function calls to the choose_email function and it shows the content of the given email chosen
    by the user in the Database

    :param db: An email database.
    """
    
    email_class=Email()
    email_ids=Database.get_email_ids(db)
    email=choose_email(email_ids)
    email_class.__str__(email)
with open(os.path.join(email_dir,email_id+email_extension),"r") as f:
    content = f.read().splitlines()
show_email(Database)


    #def __init__(self, email_id=None, sender=None, receiver=None, subject=None, date=None, body=None):

