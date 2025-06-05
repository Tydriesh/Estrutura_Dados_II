import unittest
from avltree import AvlTree

class TestAvlTree(unittest.TestCase):
    def setUp(self):
        self.tree = AvlTree[int, str]()
        print('\n[SETUP] Nova arvore AVL inicializada.')

    def test_insert_and_search(self):
        print("[TEST] Inserindo elementos na arvore.")
        self.tree[10] = "dez"
        self.tree[20] = "vinte"
        self.tree[5] = "cinco"
        
        print('[VERIFICACAO] Checando se os elementos estão na arvore.')
        self.assertEqual(self.tree[10], 'dez')
        self.assertEqual(self.tree[20], 'vinte')
        self.assertEqual(self.tree[5], 'cinco')

        print('[VERIFICACAO] Checando se um elemento não inserido está ausente')
        self.assertNotIn(15, self.tree)

    def test_delete(self):
        ('[TEST] Inserindo elementos para remocao.')
        self.tree[20] = "vinte"
        self.tree[30] = "trinta"
        self.tree[40] = "quarenta"

        print("[ACAO] Removendo 30.")
        del self.tree[30]

        print("[VERIFICACAO] Verificando se a chave 30 foi removida.")
        self.assertNotIn(30, self.tree)

        print("[VERIFICACAO] Verificando se a chave 30 foi removida.")
        self.assertIn(20, self.tree)
        self.assertIn(40, self.tree)
    
    def test_inorder_traversal(self):
        print("[TEST] Inserindo elementos para travessia em ordem.")
        elements = [50, 30, 70, 20, 40, 60, 80]
        for i in elements:
            self.tree[i] = str(i)
            print(f"[INSERTION] {i} -> '{str(i)}'")

        print("[ACTION] Realizando travessia in-order.")
        inorder = list(self.tree)

        print("[RESULT] Ordem obtida: {inorder}")

        self.assertEqual(inorder, sorted(elements))
        print("[SUCCESS] Ordem está correta.")

    def test_update_value(self):
        print("[TEST] Testando atualização de valor em uma chave")
        self.tree[100] = 'cem'
        print(f"[INSERTION] 100 -> 'cem'")
        self.assertEqual(self.tree[100], 'cem')

        print("[ACTION] Atualizando o valor")
        self.tree[100] = '100'
        self.assertEqual(self.tree[100], '100')
        print("[VERIFICATION] Valor atualizado com sucesso.")

    def test_empty_tree(self):
        print("[TEST] Verificando arvore vazia")
        self.assertEqual(list(self.tree), [])
        self.assertNotIn(1, self.tree)
        print("[SUCCESS] A arvore está vazia, conforme esperado.")


if __name__ == '__main__':
    unittest.main()
