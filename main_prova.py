import logging
import datetime

from mail_manager import utils
from mail_manager.database import Database, DatabaseConfiguration
from mail_manager.email import Email
from mail_manager.exceptions import MailManagerException

utils.load_email("emailDB","message1")