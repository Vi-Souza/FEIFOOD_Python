MENU = {
    "1": "Aperte 1 se deseja se cadastrar",
    "2": "Aperte 2 se deseja fazer login",
    "0": "Aperte 0 para sair",
}

def exibir_menu(): #função para exibir o menu principal
    print("\n=== Menu Principal ===")
    for chave, valor in MENU.items():
        print(f"{chave} - {valor}")
    print("======================\n")

def novo_cadastro(): #função para novo cadastro
    print("=====Menu de Cadastro=====")
    nome = input("Digite seu nome: ")
    usuario = input("Escolha um nome de usuário: ")
    senha = input("Escolha uma senha: ")
    with open("cadastros.txt", "a") as arquivo:
        arquivo.write(f"{nome},{usuario},{senha}\n")
    print(f"Cadastro realizado com sucesso! Bem-vindo, {nome}!")
    print("==========================")   

def login(): #função para login
    print("=====Menu de Login=====")
    usuario_login = input("Digite seu nome de usuário: ")
    senha_login = input("Digite sua senha: ")
    encontrado = False
    with open("cadastros.txt", "r") as arquivo: #abre o arquivo de cadastros
        for linha in arquivo: #lê cada linha do arquivo
            nome, usuario, senha = linha.strip().split(",") #separa as partes da linha
            if usuario == usuario_login and senha == senha_login: #verifica se o usuário e senha correspondem
                encontrado = True
                menu_usuario_logado(nome)
                break
    if not encontrado: #se não encontrou o usuário
        print("Usuário ou senha incorretos. Tente novamente.")
    print("=======================")

#funções do menu logado
MENU_LOGADO = {
    "1": "Buscar alimentos",
    "2": "Carrinho",
    "3": "Avaliar pedido",
    "0": "Logout",
}

def menu_usuario_logado(usuario): #função do menu logado
    carrinho_do_usuario = []
    while True:
        print(f"\nBem vindo {usuario}!")
        print("=== FEIFOOD ===")
        for chave, valor in MENU_LOGADO.items(): #exibe o menu logado
            print(f"{chave} - {valor}") #exibe cada opção do menu logado
        print("========================")
        escolha = input("Escolha uma opção: ")
        if escolha == "0": 
            print("Logout realizado. Voltando ao menu principal.")
            break
        elif escolha == "1": #se o usuário escolher buscar alimentos
            id_adicionado = buscar_alimentos(usuario) #chama a função de buscar alimentos com o usuário
            if id_adicionado: #se um id foi retornado
                carrinho_do_usuario.append(id_adicionado) #adiciona o id ao carrinho
                print(f"Alimento ID {id_adicionado} adicionado ao carrinho.")
        elif escolha == "2":
            carrinho(carrinho_do_usuario, usuario) #chama a função do carrinho com o carrinho e o usuário
        elif escolha == "3":
            avaliar_pedido(usuario) #chama a função de avaliar pedido com o usuário
        else:
            print("Opção inválida. Tente novamente.")

def buscar_alimentos(usuario): #função para buscar alimentos
    print("===== Buscar Alimentos =====")
    print("Aperte enter para listar todos os alimentos ou digite um termo para buscar.")
    termo = input("Digite o nome ou parte do nome do alimento: ").lower()
    
    encontrados = []

    with open("alimentos.txt", "r") as arquivo: #abre o arquivo de alimentos
        for linha in arquivo: #lê cada linha do arquivo
            partes = linha.strip().split(",") #separa as partes da linha
            if len(partes) == 3: #verifica se a linha tem 3 partes
                id_, nome, preco = partes #pega o id, nome e preço
                if termo in nome.lower(): #verifica se o termo está no nome
                    encontrados.append((id_, nome, preco)) #adiciona o alimento à lista de encontrados

    if encontrados: #se encontrou alimentos
        print("\nAlimentos encontrados:")
        for id_, nome, preco in encontrados: #exibe os alimentos encontrados
            print(f"{id_} - {nome} | R$ {preco}") 
        print("==============================")
        resposta = input("Deseja adicionar algum alimento ao carrinho? (s/n): ").lower()
        if resposta == "s": #se o usuário quiser adicionar um alimento
            id_escolhido = input("Digite o ID do alimento que deseja adicionar: ")
            ids_validos = [item[0] for item in encontrados] #lista de ids válidos
            if id_escolhido in ids_validos: #verifica se o id escolhido é válido
                return id_escolhido #retorna o id escolhido
            else:
                print("ID inválido. Nenhum alimento adicionado.")
    else:
        print("Nenhum alimento encontrado com esse nome.")
        print("==============================")
    
    return None

