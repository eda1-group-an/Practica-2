from .exceptions import MailManagerException
from .email import Email
from .linked_list import LinkedList


class Folder:
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

    def add_email(self,email):
        """
        Adds an email to the folder
        """
        self.emails.append(email)
    
    def remove_email(self,email):
        """
        Removes a mail from the Folder
        """
        self.emails.remove(email)
    
    def get_emails(self):
        """
        Gets a list with all the mails in a linked list

        return: A list with all the mails in the linked list
        """
        mails_list = []
        current = self.emails.head
        while current != None:
            mails_list.append(current.data)
        return mails_list
        
