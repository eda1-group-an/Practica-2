#NIA's: 217447, 217723, 194985. Group Code: AN. Professor: Sergio Ivan Giraldo 

import logging
import os

from .email import Email
from .folder import Folder
from .exceptions import MailManagerException
from .linked_list import LinkedList
#Hola
class DatabaseConfiguration:
    """
    This class allow us to configure all the different parameters of the database such as its location.
    """

    def __init__(self, database_dir, config_filename="EMConfig.txt", email_dir=None, email_extension=".txt"):
        """
        Initializes the database configuration with the database directory, where the configuration file is located.
        Also it allows to configure a different email directory and email extension.

        :param database_dir: Path of the base directory.
        :param config_filename: Name of the configuration file, defaults to 'EMConfig.txt'.
        :param email_dir: Path of the email directory, defaults to the base directory (database_dir).
        :param email_extension: Extension fo the email files, defaults to '.txt'.
        """

        self.database_dir = database_dir
        self.config_filename = config_filename
        #Hola
        if email_dir:
            self.email_dir = email_dir
        else:
            self.email_dir = database_dir

        self.email_extension = email_extension

    def get_config_path(self):
        """
        Returns the path where the configuration file of the database is located

        :return The config file path
        """
        return os.path.join(self.database_dir, self.config_filename)

    def get_email_path(self, email_id):
        """
        Given an email id it returns its location

        :param email_id:
        :return The email path
        """
        filename = email_id + self.email_extension
        return os.path.join(self.email_dir, filename)


