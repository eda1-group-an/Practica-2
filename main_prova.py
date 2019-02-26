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

with open(os.path.join(email_dir,email_id+email_extension),"r") as f:
    content = f.read().splitlines()
    for linea in content:
        print(linea)
