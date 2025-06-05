#Codigo de Criação de Arvore Binaria e Travessias Pre_order, in_order, post_order
class Node:
    def __init__(self,data):
        self.data = data
        self.right_child = None
        self.left_child = None

n1 = Node("Root node")
n2 = Node("Left child node")
n3 = Node("Right child node")
n4 = Node("Left grandchild node")

n1.left_child = n2
n1.right_child = n3
n2.left_child = n4

# current = n1

#while current: #busca recursiva a direita
#    print(current.data)
#    current = current.right_child

def inorder(root_node):
    current = root_node
    if current is None:
        return
    
    inorder(current.left_child)
    print(current.data)
    inorder(current.right_child)

#inorder(n1)

def preorder(root_node):
    current = root_node
    if current is None:
        return
    
    print(current.data)
    preorder(current.left_child)
    preorder(current.right_child)

#preorder(n1)

def postorder( root_node):
    current = root_node
    if current is None:
        return

    postorder(current.left_child)
    postorder(current.right_child)
    print(current.data)

#postorder(n1)

