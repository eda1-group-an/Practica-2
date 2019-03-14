#NIA's: 217447, 217723, 194985. Group Code: AN. Professor: Sergio Ivan Giraldo 

from .exceptions import MailManagerException
from .email import Email
from .linked_list import LinkedList


class Folder:
    # This class does not do much. It controls the mails inside each Folder, the name of the folder and 
    # the references of the mails inside

    """
    The folder class contains the name of the class and the list of emails.
    Add as many methods as you consider.
    """

    def __init__(self, name):
        """
        Initializes a folder assigning it a name.

        :param name: Name of the folder
        """
        self.name = name
        self.emails = LinkedList()

    def new_email(self,email):
        """
        Adds an email to the folder
        """
        self.emails.append(email)
        email.references += 1 #We add one on the references
    
    def unlink_email(self,email):
        """
        Removes a mail from the Folder
        """
        self.emails.remove(email)
        email.references -= 1

    def get_head(self):
        """
        """
        return self.emails.get_head()
    
   
        
