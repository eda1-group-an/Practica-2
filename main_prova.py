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

with open(os.path.join(email_dir,email_id+email_extension),"r") as f:
    content = f.read().splitlines()
    email = check_for_data(content)
    new_email = Email(email[0],email[1],email[2],email[3],email[4],email[5])
    print(new_email)

    #def __init__(self, email_id=None, sender=None, receiver=None, subject=None, date=None, body=None):

