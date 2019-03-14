#NIA's: 217447, 217723, 194985. Group Code: AN. Professor: Sergio Ivan Giraldo 

import logging
import datetime

from mail_manager import utils
from mail_manager.database import Database, DatabaseConfiguration
from mail_manager.email import Email
from mail_manager.exceptions import MailManagerException


def read_int_option(message, start, end):
    """
    
    Shows an input message and reads the option of the user

    :param message: input message
    :param start: minimum value the user can entero
    :param end: maximum value the user can enter
    :return: the option chosen by the user
    """

    option = input(message)
    try:
        option = int(option)

    except ValueError:
        option = None

    else:
        if option < start or option > end:
            option = None

    return option

def choose_email(email_ids):
    """
    Shows the emails contained in the database and asks the user to choose one

    :param email_ids: list of email ids
    :return: the email id chosen by the user
    """

    email_id = None
    if not email_ids:
        print("There are no emails in the database yet.")

    else:
        print("The database contains the following emails:")
        for idx, email_id in enumerate(email_ids):
            print("  {}. {}".format(idx + 1, email_id))

        email_id = None
        cancel = False
        while not cancel and not email_id:
            option = read_int_option("Choose an email: (0 to cancel)\n", 0, len(email_ids))
            if option:
                email_id = email_ids[option - 1]

            elif option == 0:
                cancel = True
                print("Operation cancelled!")

            else:
                print("Invalid option, try again.")

    return email_id

def choose_folder(folder_names):
    """
    Shows the folders contained in the database and asks the user to choose one

    :param folder_names: list of folder
    :return: the name of the folder chosen by the user
    """

    folder_name = None
    if not folder_names:
        print("There are no folders in the database yet.")

    else:
        print("The database contains the following folders:")
        for idx, name in enumerate(folder_names):
            print("  {}. {}".format(idx + 1, name))

        cancel = False
        while not cancel and not folder_name:
            option = read_int_option("Choose a folder: (0 to cancel)\n", 0, len(folder_names))
            if option:
                folder_name = folder_names[option - 1]

            elif option == 0:
                cancel = True
                print("Operation cancelled!")

            else:
                print("Invalid option, try again.")

    return folder_name

def list_emails(db):
    """
    Shows the list of emails contained in the Database

    :param db: An email database
    """
    print("\n********** Emails list **********")
    lista(db) #We created another function to be able to display also the folders with the same code

def lista (db,folder_name = None):
    """
    Show the list of email contained either in the Database or in a folder.

    :param db: An email database
    :param folder_name:  The folder where it looks. If its None, then it shows the list of the mails in the entire database
    """
    contador = 1 #For the numbering at the start of each string
    max_size = 35 # For addind "..." when the subject is too large
    reduced_size = 32 #The new size for the subject if its too large. 25 minus 3 points("...") = 22 
    pad = 50 # For a better visualization of the list
    secondpad = pad*2 # The second padding is at the double of distance than the first
    space = " " #For adding spaces when padding

    if db.get_email_ids(folder_name) != []: 
        for email_id in db.get_email_ids(folder_name):
            string = "" #The line we are going to pring
            to_print = db.get_email(email_id) #We will use some email properties that will be displayed at the list

            if len(to_print.subject) > max_size: #We control the size to a max of chars
                new_subject = to_print.subject[:reduced_size] + "..."
            else:
                new_subject = to_print.subject
            
            if len(to_print.sender) > max_size: #We control the size of a sender to a max of chars
                new_sender =to_print.sender[:reduced_size] + "..."
            else:
                new_sender = to_print.sender
            
            string += ("%s. Sender: %s." % (contador,new_sender))
            string += (pad - len(string)) * space
            string += ("Subject: %s." % (new_subject))
            string += (secondpad - len(string)) * space
            string +=  ("Date: %s." % (to_print.date))
            print(string)

            contador += 1 #To the next item!

    else: # We do not display empty lists
        print("No items in this list yet!")

def show_email(db):
    """
    This function calls to the choose_email function and it shows the content of the given email chosen
    by the user in the Database

    :param db: An email database.
    """
    print("") #Aesthetic function
    to_print = db.get_email(choose_email(db.get_email_ids()))
    print("") #Aesthetic function
    if to_print: # Choose email returns False when we cancel
        print (to_print)

