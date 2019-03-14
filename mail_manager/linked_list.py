from .exceptions import MailManagerException

class Node:
    """
    The nodes are the separated objects that will conform the Linked List.
    """

    def __init__(self, data=None):
        """
        Initializes a node instance that will contain some data.
        :param data: content of the node. This could be any object, for example, an email.
        """

        self.data = data
        self.next = None

class LinkedList:
    #Queda por hacer: 
        #Funcion que busque texto en la linked list
        #Str por implementar

    #Control de parámetros:
        # Controla el .next de los nodos
        # Controla el tamaño de la linked list
        # Controla el head de la linked list
        # No debe entrar dentro de los .data de los elementos!

    #Funcionalidades: 
        # Puede saber si una linked list está vacía o no
        # Puede saber el tamaño de la linked list
        # Puede saber cual es el primer elemento de la linked list
        # Puede insertar elementos al final de la linked list
        # Puede eliminar un elemento de la linked list si le entra el elemento
        # Puede reiniciar la linked list
        # Puede encontrar texto en la lnked list
        # Puede imprimir una representación de la linked list
    """
    This class implements a linked list.

    A linked list is a linear data structure where each element is a separate object.
    Linked list elements are not stored at contiguous location; the elements are linked using pointers.
    In this case each separated object belongs to the class Node.
    """

    def __init__(self):
        """
        Initializes the linked list. Take into account that you'll need to keep track of the first and/or
        the last element. Maybe is advisable also to have an updated size attribute.
        """

        self.head = None
        self.size = 0
    
    def is_empty(self):
        """
        Checks if the list is empry or not.
        
        :return: True if empty, False otherwise
        """
        if self.__len__() == 0:
            return True
        else:
            return False

    def get_head(self):
        """
        Returns the head of the linked list. 

        :return: The head. None if the list is empty
        """
        return self.head

    def append(self, item):
        """
        Add an item to the end of the list.

        :param item: The mail that will be added.
        :return: Nothing
        """
        #Control de entrada:
            # Esta función recibe un EMAIl y lo convierte en nodo

        #Control de errores: 
            # Esta función controla el aumento del size al añadir un elemento
            # Esta función no valora si el email tiene formato correcto o no, solo si es de la classe Email

        item = Node(item) #First we create a node with the item

        if self.is_empty(): #If the list is empty, we just change the head of the ll
            self.head = item

        else: #If not, we get through the list until the last node and then we change its .next
            current = self.get_head()
            while current.next: 
                current = current.next

            current.next = item

        self.size += 1

    def insert(self, index, item):
        """
        Insert an item at a given position.

        The first argument is the index of the element before which to insert, so a.insert(0, item) inserts
        at the front of the list and a.insert(len(a), item) is equivalent to a.append(item).

        :param index: index where the item should be stored.
        :param item: object to be stored into the linked list.
        :return: nothing
        """
        #Not implemented. We do not use it!

    def remove(self, item):
        """
        Remove from the list the first occurrence of item.
        Raises ValueError if there is no such item.

        :param item: object(node) to be removed from the linked list.
        """
        #Control de entrada:
            # Esta función recibe un EMAIL QUE YA ESTÉ EN LA LINKED LIST

        #Control de errores: 
            # Esta función controla la reducción del size al añadir un elemento
            # Esta función no valora si el nodo tiene formato correcto o no, solo si es de la classe Node
            # Esta función compara el mismo Email. Eso quiere decir que no podemos crear un nuevo Email y tratar de compararlo
            # aun cuando tengas los mismos atributos porque nunca encontrará coincidencia.  
        
        current = self.get_head()

        if current.data == item:
            self.head = current.next
            self.size -= 1

        else:        
            while current:
                if current.next:
                    if current.next.data == item:
                        current.next = current.next.next
                        self.size -= 1
                        break
                current = current.next

        if self.size == 0:
            self.clear()

        if not current:            
            raise ValueError("Email not found...")
    
    def pop(self, index=-1):
        """
        Remove the item at the given position in the list, and return it.
        If no index is specified, a.pop() removes and returns the last item in the list.

        Raises IndexError if list is empty or index is out of range.

        :param index: index where the item should be popped (removed and returned).
        """
        # We do not use it!

    def clear(self):
        """
        Remove all items from the list.
        """
        self.__init__()

    def index(self, item, start=0, end=None):

        """
        Return first index of value.

        Raises a ValueError if there is no such item.

        :param item: el objecto que buscamos
        :param start: position from which the search is going to start.
        :param end: position at which the search is going to end.

        De momento no sabemos que hace
        """

        #Not implemented

    def __len__(self):
        """
        Returns the actual size, it is, the number of elements stored in the linked list.

        :return: the number of elements currently stored in the linked list.
        """
        return self.size

    def __str__(self):
        """
        Returns a string representation of the linked list.
        """
        msg = ""
        current = self.get_head() 
        while (current):
            msg += str(current.data.id)
            msg+="\n"
            current = current.next
        
        return msg
        #Not implemented yet
