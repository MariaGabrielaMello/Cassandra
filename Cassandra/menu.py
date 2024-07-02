import CRUDusuario
import CRUDvendedor
import CRUDproduto
import CRUDcompras

while True:  # Loop principal do menu
    print("1-Usuário")
    print("2-Vendedor")
    print("3- Produto")
    print("4- Compras")
    key = input("Digite a opção desejada? (S para sair) ").upper()

    if key == '1':
        sub = 0  # Reinicia a variável sub para o submenu de usuário
        while sub != 'V':  # Loop do submenu de usuário
            print("Menu do Usuário")
            print("1-Criar Usuário")
            print("2-Listar Usuário")
            print("3-Atualizar Usuário")
            sub = input("Digite a opção desejada? (V para voltar) ").upper()
            if sub == '1':
                CRUDusuario.create_usuario()
            elif sub == '2':
                nome = input("Listar usuários, deseja algum nome especifico? ")
                CRUDusuario.read_usuario(nome)
            elif sub == '3':
                CRUDusuario.update_usuario()

    elif key == '2':
        sub = 0  # Reinicia a variável sub para o submenu de vendedor
        while sub != 'V':  # Loop do submenu de vendedor
            print("Menu do Vendedor")
            print("1-Criar Vendedor")
            print("2-Listar Vendedor")
            print("3-Atualizar Vendedor")  # Opção adicionada para atualizar vendedor
            sub = input("Digite a opção desejada? (V para voltar) ").upper()
            if sub == '1':
                CRUDvendedor.create_vendedor()
            elif sub == '2':
                cpf = input("Listar vendedores, deseja algum cpf especifico? ")
                CRUDvendedor.read_vendedor(cpf)
            elif sub == '3':  # Nova opção para atualizar vendedor
                CRUDvendedor.update_vendedor()
        
    
    elif (key == '3'):
        print("Menu do Produto")  
        print("1-Criar Produto")
        print("2-Listar Produto")    
        print("3-Atualizar Produto")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Criar produto")
            CRUDproduto.create_produto()
            
        elif (sub == '2'):           
            CRUDproduto.read_produto()
        
        elif (sub == '3'):            
            CRUDproduto.update_produto()
          

    elif key == '4':
        print("Compras") 
        print("1 - Realizar compra")
        print("2 - Ver compras realizadas")   
        print("3 - Deletar compra")     
        sub = input("Digite a opção desejada? (V para voltar) ")

        if sub == '1':
            cpf_usuario = input("Digite seu CPF: ")
            carrinho_usuario = CRUDcompras.realizar_compra(cpf_usuario)
              
        elif sub == '2':
            cpf_usuario = input("Digite seu CPF: ")
            CRUDcompras.ver_compras_realizadas(cpf_usuario)
        
        elif sub == '3':
            cpf_usuario = input("Digite seu CPF: ")
            CRUDcompras.deletar_compra(cpf_usuario)
        else:
            print("Opção inválida. Por favor, digite uma opção válida.") 
    
    elif key == 'S':
        break  
        

print("Obrigada!")