def restricted(sample):
    """
    This function takes care of not using restricted words in the fields where they are prohibited

    :param sample: The text that will be checked for forbidden words
    """

    checked = False
    restrict = ["Message-ID:","From:","To:","Subject:","Date:","Folders:","Messages:","End",""] #Array of forbidden words
 
    while not checked:
        if sample not in restrict:
            checked = True
            break

        elif sample == "":
            print("Enter something!")

        else:
            for i in range(len(restrict)):
                if restrict[i] in sample:
                    print ("You can not use the word %s in this field!" %restrict[i])
                    break
                    
        sample = input("Pleas try again: ")    

    return sample
	
def create_email(db):
    """
    Asks for the user to fill the fields of an email and creates it in the database. It also creates
    its corresponding text file

    :param db: An email database.
    """
    print("\nPlease enter the following fields: ")
    email_id = "message"+ str(db.assign_seed())
    sender = restricted(input("Sender: "))  
    receiver = restricted(input("Receiver: "))
    subject = restricted(input("Subject: "))
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Formula for using the real time on the new email. 

    print("Body of the message. Keep writing after pressing enter until you write the word end at the end of a line or on a new line (and press intro!)") 
    stri = "" #For checking
    body = "" #We add from stri to bodt after checked
    end_chars = 3 #Number of the chars of the word "end"
    
    # This one is tricky. We check at every input if it contains the secuence "end" at the end. We keep adding lines of body until we found it, 
    # and in that moment we add all the line but the word and we finish the loop. 
    while stri[(len(stri)-end_chars):] != "end": #This formula only looks for the word end at the end of the line
        stri = input("")
        if stri[(len(stri)-end_chars):] != "end":
            stri += ("\n")
            body += stri

        else:
            body += stri[:(len(stri)-end_chars)]
            
    #Finaly we add it all to an Email object
    new = Email(email_id, sender, receiver, subject, date, body)

    #Finaly, we add the new mail to the database
    db.add_email(new)

    #And we create it physically on the system with the utils function
    utils.write_email(new,db)

    print("Email created!")

def delete_email(db):
    """
    This functions calls to the choose_email function and it removes the given email chosen
    by the user

    :param db: An email database.
    """
    print("") #Aesthetical reasons

    to_delete = db.get_email(choose_email(db.get_email_ids()))

    if to_delete: #Get email returns None if no email id is provided

        print(to_delete) # Calls the str on Email class

        if delete(read_int_option("Is this the mail you want to delete? \n 1 -> Si. \n 2 -> No. \n Opción: ",1,2)): # Double checking

            #We remove it from the database
            db.remove_email(to_delete)

            #We delete it physically
            utils.delete_email(to_delete,db)

            print("Email deleted succesfully")

def show_folders(db):
    """
    This function calls to the choose_folder function and shows all the emails contained in the folder chosen
    by the user.

    :param db: An email database.
    """

    folder_name = choose_folder(list(db.folders.keys()))
    
    if folder_name:

        print("\n********** %s emails **********" %folder_name)
        lista(db,folder_name)

def create_folder(db):
    """
    Asks the user to introduce the folder name and then it creates it in the Database

    :param db: An email database.
    """

    #We do not demmand confirmation for this process. The user can always delet it afterwards
    print("")  #Aesthetical
    print("Please enter the name of the new folder.")
    db.create_folder(restricted(input("Name: ")))
    print("\nFolder created!") #For confirmation

def delete (cancelled):
    """
    Function for checking if the users is sure about deleting something or not

    :param cancelled: The first answer to the question is made in the function of origin. 
    return: True if he wants to delete it, False if not
    """
    while not cancelled:
        print("Invalid option. Please try again!")
        cancelled = read_int_option("Is this the item you wanna delete? \n 1 -> Si. \n 2 -> No \n Opción: ",1,2)
        if cancelled:
            break
        
    if cancelled == 1:
        return True

    elif cancelled == 2:
        print("")
        print("Returning to the main menu...")
        return False

def delete_folder(db):
    """
    This functions calls to the choose_folder function and deletes the chosen folder by the user

    :param db: An email database.
    """
    
    folder_to_delete = choose_folder(list(db.folders.keys())) #This to_delete is a FOLDER! not an email as before
    if folder_to_delete and folder_to_delete != "Inbox" and folder_to_delete != "OutBox": #Care with deleting key folders
        if db.folders[folder_to_delete].get_head() != None: 
            print("")
            print("These are the mails in the folder:")
            lista(db,folder_to_delete)
        else:
            print("")
            print("There are no emails in this folder")

        if delete(read_int_option("Is this the folder you wanna delete? \n 1 -> Si. \n 2 -> No. \n Opción: ",1,2)): #always check with the user for confirmation 
            potential_outcasts = db.get_email_ids(folder_to_delete) #All the references of the mails of the folder will be checked
            for ide in potential_outcasts:
                email = db.get_email(ide)
                if email.references == 1: #If you references atribute is 1 (gonna be 0 when the folder is gone) it's game over for you
                    utils.delete_email(email,db) #we remove it physically from the system
            db.remove_folder(folder_to_delete) #we call the database function

            print("Folder deleted succesfully")

    elif folder_to_delete == "Inbox" or folder_to_delete == "OutBox": 
        print("You can not eliminate that folder!") 
    

