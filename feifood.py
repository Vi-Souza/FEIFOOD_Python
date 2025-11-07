MENU = {
    "1": "Aperte 1 se deseja se cadastrar",
    "2": "Aperte 2 se deseja fazer login",
    "0": "Aperte 0 para sair",
}

def exibir_menu():
    print("\n=== Menu Principal ===")
    for chave, valor in MENU.items():
        print(f"{chave} - {valor}")
    print("======================\n")

def novo_cadastro():
    print("=====Menu de Cadastro=====")
    nome = input("Digite seu nome: ")
    usuario = input("Escolha um nome de usuário: ")
    senha = input("Escolha uma senha: ")
    with open("cadastros.txt", "a") as arquivo:
        arquivo.write(f"{nome},{usuario},{senha}\n")
    print(f"Cadastro realizado com sucesso! Bem-vindo, {nome}!")
    print("==========================")   

def login():
    print("=====Menu de Login=====")
    usuario_login = input("Digite seu nome de usuário: ")
    senha_login = input("Digite sua senha: ")
    encontrado = False
    with open("cadastros.txt", "r") as arquivo:
        for linha in arquivo:
            nome, usuario, senha = linha.strip().split(",")
            if usuario == usuario_login and senha == senha_login:
                encontrado = True
                menu_usuario_logado(nome)
                break
    if not encontrado:
        print("Usuário ou senha incorretos. Tente novamente.")
    print("=======================")

#funções do menu logado
MENU_LOGADO = {
    "1": "Buscar alimentos",
    "2": "Carrinho",
    "3": "Avaliar pedido",
    "0": "Logout",
}

def menu_usuario_logado(usuario):
    carrinho_do_usuario = []
    while True:
        print("\n=== FEIFOOD ===")
        for chave, valor in MENU_LOGADO.items():
            print(f"{chave} - {valor}")
        print("========================")
        escolha = input("Escolha uma opção: ")
        if escolha == "0":
            print("Logout realizado. Voltando ao menu principal.")
            break
        elif escolha == "1":
            id_adicionado = buscar_alimentos(usuario)
            if id_adicionado:
                carrinho_do_usuario.append(id_adicionado)
                print(f"Alimento ID {id_adicionado} adicionado ao carrinho.")
        elif escolha == "2":
            carrinho(carrinho_do_usuario, usuario)
        elif escolha == "3":
            avaliar_pedido(usuario)
        else:
            print("Opção inválida. Tente novamente.")

def buscar_alimentos(usuario):
    print("===== Buscar Alimentos =====")
    print("Aperte enter para listar todos os alimentos ou digite um termo para buscar.")
    termo = input("Digite o nome ou parte do nome do alimento: ").lower()
    
    encontrados = []

    with open("alimentos.txt", "r") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(",")
            if len(partes) == 3:
                id_, nome, preco = partes
                if termo in nome.lower():
                    encontrados.append((id_, nome, preco))

    if encontrados:
        print("\nAlimentos encontrados:")
        for id_, nome, preco in encontrados:
            print(f"{id_} - {nome} | R$ {preco}")
        print("==============================")
        resposta = input("Deseja adicionar algum alimento ao carrinho? (s/n): ").lower()
        if resposta == "s":
            id_escolhido = input("Digite o ID do alimento que deseja adicionar: ")
            ids_validos = [item[0] for item in encontrados]
            if id_escolhido in ids_validos:
                return id_escolhido
            else:
                print("ID inválido. Nenhum alimento adicionado.")
    else:
        print("Nenhum alimento encontrado com esse nome.")
        print("==============================")
    
    return None

def avaliar_pedido(usuario, id_pedido=None):
    print("===== Avaliação de Pedido =====")
    if not id_pedido:
        id_pedido = input("Digite o ID do pedido que deseja avaliar: ")

    encontrado = False
    with open("pedidos.txt", "r") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(",")
            if len(partes) == 3:
                id_, dono, _ = partes
                if id_ == id_pedido and dono == usuario:
                    encontrado = True
                    break

    if not encontrado:
        print("Pedido não encontrado ou não pertence a você.")
        return

    nota = input("Dê uma nota de 1 a 5 para o pedido: ")
    comentario = input("Deixe um comentário (opcional): ")

    with open("avaliacoes.txt", "a") as arquivo:
        arquivo.write(f"{id_pedido},{usuario},{nota},{comentario}\n")

    print("Avaliação registrada com sucesso!")

def finalizar_pedido(usuario, lista_ids):
    novo_id = 1
    with open("pedidos.txt", "r") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(",")
            if partes and partes[0].isdigit():
                id_existente = int(partes[0])
                if id_existente >= novo_id:
                    novo_id = id_existente + 1

    with open("pedidos.txt", "a") as arquivo:
        arquivo.write(f"{novo_id},{usuario},{'|'.join(lista_ids)}\n")

    print(f"Pedido #{novo_id} finalizado com sucesso!")

    avaliar = input("Deseja avaliar este pedido agora? (s/n): ").lower()
    if avaliar == "s":
        avaliar_pedido(usuario, str(novo_id))

def carrinho(carrinho_do_usuario, usuario):
    while True:
        print("\n===== Seu Carrinho =====")
        if not carrinho_do_usuario:
            print("Carrinho vazio.")
        else:
            alimentos = {}
            with open("alimentos.txt", "r") as arquivo:
                for linha in arquivo:
                    partes = linha.strip().split(",")
                    if len(partes) == 3:
                        id_, nome, preco = partes
                        alimentos[id_] = (nome, preco)

            for id_ in carrinho_do_usuario:
                if id_ in alimentos:
                    nome, preco = alimentos[id_]
                    print(f"{id_} - {nome} | R$ {preco}")
        
        print("=========================")
        print("Opções:")
        print("1 - Remover item do carrinho")
        print("2 - Finalizar pedido")
        print("0 - Voltar ao menu logado")
        escolha = input("Escolha uma opção: ")

        if escolha == "0":
            break
        elif escolha == "1":
            id_remover = input("Digite o ID do alimento que deseja remover: ")
            if id_remover in carrinho_do_usuario:
                carrinho_do_usuario.remove(id_remover)
                print(f"Item {id_remover} removido do carrinho.")
            else:
                print("ID não encontrado no carrinho.")
        elif escolha == "2":
            if not carrinho_do_usuario:
                print("Carrinho vazio. Não é possível finalizar o pedido.")
            else:
                finalizar_pedido(usuario, carrinho_do_usuario)
                carrinho_do_usuario.clear()
                break
        else:
            print("Opção inválida. Tente novamente.")

while True:
    exibir_menu()
    opcao = input("Escolha uma opção: ")
    if opcao == "0":
        print("Saindo do programa. Até logo!")
        break
    elif opcao == "1":
        novo_cadastro()
    elif opcao == "2":
        login()
    else:
        print("Opção inválida. Tente novamente.")