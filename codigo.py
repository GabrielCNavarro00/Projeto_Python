#================USUARIOS================#
import random

def gerarID():

    while True:

        novoID = str(random.randint(1000, 9999))
        existe = False

        try:
            with open("users/usuarios.txt", "r", encoding="utf-8") as arquivo:

                linhas = arquivo.readlines()

                for linha in linhas:

                    info = linha.strip().split(";")

                    # verifica se o ID já existe
                    if len(info) == 4 and info[0] == novoID:

                        existe = True

        except FileNotFoundError:

            pass

        if not existe:
            return novoID

def usuarioExistente(email):

    try:

        with open("users/usuarios.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

    except FileNotFoundError:
        return False

    for linha in linhas:
        info = linha.strip().split(";")
        if len(info) != 4:
            continue

        if info[2] == email:
            return True

    return False

def cadastroUsuario():

    nome = input("\nDigite seu nome: ")
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    if usuarioExistente(email):
        print("Email já cadastrado!")
        return

    idUsuario = gerarID()

    with open("users/usuarios.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(idUsuario + ";" + nome + ";" + email + ";" + senha + "\n")

    print("Cadastro realizado!")
    print("Seu ID é:", idUsuario)


def validacaoLogin(email, senha):

    try:

        with open("users/usuarios.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

    except FileNotFoundError:
        return False

    for linha in linhas:
        info = linha.strip().split(";")
        if len(info) != 4:
            continue

        if info[2] == email and info[3] == senha:
            return info[0]

    return False

def loginUsuario():

    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    resultado = validacaoLogin(email, senha)

    if resultado:
        print("Login realizado!")
        return resultado
    else:
        print("Email ou senha inválidos")
        return False

#================CONTEUDO================#
def carregarConteudo(caminho):

    conteudos = []

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return conteudos

    for linha in linhas:
        info = linha.strip().split(";")
        if len(info) != 6:
            continue

        conteudo = {
            "nome": info[0],
            "categoria": info[1],
            "duracao": info[2],
            "elenco": info[3],
            "ano": info[4],
            "classificacao": info[5]
        }
        conteudos.append(conteudo)

    return conteudos


#================LISTAS================#
def verLista(nomeArquivo, usuario, titulo):

    try:
        with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
        print(f"\n{titulo}:")

        encontrou = False

        for linha in linhas:
            info = linha.strip().split(";")
            if info[0] == usuario:
                print("-", info[1])
                encontrou = True

        if not encontrou:
            print("Lista vazia.")
    except FileNotFoundError:
        print("Lista vazia.")

def removerDaLista(nomeArquivo, usuario):

    nomeRemover = input("Digite o nome para remover: ")

    try:
        with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
        novasLinhas = []
        for linha in linhas:
            info = linha.strip().split(";")
            # mantém apenas o que NÃO será removido
            if not (
                info[0] == usuario and
                info[1].lower() == nomeRemover.lower()
            ):
                novasLinhas.append(linha)

        with open(nomeArquivo, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(novasLinhas)
        print("Removido com sucesso!")
    except FileNotFoundError:
        print("Lista não existe.")

#================INTERAÇÃO================#

def gerenciarFavoritos(conteudo, usuario):

    nome = conteudo["nome"]

    print(f"\nConteúdo selecionado: {nome}")

    print("1 - Curtir")
    print("2 - Descurtir")
    print("3 - Favoritar")
    print("4 - Assistir mais tarde")
    print("5 - Ver favoritos")
    print("6 - Ver assistir mais tarde")
    print("7 - Remover dos favoritos")
    print("8 - Remover assistir mais tarde")

    opcao = input("Escolha: ")

    if opcao == "1":
        with open("users/curtidas.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(usuario + ";" + nome + "\n")
        print("Conteúdo curtido!")

    elif opcao == "2":
        with open("users/descurtidas.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(usuario + ";" + nome + "\n")
        print("Conteúdo descurtido!")

    elif opcao == "3":
        with open("users/favoritos.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(usuario + ";" + nome + "\n")
        print("Conteúdo favoritado!")

    elif opcao == "4":
        with open("users/assistir_mais_tarde.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(usuario + ";" + nome + "\n")
        print("Adicionado à lista!")

    elif opcao == "5":
        verLista("users/favoritos.txt", usuario, "Seus favoritos")

    elif opcao == "6":
        verLista("users/assistir_mais_tarde.txt", usuario, "Assistir mais tarde")

    elif opcao == "7":
        removerDaLista("users/favoritos.txt", usuario)

    elif opcao == "8":
        removerDaLista("users/assistir_mais_tarde.txt", usuario)

#================MENU================#
def menuConteudo(caminho, tipo, usuario):

    conteudos = carregarConteudo(caminho)

    while True:
        print(f"\n--- {tipo.upper()} ---")

        print("1 - Ver todos")
        print("2 - Buscar por nome")
        print("3 - Buscar por categoria")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            if len(conteudos) == 0:
                print("Nenhum conteúdo encontrado.")
                continue

            for i in range(len(conteudos)):
                print(f"{i+1} - {conteudos[i]['nome']}")

            escolha = int(input("Escolha um número (0 para voltar): "))

            if escolha == 0:

                continue

            indice = escolha - 1

            if indice < 0 or indice >= len(conteudos):
                print("Opção inválida.")
                continue

            conteudoEscolhido = conteudos[indice]

            print("\nNome:", conteudoEscolhido["nome"])
            print("Categoria:", conteudoEscolhido["categoria"])
            print("Duração:", conteudoEscolhido["duracao"])
            print("Elenco:", conteudoEscolhido["elenco"])
            print("Ano:", conteudoEscolhido["ano"])
            print("Classificação:", conteudoEscolhido["classificacao"])

            resposta = input("\nDeseja interagir? (s/n): ")

            if resposta.lower() == "s":
                gerenciarFavoritos(conteudoEscolhido, usuario)

        elif opcao == "2":

            busca = input("Digite o nome: ").lower()

            resultados = []

            for item in conteudos:
                if busca in item["nome"].lower():
                    resultados.append(item)
            if len(resultados) == 0:
                print("Nada encontrado.")
                continue

            for i in range(len(resultados)):
                print(f"{i+1} - {resultados[i]['nome']}")

            escolha = int(input("Escolha um número (0 para voltar): "))

            if escolha == 0:
                continue

            indice = escolha - 1

            if indice < 0 or indice >= len(resultados):
                print("Opção inválida.")
                continue

            conteudoEscolhido = resultados[indice]

            print("\nNome:", conteudoEscolhido["nome"])
            print("Categoria:", conteudoEscolhido["categoria"])
            print("Duração:", conteudoEscolhido["duracao"])
            print("Elenco:", conteudoEscolhido["elenco"])
            print("Ano:", conteudoEscolhido["ano"])
            print("Classificação:", conteudoEscolhido["classificacao"])

            resposta = input("\nDeseja interagir? (s/n): ")

            if resposta.lower() == "s":

                gerenciarFavoritos(conteudoEscolhido, usuario)

        elif opcao == "3":

            categorias = []

            for item in conteudos:
                if item["categoria"] not in categorias:
                    categorias.append(item["categoria"])

            for i in range(len(categorias)):
                print(f"{i+1} - {categorias[i]}")
            escolhaCategoria = int(input("Escolha categoria: ")) - 1

            if escolhaCategoria < 0 or escolhaCategoria >= len(categorias):
                print("Categoria inválida.")
                continue

            categoriaEscolhida = categorias[escolhaCategoria]

            resultados = []

            for item in conteudos:
                if item["categoria"] == categoriaEscolhida:
                    resultados.append(item)

            for i in range(len(resultados)):
                print(f"{i+1} - {resultados[i]['nome']}")

            escolha = int(input("Escolha um número (0 para voltar): "))

            if escolha == 0:
                continue

            indice = escolha - 1

            if indice < 0 or indice >= len(resultados):
                print("Opção inválida.")
                continue

            conteudoEscolhido = resultados[indice]

            print("\nNome:", conteudoEscolhido["nome"])
            print("Categoria:", conteudoEscolhido["categoria"])
            print("Duração:", conteudoEscolhido["duracao"])
            print("Elenco:", conteudoEscolhido["elenco"])
            print("Ano:", conteudoEscolhido["ano"])
            print("Classificação:", conteudoEscolhido["classificacao"])

            resposta = input("\nDeseja interagir? (s/n): ")

            if resposta.lower() == "s":
                gerenciarFavoritos(conteudoEscolhido, usuario)

        elif opcao == "0":
            break

        else:

            print("Opção inválida.")


#================SISTEMA PRINCIPAL================#
def sistema():

    logado = False
    usuario = None

    while True:

        if not logado:
            print("\n1 - Cadastro")
            print("2 - Login")
            print("0 - Sair")

            opcao = input("Escolha: ")

            if opcao == "1":
                cadastroUsuario()

            elif opcao == "2":
                usuario = loginUsuario()

                if usuario:
                    logado = True

            elif opcao == "0":
                print("Encerrando sistema...")
                break

        else:

            print("\n1 - Filmes")
            print("2 - Séries")
            print("3 - Ver favoritos")
            print("4 - Ver assistir mais tarde")
            print("0 - Logout")

            opcao = input("Escolha: ")

            if opcao == "1":
                menuConteudo("conteudo/filmes.txt", "filmes", usuario)

            elif opcao == "2":
                menuConteudo("conteudo/series.txt", "series", usuario)

            elif opcao == "3":
                verLista("users/favoritos.txt", usuario, "Seus favoritos")

            elif opcao == "4":
                verLista("users/assistir_mais_tarde.txt", usuario, "Assistir mais tarde")

            elif opcao == "0":
                print("Deslogando...")

                logado = False
                usuario = None


#================INICIO================#

sistema()