import matplotlib.pyplot as plt
import networkx as nx

# Classe Node
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

# Classe AVL Tree
class AvlTree:
    def __init__(self):
        self._root = None

    def get_root(self):
        return self._root

    def insert(self, key, value):
        self._root = self._insert(self._root, key, value)

    def _insert(self, node, key, value):
        if not node:
            return Node(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance(node)

        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _height(self, node):
        return node.height if node else 0
    
    def _balance(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0
    
    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._height(z.left),self._height(z.right))
        y.height = 1 + max(self._height(y.left),self._height(y.right))
        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._height(z.left),self._height(z.right))
        y.height = 1 + max(self._height(y.left),self._height(y.right))
        return y
    
    def get(self, key):
        return self._get(self._root, key)
    
    def _get(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._get(node.left, key)
        else:
            return self._get(node.right, key)
        
    def __iter__(self):
        return self._in_order(self._root)
    
    def _in_order(self, node):
        if node:
            yield from self._in_order(node.left)
            yield node.key
            yield from self._in_order(node.right)
    
# Dados dos funcionarios

alunos = [
    (101, "Aline"), (203, "Ana"), (150, "Rueda"), (304, "Romani"),
    (500, "Breno"), (220, "Bruno"), (111, "Caio"), (405, "Carlos"),
    (210, "Daniel"), (340, "Juffo"), (520, "Pontes"), (600, "Eduardo"),
    (315, "Emanuel"), (430, "Erick"), (250, "Erico"), (710, "Estevao"),
    (820, "Felipe"), (910, "Fernando"), (612, "Biancardi"), (711, "Pereira"),
    (215, "Piffer"), (130, "Alcantaro"), (250, "Thomazi"), (713, "Giovanni"),
    (129, "Lopes"), (211, "Miranda"), (622, "Gustavo"), (111, "Igor"),
    (10, "Isabel"), (460, "Costa"), (120, "Louback"), (602, "Machado"),
    (325, "Juliany"), (403, "Kuan"), (217, "Lucas"), (371, "Missagia"),
    (151, "Zortea"), (103, "Borges"), (50, "Moura"), (364, "Eduarda"),
    (505, "Paulo"), (22, "Lyra"), (119, "Barros"), (452, "Ramses"),
]

# Criar e preencher a árvore AVL
tree = AvlTree()
for id_func, nome in alunos:
    tree.insert(id_func, nome)

# ID a ser buscado
id_busca = 710

# Função para desenhar e salvar a árvore
def plot_tree(avl_tree, id_destacado = None, filename = "avl_tree.png"):
    G = nx.DiGraph()
    nomes = {}
    cores = {}

    def add_nodes_edges(node, parent = None):
        if node is None:
            return
        G.add_node(node.key)
        nomes[node.key] = node.value
        if parent:
            G.add_edge(parent.key, node.key)
        add_nodes_edges(node.left, node)
        add_nodes_edges(node.right, node)
    
    root = avl_tree.get_root()
    add_nodes_edges(root)

    # Layout comm bom espaçamento
    pos = nx.spring_layout(G, seed=42, k=1.2)

    # Definir cores: azul claro (default), verde (destacado), vermelho (raiz)
    for node in G.nodes:
        if node == root.key:
            cores[node] = 'red'
        elif node == id_destacado:
            cores[node] = 'darkgreen'
        else:
            cores[node] = 'skyblue'
        
    node_colors = [cores[n] for n in G.nodes]

    plt.figure(figsize=(10,14))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold')

    #Rotulos com os nomes dos funcionarios
    for key, (x,y) in pos.items():
        plt.text(x,y - 0.07, nomes[key], fontsize=9,ha='center',va='top',color='black')

    plt.title("Arvore AVL de alunos\n(ID nos nós / Nome abaixo / Raiz em vermelho / Buscado em verde)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Árvore salva como {filename}")

#Buscar e mostrar funcionário
nome_encontrado = tree.get(id_busca)
if nome_encontrado:
    print(f"\nAlunos com ID {id_busca}: {nome_encontrado}\n")
else:
    print(f"\nAlunos com ID {id_busca} não encontrado.\n")

#Mostrar todos os funcionarios ordenados por ID
print("Alunos ordenados por ID:")
for id_func in tree:
    print(f"ID: {id_func}, Nome: {tree.get(id_func)}")
    
#Salvar a árvore com destaque
plot_tree(tree, id_destacado=id_busca)