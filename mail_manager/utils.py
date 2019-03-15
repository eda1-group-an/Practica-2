#NIA's: 217447, 217723, 194985. Group Code: AN. Professor: Sergio Ivan Giraldo 
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
    try: 
        with open(os.path.join(email_dir,email_id+email_extension),"r") as f:

            content = f.read().splitlines() # we divide all the content into lines on a list

            data = {"Message-ID:":"","From:":"","To:":"","Subject:":"","Date:":""} #Keywords of the fields
            body = ""
            head = True #Controls wether the head is over

            for line in content: #We look at every line of the file
                if ("" in data.values()) and head: #It checks if there's data not filled and whether we are on the head or not
                    for keyword in data: 
                        if keyword in line:
                            data[keyword] = slice(line,"right")
                            break

                elif line == "" and head: #A blank line marks the gap between head and body
                    head = False

                else:
                    body += line
                    body += "\n" #We want to respect the original spacing

            if head ==True:
                raise MailManagerException("Mail has some mistakes")
    
    except FileNotFoundError:
        raise MailManagerException("Mail not found...")


    new_email = Email(data["Message-ID:"],data["From:"],data["To:"],data["Subject:"],data["Date:"],body)
    return new_email #we pack all the info into an Email object and return it

def slice(line, side):
    """
    Cuts a string where it found an empty space, and it returns one of the two sides.

    :param line: The line that will be cut in half
    :param side: The side that will be kept after the cut
    :return: The slice of the string at the right or left of the first empty space
    """
    # Although it's not a function that alters something physically, it's needed for the functions here, so thats why it's in utils
    
    counter = 0 #To know where to cut
    do_not_keep_the_space = 1 #To remove the blank space when keeping the left part

    for character in line:
        counter += 1
        if character == " ": #When we find an empty space, we stop the loop
            break
    
    if side == "right":
        string = line[counter:] 

    elif side == "left":
        string = line[:counter-do_not_keep_the_space]

    return string

def write_email(email, db, db_config=None):
    """
    This function writes the email text file corresponding to a given email object.

    :param email: email
    :param db: Database
    :param db_config: Database Configuration
    """
    #This function does not check parameters. All is checked in the db or the main! Reasons why we do this on the handout
    try:
        with open(os.path.join(db.db_config.email_dir,email.id+db.db_config.email_extension), "w") as new:
            new.write(email.template.format(email))
    except:
        raise MailManagerException("No email database detected!")
    
def delete_email(email, db, db_config=None):
    """
    Removes the email text file corresponding to a given email object (Optional, be careful)

    :param email: email
    :param db: Database
    :param db_config: Database Configuration
    """
    #This function does not check parameters. All is checked in the db or the main! Reasons why we do this on the handout
    try:
        os.remove(db.db_config.get_email_path(email.id))
    except FileNotFoundError:
        raise MailManagerException("Mail not found...")

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
        folders = [] #For error control
        inbox_present = False #To check for the folder
        outbox_present = False #To check for the folder

        try: #For general errors managing. 

            for linea in content:
                if "Message-ID:" in linea: #Case 1: Create the db with the seed given
                    seed = slice(linea,"right")
                    datab = Database(db_config,int(seed))
                    
                elif linea == "": #When we find a blank line, we reset what we're doing and start over askin where we are
                    writing_folders = False
                    writing_emails = False
                    
                elif "Folders:" in linea: #Case 2: After word Folders: we start the mode writing_folders
                    writing_folders = True
                
                elif writing_folders:   #If we are writing folders, we create the folder on every line
                    datab.create_folder(linea)
                    folders.append(linea) #folders list for error control
                        
                elif "Messages:" in linea: #Case 3: After word Messages: we start the mode writing_emails
                    writing_emails = True
                    current_folder = slice(linea,"left") #We take the name of the folder

                    if current_folder == "OutBox": #This folder has to be in the file!
                        outbox_present = True

                    if current_folder == "Inbox": #This folder has to be in the file!
                        inbox_present = True

                    if folders[0] == current_folder:
                        folders.pop(0) #The folders mails list appear in the order we created them
                    else:
                        raise MailManagerException("EMConfig has some mistakes")

                elif writing_emails: # We first  load the mail with the utils function load_email, then we add it to the current_folder 
                    datab.add_email(load_email(db_config.database_dir,linea),current_folder)
                        
                elif linea == "End": #We check for the 2 important folders
                    if not inbox_present:
                        print("no Inbox folder! Program will stop due to a config mistake")
                        raise MailManagerException()
                    if not outbox_present:
                        print("no OutBox folder! Program will stop due to a config mistake")
                        raise MailManagerException()
                    break
        except:
            raise MailManagerException("EMConfig has some mistakes!")

        if folders == []:  
           return datab

        else: #If some folders have no "folder Messages:" line, we are not good with the EMconfig file.
            raise MailManagerException("EMConfig has some mistakes")

def write_database(db, db_config=None):
    """
    Writes the corresponding Email Config File (text file) from a given Database

    :param db: Database
    :param db_config: Database Configuration
    """

    with open(db.db_config.get_config_path(),"w") as f: # we use f because its short and we are going to use it a lot of times! 
        f.write("Message-ID: "+ str(db.email_id_seed)+"\n") # First the msg_id
        
        f.write("\n") #Jump line
        
        f.write("Folders:"+"\n") 
        for folder in db.folders:
            f.write(db.folders[folder].name+"\n")
        
        f.write("\n")

        for folder in db.folders: 
            f.write(db.folders[folder].name+" Messages:\n")
            current = db.folders[folder].get_head()
            while current != None:
                f.write(current.data.id+"\n") #we  go through the linked list and we call all the .id 
                current = current.next
            f.write("\n")

        f.write("End") #Kewword for the end of the doc



