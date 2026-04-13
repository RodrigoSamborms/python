class Node:
    def __init__(self,data):
        self.right=self.left=None
        self.data = data
class Solution:
    def insert(self,root,data):
        if root==None:
            return Node(data)
        else:
            if data<=root.data:
                cur=self.insert(root.left,data)
                root.left=cur
            else:
                cur=self.insert(root.right,data)
                root.right=cur
        return root

    def getHeight(self,root):
        #Write your code here
        # Caso base: si el nodo es nulo, la altura es -1 para que la altura de un árbol vacío sea 0
        if root is None:
            return -1
    
        # Recursividad: 1 + max(altura_izq, altura_der)
        height_left = self.getHeight(root.left)
        height_right = self.getHeight(root.right)
        
        return 1 + max(height_left, height_right)   #con el caso base -1 ahora si el resultado es -1 el 
                                                    #arbol tienen altura 0
    def levelOrder(self,root):
        #Write your code here
        if root is None:
            return []

        resultado = []
        cola = [root]
        inicio = 0

        while inicio < len(cola):
            nivel_actual = []
            elementos_en_nivel = len(cola) - inicio

            for _ in range(elementos_en_nivel):
                nodo = cola[inicio]
                inicio += 1
                nivel_actual.append(nodo.data)

                if nodo.left is not None:
                    cola.append(nodo.left)
                if nodo.right is not None:
                    cola.append(nodo.right)

            resultado.append(nivel_actual)

        salida = " ".join(str(valor) for nivel in resultado for valor in nivel)
        print(salida)
        return resultado                                           

T=int(input())
myTree=Solution()
root=None
for i in range(T):
    data=int(input())
    root=myTree.insert(root,data)
#height=myTree.getHeight(root)
#print(height)
myTree.levelOrder(root)
