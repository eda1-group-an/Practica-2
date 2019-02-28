import logging
import datetime
import os
from mail_manager import utils
from mail_manager.database import Database, DatabaseConfiguration
from mail_manager.email import Email
from mail_manager.exceptions import MailManagerException


email_extension = ".txt"
email_dir = "EmailDB"
email_id = "message8"


def check_for_data(content):
    data = ["Date:","From:","To:","Message_ID:","Subject:"]
    filled = [None,None,None,None,None]
    for linea in content:
        split = linea.split()
        if (sum(1 for i in range(len(filled)) if filled[i] == None) != 0):
            for i in range(len(data)): 
                if data[i] in split:
                    filled[i] == split[:data]
                    break
        else:
            if split == "\n":
                pass
                #body = content[:el head]
                #filled.append(body)

                



with open(os.path.join(email_dir,email_id+email_extension),"r") as f:
    content = f.read().splitlines()
    check_for_data(content)


