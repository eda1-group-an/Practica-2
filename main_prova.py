import logging
import datetime
import os
from mail_manager import utils
from mail_manager.database import Database, DatabaseConfiguration
from mail_manager.email import Email
from mail_manager.exceptions import MailManagerException




db_config = DatabaseConfiguration("emailDB")
db = utils.load_database(db_config)

print(db.emails)
