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

db_config = DatabaseConfiguration("emailDB")
db = utils.load_database(db_config)

to_remove = db.emails.get_head()
to_remove = to_remove.next.next.data
db.emails.remove(to_remove)
