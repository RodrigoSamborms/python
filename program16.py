class Node:
    def __init__(self,data):
        self.data = data
        self.next = None 
class Solution: 
    def display(self,head):
        current = head
        while current:
            print(current.data,end=' ')
            current = current.next
    
    def insert(self,head,data): 
        #Complete this method
        #Debemos inciar head si lista es vacia y vamos a insertar por la tail
        if head is None: #verificamos si la head es None, lo que indica lista vacia
            head = Node(data) #inciamos la head de la lista
            head.next = None #ahora head apunta a None, indicando que es el ultimo nodo en la lista
        else: #Head no es None, la lista no esta vacia, debemos recorrer la lista hasta el final para insertar
            current = head #iniciamos un nodo temporal para recorrer la lista
            while current.next: #recorremos la lista hasta el final
                current = current.next
            new_node = Node(data) #creamos un nuevo nodo con el dato a insertar
            current.next = new_node #el ultimo nodo actual apunta al nuevo nodo
            new_node.next = None #el nuevo nodo apunta a None, indicando que es el nuevo ultimo nodo
        return head #devolvemos la nueva head de la lista
    '''
    def insert(self,head,data): 
        #Complete this method
        #Como este metodo tiene el parametro head, vamos a insertar por la head
        if head is None: #verificamos si la head es None, lo que indica lista vacia
            head = Node(data) #inciamos la head de la lista
            head.next = None #ahora head apunta a None, indicando que es el ultimo nodo en la lista
        else: #Head no es None, la lista no esta vacia
            new_node = Node(data) #creamos un nuevo nodo con el dato a insertar
            new_node.next = head #el nuevo nodo apunta al nodo head actual
            head = new_node #el nuevo nodo se convierte en la nueva head
            #note que el nodo anterior sigue apuntando a None, el final de la lista
        return head #devolvemos la nueva head de la lista
    '''
    #NOTE ==> insertar al inicio es mas facil qu einsertar al final. en una lista enlazada simple
mylist= Solution()
T=int(input())
head=None
for i in range(T):
    data=int(input())
    head=mylist.insert(head,data)    
mylist.display(head); 	  