def avaliar_pedido(usuario, id_pedido=None): #função para avaliar pedido com id opcional e usuário
    print("===== Avaliação de Pedido =====")
    if not id_pedido: #se o id não for fornecido
        id_pedido = input("Digite o ID do pedido que deseja avaliar: ") 

    encontrado = False
    with open("pedidos.txt", "a+") as arquivo: #abre o arquivo de pedidos
        arquivo.seek(0) #volta ao início do arquivo
        for linha in arquivo:
            partes = linha.strip().split(",") #lê cada linha do arquivo
            if len(partes) == 3: #verifica se a linha tem 3 partes
                id_, dono, _ = partes #pega o id e o dono do pedido
                if id_ == str(id_pedido) and dono == usuario: #verifica se o id e o dono correspondem
                    encontrado = True
                    break

    if not encontrado:
        print("Pedido não encontrado ou não pertence a você.")
        return

    while True: 
        nota = input("Dê uma nota de 1 a 5 para o pedido: ").strip()
        if nota.isdigit() and 1 <= int(nota) <= 5: #verifica se a nota é válida
            break
        print("Nota inválida. Digite um número entre 1 e 5.") 

    comentario = input("Deixe um comentário (opcional): ").strip()

    with open("avaliacoes.txt", "a+") as arquivo: #abre o arquivo de avaliações
        arquivo.write(f"{id_pedido};{usuario};{nota};{comentario}\n") #escreve a avaliação no arquivo

    print("Avaliação registrada com sucesso!")

def finalizar_pedido(usuario, lista_ids): #função para finalizar pedido
    novo_id = 1 #inicia o id do pedido
    with open("pedidos.txt", "a+") as arquivo: #abre o arquivo de pedidos
        arquivo.seek(0) #volta ao início do arquivo
        for linha in arquivo:
            partes = linha.strip().split(",") #lê cada linha do arquivo
            if len(partes) >= 2: #verifica se a linha tem pelo menos 2 partes
                id_existente, dono = partes[0], partes[1] #pega o id e o dono do pedido
                if dono == usuario and id_existente.isdigit(): #verifica se o dono é o usuário e se o id é um número
                    id_num = int(id_existente) #converte o id para número
                    if id_num >= novo_id: #atualiza o novo id se necessário
                        novo_id = id_num + 1 #incrementa o id

        arquivo.write(f"{novo_id},{usuario},{'|'.join(lista_ids)}\n") #escreve o novo pedido no arquivo

    print(f"Pedido #{novo_id} finalizado com sucesso para o usuário {usuario}!") 

    avaliar = input("Deseja avaliar este pedido agora? (s/n): ").lower() #pergunta se o usuário quer avaliar o pedido
    if avaliar == "s":
        avaliar_pedido(usuario, str(novo_id)) #chama a função de avaliar pedido com o id do novo pedido

def carrinho(carrinho_do_usuario, usuario): #função do carrinho
    while True:
        print("\n===== Seu Carrinho =====")
        if not carrinho_do_usuario: #verifica se o carrinho está vazio
            print("Carrinho vazio.")
        else: #exibe os itens do carrinho
            alimentos = {}
            with open("alimentos.txt", "a+") as arquivo:
                arquivo.seek(0) #volta ao início do arquivo
                for linha in arquivo:
                    partes = linha.strip().split(",")
                    if len(partes) == 3:
                        id_, nome, preco = partes
                        alimentos[id_] = (nome, preco)

            for id_ in carrinho_do_usuario: #para cada id no carrinho
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
            if id_remover in carrinho_do_usuario: #verifica se o id está no carrinho
                carrinho_do_usuario.remove(id_remover)
                print(f"Item {id_remover} removido do carrinho.")
            else:
                print("ID não encontrado no carrinho.")
        elif escolha == "2":
            if not carrinho_do_usuario: #verifica se o carrinho está vazio
                print("Carrinho vazio. Não é possível finalizar o pedido.")
            else: #finaliza o pedido
                finalizar_pedido(usuario, carrinho_do_usuario) #chama a função de finalizar pedido
                carrinho_do_usuario.clear() #esvazia o carrinho
                break
        else:
            print("Opção inválida. Tente novamente.")

while True: #loop do menu principal
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
