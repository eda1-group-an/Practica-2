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

def slice(line, side=None):
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
    
    if not side:
        string = line[counter:]
    else:
        string = line[:counter-1]

    return string

def write_email(email, db, db_config=None):
    """
    This function writes the email text file corresponding to a given email object.

    :param email: email
    :param db: Database
    :param db_config: Database Configuration
    """
    with open(db_config.get_file_path(),"w") as f:
        f.write(email.template.format(email))

def delete_email(email, db, db_config=None):
    """
    Removes the email text file corresponding to a given email object (Optional, be careful)

    :param email: email
    :param db: Database
    :param db_config: Database Configuration
    """

    ## If file exists, delete it ##
    try:
        path = db_config.get_file_path(email.data.id)
        os.remove(path)
    else:    ## Show an error ##
        raise MailManagerException("File not found!")

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

    with open(db_config.get_config_path(),"r") as f:
        content = f.read().splitlines()
        headers = ["Message-ID:","Folders:","Messages:"]
        folders = [] #For error control

        try:
            for linea in content:
                
                if headers[0] in linea: #Case 1: Create the db with the seed given
                    seed = slice(linea)
                    datab = Database(db_config,seed)

                elif linea == "":
                    writing_folders = False
                    writing_emails = False
                    
                elif headers[1] in linea: #Case 2: After word Folders: we start the mode writing_folders
                    writing_folders = True
                
                elif writing_folders:  
                    datab.create_folder(linea)
                    folders.append(linea)
                        
                elif headers[2] in linea: #Case 3: After word Messages: we start the mode writing_emails
                    writing_emails = True
                    current_folder = slice(linea,1) #We take the name of the folder
                    folders.pop(0) #The folders mails list appear in the order we created them

                elif writing_emails:
                    emails = datab.get_email_ids(current_folder)
                    if linea not in emails:
                        datab.add_email(load_email("emailDB",linea),current_folder)
                        
                elif linea == "End":
                    break
        except:
            raise MailManagerException("EMConfig has some mistakes")

        if folders == []:
           return datab
        else:
            raise MailManagerException("EMConfig has some mistakes")

def write_database(db, db_config=None):

    """
    Writes the corresponding Email Config File (text file) from a given Database

    :param db: Database
    :param db_config: Database Configuration
    """
    with open(db_config.get_config_path(),"w") as f:
        f.write("Message-ID: "+ db.email_id_seed+"\n")
        
        f.write("\n")
        
        f.write("Folders:"+"\n")
        for folder in db.folders:
            f.write(db.folders[folder].name+"\n")
        
        f.write("\n")

        for folder in db.folders:
            f.write(db.folders[folder].name+" Messages:\n")
            current = db.folders[folder].get_head()
            while current != None:
                f.write(current.data.id+"\n")
                current = current.next
            f.write("\n")


        f.write("End")



