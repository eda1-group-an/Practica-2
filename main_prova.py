import logging
import datetime
import os
from mail_manager import utils
from mail_manager.database import Database, DatabaseConfiguration
from mail_manager.email import Email
from mail_manager.exceptions import MailManagerException


email_extension = ".txt"
email_dir = "EmailDB"
email_id = "CAFdmR09@mail.gmail.com"


with open(os.path.join(email_dir,email_id+email_extension),"r") as f:

    content = f.read().splitlines()

    data = ["Message-ID:","From:","To:","Subject:","Date:"]
    body = ""
    filled = [None]*5
    head = True #Controls if the head is over

    for line in content: #We look at every line of the file
        if (sum(1 for i in range(len(filled)) if filled[i] == None) != 0 and head): #It checks if there's data not filled and whether we are on the head or not
            for i in range(len(data)): 
                if data[i] in line:
                    counter = 0
                    for character in line:
                        counter += 1
                        if character == " ":
                            break
                    filled[i] = line[counter:]
                    break

        elif line == "" and head:
            head = False

        else:
            body += line
            if body != "":
                body += "\n"

    filled.append(body)    
    new_email = Email(filled[0],filled[1],filled[2],filled[3],filled[4],filled[5])


print(new_email)