def add_email_to_folder(db):
    """
    This functions first calls to the choose_email function. After that, it calls to the choose_folder function and
    adds the chosen email to the chosen folder.

    :param db: An email database.ººº
    """
    
    print("Which email do you want to add to a folder?")
    email = db.get_email(choose_email(db.get_email_ids()))
    #First we take the email 

    if email: 
        try: #This try controls wether the folder contains the mail already or not. The error will be raised by the add_email function
            print("In which folder do you want to add it?")
            folder = choose_folder(list(db.folders.keys()))

            if folder:
                db.add_email(email,folder)
            
                print("")
                print("Email added succesfully!")

        except:
            print("")
            print("Mail on that folder already!")


def remove_email_from_folder(db):
    """
    This function first calls to the choose_folder function. After that, it shows all the emails belonging to that
    folder and asks the user to chose which one wants to remove. Then, the chosen mail is removed

    :param db: An email database.
    """

    print("From which folder do you want to remove a mail?")
    folder = choose_folder(list(db.folders.keys()))
    #First we take the folder 

    if folder:
        print("Which email are you willing to remove form the folder?")
        email = db.get_email(choose_email(db.get_email_ids(folder)))
        #Then we take the email from the folder
        if email:
            if db.remove_email(email,folder) == 0: #remove_email return the number of references. If it's the last reference, we delete it from the system
                db.remove_email(email) 
                utils.delete_email(email,db)
            print("")
            print("Email removed succesfully!")

def search(db):
    """
    Ask the user for the text to be searched and searches the text into the database, showing the emails
    that contains said text.

    :param db: An email database.
    """

    search = input("Enter the string of text you want to look for in the database (0 to cancel): ") # You cann add any string you want but an empty space
    while search == "":
        search = input("Please enter something (0 to cancel): ")

    if search != "0":
        if db.search(search) != []: #db search returns us a list of mails with the matches
            for mail in db.search(search):
                print(mail)
                print("")
                print("")
            print("These are all the mails containing the string %s. " %(search))

        else:
            print("There are no mails containging the string %s. " %(search))

def show_menu(db):
    """
    Shows all the different menu options. This function also calls to the read_int_option function and calls to
    the chosen option

    :param db: An email database.
    """
    options = [
        {"message": "Exit", "function": None},
        {"message": "List emails", "function": list_emails},
        {"message": "Show email", "function": show_email},
        {"message": "Create email", "function": create_email},
        {"message": "Delete email", "function": delete_email},
        {"message": "Show folders and folder emails", "function": show_folders},
        {"message": "Create folder", "function": create_folder},
        {"message": "Delete folder", "function": delete_folder},
        {"message": "Add email to folder", "function": add_email_to_folder},
        {"message": "Remove email from folder", "function": remove_email_from_folder},
        {"message": "Search", "function": search},
    ]

    exit_program = False
    while not exit_program:

        print("\nMain menu:")
        for idx, option in enumerate(options[1:]):
            print("  {}.- {}".format(idx+1, option["message"]))

        print("  {}.- {}".format(0, options[0]["message"]))

        option = read_int_option("What do you want to do? Choose an option:\n", 0, len(options))
        if option is None:
            print("Invalid option, try again.")

        elif option == 0:
            exit_program = True

        else:
            option_function = options[option]["function"]
            try:
                option_function(db)

            except MailManagerException as mme:
                print("Error: {}", mme)

            except Exception as e:
                print("Unexpected error: {}", e)
                raise

            input("\nPress Enter to continue...")

def main():
    """
    MAIN function of the email manager.
    """

    # We create a Database Configuration object with the name of the folder where our emails and configuration files are
    # going to be stored. In our case all of them are placed inside "emailDB".
    db_config = DatabaseConfiguration("emailDB")

    # This function reads the EMConfig file and returns a Database object with all the information about
    # the state of the email manager.
    db = utils.load_database(db_config)

    # Calls the menu
    show_menu(db)
    # When the user decides to exit the program it has to save all the information related to the changes done in the
    # email manager. So it writes a new EMConfig file with the new state of folders, emails and Message-Id.
    utils.write_database(db)


if __name__ == '__main__':
    main()
