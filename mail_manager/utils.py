import os
import re
import logging

from .database import Database, DatabaseConfiguration
from .email import Email
from .exceptions import MailManagerException


def load_email(email_dir, email_id, email_extension='.txt'):
    """
    This function loads the corresponding email object from an email text file.

    :param email_dir: path of the email
    :param email_id:
    :param email_extension:
    :return: it returns an email object
    """
    
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
                        filled[i] = slice(line)
                        break

            elif line == "" and head: #A blank line marks the gap between head and body
                head = False

            else:
                body += line
                if body != "":
                    body += "\n"

        filled.append(body)    
        new_email = Email(filled[0],filled[1],filled[2],filled[3],filled[4],filled[5])

        return new_email

def slice(line):
    """
    Cuts a string where it found an empty space, and it returns the right side.

    :param line: The line that will be cut in half
    :return: The slice of the string at the right of the first empty space
    """
    counter = 0
    for character in line:
        counter += 1
        if character == " ":
            break
    string = line[counter:]
    return string

def write_email(email, db, db_config=None):
    """
    This function writes the email text file corresponding to a given email object.

    :param email: email
    :param db: Database
    :param db_config: Database Configuration
    """
    pass

def delete_email(email, db, db_config=None):
    """
    Removes the email text file corresponding to a given email object (Optional, be careful)

    :param email: email
    :param db: Database
    :param db_config: Database Configuration
    """
    pass

def load_database(db_config):

    """
    Loads database using the information stored in the DatabaseConfiguration object.
    This function creates a Database object, reads the "EMConfig.txt" file and fills the Database object with the
    information found there (folders, emails etc...). For that purpose you will need to make use of the load_email
    function.

    It raises a MailManagerException if it finds an invalid configuration format.

    :param db_config:
    :return: Database object
    """

    with (db_config.get_config_path(),"r") as f:
        content = f.read().splitlines()
        headers = ["Message-ID:","Folders:","Messages:"]
        writing_folders = False
        writing_emails = False
        current_folder = ""

        for linea in content:
            
            if headers[0] in linea:
                seed = slice(linea)
                datab = Database(db_config,seed)
                
        
            elif headers[1] in linea:
                writing_folders = True
                        

            elif headers[2] in linea:
                writing_emails = True
                

            elif writing_folders:
                while (linea != ""):
                    datab.create_folder(linea)
                    headers.append(linea)
                writing_folders = False

            elif writing_emails:
                while (linea != ""):
                    datab.add_email(load_email("emailDB",linea),current_folder)
                writing_emails = False
                      
            elif linea == "":
                pass




def write_database(db, db_config=None):

    """
    Writes the corresponding Email Config File (text file) from a given Database

    :param db: Database
    :param db_config: Database Configuration
    """
    pass

