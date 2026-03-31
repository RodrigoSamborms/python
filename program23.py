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
myTree.levelOrder(root)
