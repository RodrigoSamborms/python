class Node:
    def __init__(self,data):
        self.data = data
        self.next = None 
class Solution: 
    def insert(self,head,data):
            p = Node(data)           
            if head==None:
                head=p
            elif head.next==None:
                head.next=p
            else:
                start=head
                while(start.next!=None):
                    start=start.next
                start.next=p
            return head  
    def display(self,head):
        current = head
        while current:
            print(current.data,end=' ')
            current = current.next

    def removeDuplicates(self,head):
        #Write your code here
        """
        Elimina datos duplicados de la lista.
        Utiliza un set para rastrear nodos visitados.
        Ya que la propiedad del tipo Set en python evita duplicados
        """
        if not head:
            return head #indica que la lista esta vacia

        nodos_vistos = set() #registramos los datos para verificar si estan duplicados
        actual = head #inicializamos la configuracion para recorrer la lista simplemente enlazada
        nodos_vistos.add(actual.data) #Guardamos el primer dato en la varible conjunto
        
        # Recorremos la lista
        while actual.next: #mientras no lleguemos al nodo null
            if actual.next.data in nodos_vistos: #vemos el valor del nod siguiente para verificar si es repetido
                # Si el dato ya fue visto, saltarse el nodo (eliminar)
                actual.next = actual.next.next #eliminamos
            else:
                # Si es nuevo, anadir al set y mover el puntero
                nodos_vistos.add(actual.next.data)
                actual = actual.next

        return head

mylist= Solution()
T=int(input())
head=None
for i in range(T):
    data=int(input())
    head=mylist.insert(head,data)    
head=mylist.removeDuplicates(head)
mylist.display(head); 