from connect_database import db
from astrapy.collection import Collection
from CRUDusuario import create_usuario
from CRUDproduto import list_produtos_indexados

def cadastrar_endereco(cpf_usuario):
    print("Cadastro de novo endereço.")
    rua = input("Rua: ")
    num = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP: ")

    novo_endereco = {
        "rua": rua,
        "num": num,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "cep": cep
    }

   
    collection: Collection = db.get_collection("usuario")
    collection.update_one(
        {"cpf": cpf_usuario}, 
        {
            "$set": {"end": []},  # Cria o array 'end' se não existir
            "$push": {"end": novo_endereco}  # Adiciona o novo endereço
        }
    )

    print("Endereço cadastrado com sucesso.")
    return novo_endereco

def realizar_compra(cpf_usuario):
    print("Realizando compra:")
    usuario_collection: Collection = db.get_collection("usuario")
    produto_collection: Collection = db.get_collection("produto")
    compra_collection: Collection = db.get_collection("compra")

    usuario = usuario_collection.find_one({"cpf": cpf_usuario})
    if not usuario:
        print("Usuário não encontrado. Deseja realizar o cadastro? (S/N)")
        resposta = input().upper()
        if resposta == 'S':
            cpf_usuario = create_usuario()
            usuario = usuario_collection.find_one({"cpf": cpf_usuario})
            if not usuario:
                print("Erro: Usuário não encontrado após o cadastro.")
                return
        else:
            print("Não é possível continuar com a compra sem um usuário cadastrado.")
            return

    carrinho = []
    produtos = list(db.get_collection("produto").find())  # Obter a lista de produtos apenas uma vez

    if not produtos:
        print("Nenhum produto encontrado.")
        return

    print("Lista de produtos disponíveis:")
    for i, produto in enumerate(produtos, start=1):
        print(f"{i}. Nome: {produto['nome']}, Preço: {produto['preco']}")

    while True:
        id_produto = input("\nDigite o número do produto que deseja adicionar ao carrinho (ou 'C' para concluir): ")
        if id_produto.upper() == 'C':
            break

        try:
            id_produto = int(id_produto)
            if 1 <= id_produto <= len(produtos):
                produto = produtos[id_produto - 1]
                carrinho.append(produto)
                print(f"Produto '{produto['nome']}' adicionado ao carrinho.")
            else:
                raise ValueError
        except ValueError:
            print("Erro: Produto inválido. Digite um número válido.")

    total = sum(float(produto["preco"]) for produto in carrinho)
    print(f"\nValor total do carrinho: R${total:.2f}")

    confirmar = input("\nDeseja confirmar a compra (S/N)? ").upper()
    if confirmar != "S":
        print("Compra cancelada.")
        return carrinho

    enderecos = usuario.get("end", [])
    if not enderecos:
        print("Nenhum endereço cadastrado. Deseja cadastrar um novo endereço? (S/N)")
        resposta = input().upper()
        if resposta == 'S':
            endereco_entrega = cadastrar_endereco(cpf_usuario)
            enderecos = [endereco_entrega]
        else:
            print("Não é possível continuar com a compra sem um endereço de entrega.")
            return

    print("\nSelecione o endereço de entrega:")
    for i, endereco in enumerate(enderecos, start=1):
        print(f"{i} - {enderecos[i-1]['rua']}, {enderecos[i-1]['num']}, {enderecos[i-1]['bairro']}, {enderecos[i-1]['cidade']}, {enderecos[i-1]['estado']}, CEP: {enderecos[i-1]['cep']}")  
    
    while True:
        endereco_selecionado = input("Digite o número do endereço selecionado (ou 'N' para cadastrar um novo): ")
        if endereco_selecionado.upper() == 'N':
            endereco_entrega = cadastrar_endereco(cpf_usuario)
            break
        try:
            endereco_selecionado = int(endereco_selecionado)
            if 1 <= endereco_selecionado <= len(enderecos):
                endereco_entrega = enderecos[endereco_selecionado - 1]
                break
            else:
                print("Número de endereço inválido.")
        except ValueError:
            print("Entrada inválida. Digite um número válido ou 'N' para cadastrar um novo endereço.")

    # Inserir a compra no banco de dados (Cassandra)
    compra_collection.insert_one({
        "cpf_usuario": cpf_usuario,
        "produtos": carrinho,
        "endereco_entrega": endereco_entrega,
        "valor_total": total
    })

    print("Compra realizada com sucesso.")
    return carrinho

def ver_compras_realizadas(cpf_usuario):
    compra_collection: Collection = db.get_collection("compra")

    print("Compras realizadas pelo usuário:")
    compras_realizadas = compra_collection.find({"cpf_usuario": cpf_usuario})

    count = 0
    for compra in compras_realizadas:
        count += 1
        print(f"Compra {count}:")
        for produto in compra['produtos']:
            print(f"  - {produto['nome']}: R${produto['preco']:.2f}")
        print(f"  Endereço de Entrega: {compra['endereco_entrega']}")
        print(f"  Valor Total: R${compra['valor_total']:.2f}")

    if count == 0:
        print("Nenhuma compra encontrada para este usuário.")


# Função para deletar uma compra
def deletar_compra(cpf_usuario):
    collection: Collection = db.get_collection("compra")
    compras = list(collection.find({"cpf_usuario": cpf_usuario}))

    if not compras:  # Verifica se a lista de compras está vazia
        print("Nenhuma compra encontrada para este usuário.")
        return  # Sai da função se não houver compras

    print("Compras do usuário:")
    for i, compra in enumerate(compras, start=1):
        print(f"{i}. {compra}")
        
    while True:
        try:
            index_str = input("Digite o número da compra que deseja excluir: ")
            if not index_str.isdigit():
                raise ValueError("Entrada inválida. Digite um número.")
            index = int(index_str) - 1
            if index >= 0:
                # Encontra a compra pelo índice e exclui pelo ID
                count = 0
                for compra in collection.find({"cpf_usuario": cpf_usuario}):
                    if count == index:
                        collection.delete_one({"_id": compra["_id"]}) # Filtra pelo _id da compra
                        print("Compra excluída com sucesso!")
                        return
                    count += 1
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError as e:
            print(f"Erro: {e}")



