# ==============================
# main.py
# menu terminal para testar CRUD
# ponto de entrada do programa
# verifica os codigos de retorno
# e mostra mensagens ao utilizador
# ==============================
import utilizadores as bd_utilizadores
import conteudo     as bd_conteudo
import historico    as bd_historico

# ── helper: mostra o resultado de qualquer operacao ─────────
def mostrar(codigo, dados):
    if codigo in (200, 201):
        print(f"\n[{codigo}] ", end="")
        if isinstance(dados, dict):
            for item in dados.values():
                print(item)
        else:
            print(dados)
    else:
        print(f"\n[ERRO {codigo}] {dados}")

# ── MENUS ────────────────────────────────────────────────────
def menu_principal():
    print("\n========== GESTOR DE STREAMING ==========")
    print("1 - Utilizadores")
    print("2 - Conteudos")
    print("3 - Historico de Visualizacoes")
    print("0 - Sair")
    print("==========================================")

def menu_utilizadores():
    print("\n----- Utilizadores -----")
    print("1 - Criar")
    print("2 - Listar todos")
    print("3 - Obter por ID")
    print("4 - Atualizar")
    print("5 - Remover")
    print("0 - Voltar")

def menu_conteudos():
    print("\n----- Conteudos -----")
    print("1 - Criar")
    print("2 - Listar todos")
    print("3 - Obter por ID")
    print("4 - Atualizar")
    print("5 - Remover")
    print("0 - Voltar")

def menu_historico():
    print("\n----- Historico -----")
    print("1 - Registar visualizacao")
    print("2 - Listar todo o historico")
    print("3 - Ver historico de um utilizador")
    print("4 - Atualizar progresso")
    print("5 - Remover registo")
    print("0 - Voltar")

# ── GESTAO DE UTILIZADORES ───────────────────────────────────
def gerir_utilizadores():
    while True:
        menu_utilizadores()
        op = input("Opcao: ").strip()

        if op == "1":
            nome      = input("Nome: ")
            email     = input("Email: ")
            passe     = input("Palavra-passe: ")
            plano     = input("Plano (basic/premium): ")
            mostrar(*bd_utilizadores.criar_utilizador(nome, email, passe, plano))

        elif op == "2":
            mostrar(*bd_utilizadores.listar_utilizadores())

        elif op == "3":
            uid = input("ID (ex: U001): ")
            mostrar(*bd_utilizadores.obter_utilizador(uid))

        elif op == "4":
            uid   = input("ID (ex: U001): ")
            nome  = input("Novo nome (Enter para ignorar): ")
            email = input("Novo email (Enter para ignorar): ")
            passe = input("Nova palavra-passe (Enter para ignorar): ")
            plano = input("Novo plano (Enter para ignorar): ")
            mostrar(*bd_utilizadores.atualizar_utilizador(
                uid,
                nome      or None,
                email     or None,
                passe     or None,
                plano     or None
            ))

        elif op == "5":
            uid = input("ID (ex: U001): ")
            mostrar(*bd_utilizadores.remover_utilizador(uid))

        elif op == "0":
            break
        else:
            print("Opcao invalida!")

# ── GESTAO DE CONTEUDOS ──────────────────────────────────────
def gerir_conteudos():
    while True:
        menu_conteudos()
        op = input("Opcao: ").strip()

        if op == "1":
            titulo    = input("Titulo: ")
            tipo      = input("Tipo (filme/serie): ")
            genero    = input("Genero: ")
            ano       = input("Ano de lancamento: ")
            class_et  = input("Classificacao etaria (ex: M/6, M/12, M/16, M/18): ")
            aval      = input("Avaliacao (0-10): ")
            num_aval  = input("Numero de avaliadores: ")
            produtor  = input("Produtor: ")
            realizador = input("Realizador: ")
            duracao = numero_temporadas = 0
            if tipo.lower() == "filme":
                duracao = input("Duracao (min): ") or 0
            else:
                numero_temporadas = input("Numero de temporadas: ") or 0
            mostrar(*bd_conteudo.criar_conteudo(
                titulo, tipo, genero, ano, class_et,
                aval, num_aval, produtor, realizador,
                duracao, numero_temporadas
            ))

        elif op == "2":
            mostrar(*bd_conteudo.listar_conteudos())

        elif op == "3":
            cid = input("ID (ex: C001): ")
            mostrar(*bd_conteudo.obter_conteudo(cid))

        elif op == "4":
            cid        = input("ID (ex: C001): ")
            titulo     = input("Novo titulo (Enter para ignorar): ")
            avaliacao  = input("Nova avaliacao (Enter para ignorar): ")
            produtor   = input("Novo produtor (Enter para ignorar): ")
            realizador = input("Novo realizador (Enter para ignorar): ")
            mostrar(*bd_conteudo.atualizar_conteudo(
                cid,
                titulo     or None,
                avaliacao  = float(avaliacao) if avaliacao else None,
                produtor   = produtor   or None,
                realizador = realizador or None
            ))

        elif op == "5":
            cid = input("ID (ex: C001): ")
            mostrar(*bd_conteudo.remover_conteudo(cid))

        elif op == "0":
            break
        else:
            print("Opcao invalida!")

# ── GESTAO DE HISTORICO ──────────────────────────────────────
def gerir_historico():
    while True:
        menu_historico()
        op = input("Opcao: ").strip()

        if op == "1":
            uid       = input("ID Utilizador (ex: U001): ")
            cid       = input("ID Conteudo (ex: C001): ")
            progresso = input("Progresso (0-100%): ")
            mostrar(*bd_historico.registar_visualizacao(uid, cid, progresso))

        elif op == "2":
            mostrar(*bd_historico.listar_historico())

        elif op == "3":
            uid = input("ID Utilizador (ex: U001): ")
            mostrar(*bd_historico.obter_historico_utilizador(uid))

        elif op == "4":
            hid       = input("ID Registo (ex: H001): ")
            progresso = input("Novo progresso (0-100%): ")
            mostrar(*bd_historico.atualizar_historico(hid, progresso or None))

        elif op == "5":
            hid = input("ID Registo (ex: H001): ")
            mostrar(*bd_historico.remover_historico(hid))

        elif op == "0":
            break
        else:
            print("Opcao invalida!")

# ── MAIN ─────────────────────────────────────────────────────
def main():
    while True:
        menu_principal()
        op = input("Opcao: ").strip()
        if op == "1":
            gerir_utilizadores()
        elif op == "2":
            gerir_conteudos()
        elif op == "3":
            gerir_historico()
        elif op == "0":
            print("A sair... Ate logo!")
            break
        else:
            print("Opcao invalida!")

if __name__ == "__main__":
    main()
