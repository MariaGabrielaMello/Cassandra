from connect_database import db
from astrapy.collection import Collection
from CRUDusuario import input_with_cancel


def create_produto():
    print("\nInserindo um novo produto")
    nome = input_with_cancel("Nome do produto: ")
    if nome is None: return   

    while True:
        try:
            preco = float(input_with_cancel("Preço: "))
            if preco < 0:
                raise ValueError("Preço não pode ser negativo.")
            break
        except ValueError as e:
            print(f"Erro: {e}. Tente novamente.")
    

    # Inserir produto
    collection: Collection = db.get_collection("produto")
    collection.insert_one(document={"nome": nome,  "preco": preco})
    print("Produto inserido com sucesso.")

def list_produtos_indexados():
    collection: Collection = db.get_collection("produto")
    produtos = list(collection.find())

    if not produtos:
        print("Nenhum produto encontrado.")
        return None

    print("Produtos disponíveis:")
    for i, produto in enumerate(produtos):
        print(f"{i+1}. Nome: {produto['nome']}, Preço: {produto['preco']}")

    while True:
        try:
            index = int(input("Digite o número do produto que deseja: ")) - 1
            if 0 <= index < len(produtos):
                return produtos[index]['nome']  
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def update_produto():
    nome_produto = list_produtos_indexados()  
    if nome_produto is None:
        return  

    # Buscar produto pelo nome
    collection: Collection = db.get_collection("produto")
    existing_produto = collection.find_one({"nome": nome_produto})

    if existing_produto:
        print("Dados atuais do produto:", existing_produto)

        # Obter novos valores para os campos (com opção de manter os atuais)
        nome = input_with_cancel(f"Novo nome (ou pressione Enter para manter '{existing_produto['nome']}' ): ") or existing_produto['nome']
        
        
        while True:
            try:
                preco = float(input_with_cancel(f"Novo preço (ou pressione Enter para manter '{existing_produto['preco']}' ): "))
                if preco is not None and preco < 0:
                    raise ValueError("Preço não pode ser negativo.")
                break
            except ValueError as e:
                print(f"Erro: {e}. Tente novamente.")
        preco = preco if preco is not None else existing_produto['preco']
       

        # Atualizar o produto no banco de dados
        collection.update_one(
            {"nome": nome_produto},  # Filtro para encontrar o produto pelo nome
            {
                "$set": {
                    "nome": nome,                     
                    "preco": preco                    
                }
            }
        )
        print("Produto atualizado com sucesso!")
    else:
        print("Produto não encontrado.")

def read_produto(nome=None):
    collection: Collection = db.get_collection("produto")

    if nome:
        # Buscar produto específico pelo nome
        produto = collection.find_one({"nome": nome})
        if produto:
            print("\nDetalhes do Produto:")
            for chave, valor in produto.items():
                print(f"{chave}: {valor}")
        else:
            print("Produto não encontrado.")
    else:
        # Listar todos os produtos com índice
        produtos = list(collection.find())

        if not produtos:
            print("Nenhum produto encontrado.")
            return

        print("Produtos disponíveis:")
        for i, produto in enumerate(produtos):
            print(f"{i+1}. Nome: {produto['nome']}")

        while True:
            try:
                index = int(input("Digite o número do produto para ver detalhes: ")) - 1
                if 0 <= index < len(produtos):
                    produto_selecionado = produtos[index]
                    print("\nDetalhes do Produto:")
                    for chave, valor in produto_selecionado.items():
                        print(f"{chave}: {valor}")
                    break  # Sair do loop após exibir os detalhes
                else:
                    print("Índice inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