class Database:
    """
    This class is the one in charge of managing the different operations of the database like
    adding and removing emails and folders
    """

    #Control de parámetros:
        #Parametro seed: Vamos controlando el seed con el que se generan los id de los correos

    #Funcionalidades: 
        #añadir un email a un folder
        #añadir un email a la database virtual (self.emails)
        #eliminar un mail de una carpeta
        #eliminar un email de la database virtual (self.emails)
        #mirar si existe un mail en la database en función del id
        #dar todos los ids de una carpeta
        #dar todos los ids de la database virtual (self.emails)
        #Crear un nuevo folder
        #Eliminar un folder
        #Buscar texto (queda por hacer)
        #Conseguir una lista con todos los nombres de las carpetas
        #Saber si una folder existe o no
        #Asignar un seed a un correo
        #Funciones de la clase DatabaseConfig, ya que la incluimos

    def __init__(self, db_config, seed):
        """
        Initializes the database class with a given seed and the database configuration instance that contains
        the path where the emails (and the config file) are stored

        :param seed: Seed used for email id generation.
        """

        self.db_config = db_config
        self.email_id_seed = seed
        self.folders = {}
        self.emails = LinkedList()

    def add_email(self, email, folder_name=None):
        """
        Add the given email to the database and to the specified folder. If the folder is not found in the Database
        it should raise a MailManagerException. If no folder is provided, the email will be
        added to the outbox folder by default.

        :param email: Email to be added.
        :param folder_name: Name of the older to which the email is added. If not provided, defaults to outbox folder.
        :return: The email id
        """

        #Control de entrada:
            #Esta función no controla el id del mail, la forma del mail ni la forma del folder_name 
            # -> El id y el folder_name lo controla el main, y el email lo controla tanto create email como load email

        #Control de errores: 
            #Esta función controla si el mail existe o no
            #Esta función controla si la carpeta existe o no
            #Esta función controla si el mail está en el folder o no
            #Esta función no controla las referencias de los mails

        # First of all, we add it on self.emails if he's not already there
        if email.id not in self.get_email_ids():
            self.emails.append(email) #We only add it on self.emails if he's not already there

        # Second of all, we check the folder where the mail is going
        if not folder_name:
            folder_name = "OutBox" #If no folder is provided it adds the mail to the outbox folder.

        if folder_name not in self.folders.keys(): 
            raise MailManagerException("There's no such Folder")

        # Finally, we add it to the Folder only if it's not there already
        if email.id not in self.get_email_ids(folder_name):
            self.folders[folder_name].new_email(self.get_email(email.id)) #Method for adding the mail to the folder
        else:
            raise MailManagerException("The mail is already on that Folder!")

        return email.id

    def remove_email(self, email, folder_name=None):
        """
        Remove given email from the given folder. If the folder is not found in the Database
        it should raise a MailManagerException. If no folder_name is provided, the email is removed completely
        from the database.

        :param email: The email to be removed.
        :param folder_name: The name of the folder from which the email should be removed. If no folder name is
        provided, the email is removed from all the folders and from the database.
        :return: The number of folder referencing this email. ??
        """

        #Control de entrada:
            #Esta función no controla el id del mail, la forma del mail ni la forma del folder_name 
            # -> El id y el folder_name lo controla el main, y el email lo controla tanto create email como load email

        #Control de errores: 
            #Esta función si controla si el mail existe o no
            #Esta función si controla si la carpeta existe o no 
            #Esta función no controla las referencias de los mails
        
        #First we check if the folder exists. If it does not, an error will rise 
        if folder_name:
            if folder_name in self.folders.keys(): 
                self.folders[folder_name].unlink_email(email)
            else:
                raise MailManagerException("There's no such Folder")

        elif not folder_name:
            for folder in self.folders.keys():
                if email.id in self.get_email_ids(folder):
                    self.folders[folder].unlink_email(email) 
            self.emails.remove(email) #It will remove it from the main db linked list 
            
        return email.references 

    def get_email(self, email_id):
        """
        Looks for the given email in the database and returns it

        :param email_id: The id of the mail we are looking for
        :return: If email id is found in the database it returns it. If it is not found it returns None.
        """
        #Control de entrada:
            # Esta función no controla si el id del mail existe

        #Control de errores: 
            # Se supone que la linked list acaba en None!

        current = self.emails.get_head()

        while current != None:
            if current.data.id == email_id:
                return current.data
            current = current.next

        return None

    def get_email_ids(self, folder_name=None):
        """
        Get email ids from a given folder. If the folder is not found in the Database
        it should raise a MailManagerException.

        :param folder_name:
        :return: Returns the list of email ids of a given folder. If the folder_name parameter is not passed
         it returns the list of emails of the database.
        """
        #Control de entrada:
            #El folder name lo controla el main

        #Control de errores: 
            #Esta función si controla si el folder existe
            #Esta función no controla si la folder está vacía o no. Si está vacia devuelve una lista vacia
            #Esta función no controla si un mail está repetido en un folder

        email_ids = []

        if folder_name:
            if folder_name in self.folders.keys():
                current = self.folders[folder_name].get_head()
            else:
                raise MailManagerException("There's no such Folder")

        else:
            current = self.emails.get_head()
            
        while current != None:
            email_ids.append(current.data.id)
            current = current.next

        return email_ids

    def create_folder(self, folder_name):
        """
        Adds a folder to the database

        :param folder_name: the name of the new folder
        """
        #Control de entrada:
            #El folder name lo controla el main

        #Control de errores: 
            #Esta función no controla si el folder existe, lo controla check_folder()

        if folder_name in self.folders.keys():
            raise MailManagerException("There's a Folder with that name already!")
        else:
            self.folders[folder_name] = Folder(folder_name)
            
    def remove_folder(self, folder_name): 
        """
        Remove given folder from database. If the folder is not found in the Database
        it should raise a MailManagerException. If some of the emails that belong to that folder doesn't belong
        to any more folders, those emails are removed from the database.

        :param folder_name: the name of the folder to be removed
        """
        #Control de entrada:
            #El folder name lo controla el main

        #Control de errores: 
            #Esta función no controla si el folder existe, lo controla check_folder()

        if folder_name in self.folders.keys():
            current = self.folders[folder_name].get_head()
            while current != None:
                self.folders[folder_name].unlink_email(current.data)
                if current.data.references == 0:
                    self.emails.remove(current.data) #It will remove it from the main linked list 
                current = current.next
            self.folders.pop(folder_name)

        else:
            raise MailManagerException("There's no such folder")

    def search(self, text):
        """
        Searches the text into the titles and bodies of the emails, returning the emails that contains said text.

        :param text: the text to be searched
        :return: the list of emails containing that text.
        """
        #Control de entrada:
            #text puede ser cualquier string menos una posición en blanco

        #Control de errores: 
            #Esta función no controla si hay coincidencias o no. 

        matches = []

        for ide in self.get_email_ids():
            email = self.get_email(ide)
            if text in email.sender or text in email.receiver or text in email.subject or text in email.date or text in email.body:
                matches.append(email)

        return matches
        
    def assign_seed(self):
        """
        It assigns a seed to a mail we create in the main

        :return: the new seed for the mail
        """
        self.email_id_seed += 1 #We sum one to the atribute
        return self.email_id_seed
