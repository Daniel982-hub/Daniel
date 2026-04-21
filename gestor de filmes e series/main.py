# ==============================
# main.py
# menu terminal para testar CRUD
# ponto de entrada do programa
# verifica os codigos de retorno
# e mostra mensagens ao utilizador
# os inputs e loops ficam todos aqui
# ==============================
import os
from utilizadores import (
    criar_utilizador,
    listar_utilizadores,
    consultar_utilizador,
    atualizar_utilizador,
    remover_utilizador,
    utilizadores
)
from conteudos import (
    criar_conteudo,
    listar_conteudos,
    consultar_conteudo,
    atualizar_conteudo,
    remover_conteudo,
    conteudos
)
from historico import (
    criar_historico,
    listar_historico,
    consultar_historico,
    atualizar_historico,
    remover_historico
)

# limpa o ecra conforme o sistema operativo (Windows ou Linux/Mac)
def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

# imprime o cabecalho do programa
def cabecalho():
    print("=" * 45)
    print("   🎬  GESTOR DE FILMES E SERIES  🎬")
    print("=" * 45)

# menu principal
def menu():
    limpar()
    cabecalho()
    print()
    print("  1. Utilizadores")
    print("  2. Conteudos (Filmes / Series)")
    print("  3. Historico de Visualizacao")
    print("  0. Sair")
    print("-" * 45)

# submenu de utilizadores
def menu_utilizadores():
    limpar()
    cabecalho()
    print("\n  ── UTILIZADORES ──\n")
    print("  1. Criar utilizador")
    print("  2. Listar utilizadores")
    print("  3. Consultar utilizador")
    print("  4. Atualizar utilizador")
    print("  5. Remover utilizador")
    print("  0. Voltar")
    print("-" * 45)

# submenu de conteudos
def menu_conteudos():
    limpar()
    cabecalho()
    print("\n  ── CONTEUDOS ──\n")
    print("  1. Criar conteudo")
    print("  2. Listar conteudos")
    print("  3. Consultar conteudo")
    print("  4. Atualizar conteudo")
    print("  5. Remover conteudo")
    print("  0. Voltar")
    print("-" * 45)

# submenu de historico
def menu_historico():
    limpar()
    cabecalho()
    print("\n  ── HISTORICO DE VISUALIZACAO ──\n")
    print("  1. Registar visualizacao")
    print("  2. Listar todo o historico")
    print("  3. Consultar registo")
    print("  4. Atualizar progresso")
    print("  5. Remover registo")
    print("  0. Voltar")
    print("-" * 45)

def main():
    while True:
        menu()
        opcao = input("  Opcao: ")

        # ── UTILIZADORES ────────────────────────────────────────────────────
        if opcao == "1":
            while True:
                menu_utilizadores()
                op = input("  Opcao: ")
                print()

                if op == "1":
                    # recolhe os dados — loop repete se houver erro de validacao (400)
                    while True:
                        nome        = input("  Nome: ")
                        email       = input("  Email: ")
                        palavraPasse = input("  Password: ")
                        print("  Planos disponiveis: basico, standard, premium")
                        tipoPlan    = input("  Tipo de plano: ")
                        print("  Estados disponiveis: ativo, inativo, suspenso")
                        estado      = input("  Estado: ")
                        print()
                        code, obj = criar_utilizador(nome, email, palavraPasse, tipoPlan, estado)
                        if code == 201:
                            print(f"  [{code}] Utilizador criado com sucesso. Nome: {obj['nome']}")
                            break
                        elif code == 400:
                            print(f"  [{code}] {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "2":
                    print()
                    code, obj = listar_utilizadores()
                    if code == 200:
                        for uid, dados in obj.items():
                            print(f"  ID: {uid} | Nome: {dados['nome']} | "
                                  f"Email: {dados['email']} | "
                                  f"Plano: {dados['tipoPlan']} | "
                                  f"Estado: {dados['estado']}")
                    elif code == 404:
                        print(f"  [{code}] Not Found: {obj}")
                    elif code == 500:
                        print(f"  [{code}] Internal Error: {obj}")

                elif op == "3":
                    # loop repete se o ID nao existir (404)
                    while True:
                        uid = input("  ID do utilizador: ")
                        print()
                        code, dados = consultar_utilizador(uid)
                        if code == 200:
                            print(f"  ID: {uid}")
                            print(f"    Nome:       {dados['nome']}")
                            print(f"    Email:      {dados['email']}")
                            # mostra a password mascarada com asteriscos por seguranca
                            print(f"    Password:   {'*' * len(dados['palavraPasse'])}")
                            print(f"    Plano:      {dados['tipoPlan']}")
                            print(f"    Estado:     {dados['estado']}")
                            break
                        elif code == 404:
                            print(f"  [{code}] Not Found: {dados}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {dados}")
                            break

                elif op == "4":
                    # loop repete se o ID nao existir (404) ou dados invalidos (400)
                    while True:
                        uid         = input("  ID do utilizador: ")
                        nome        = input("  Novo nome (enter para manter): ")
                        email       = input("  Novo email (enter para manter): ")
                        palavraPasse = input("  Nova password (enter para manter): ")
                        tipoPlan    = input("  Novo plano basico/standard/premium (enter para manter): ")
                        estado      = input("  Novo estado ativo/inativo/suspenso (enter para manter): ")
                        print()
                        # passa None nos campos que ficaram em branco
                        code, obj = atualizar_utilizador(
                            uid,
                            nome         if nome         else None,
                            email        if email        else None,
                            palavraPasse if palavraPasse else None,
                            tipoPlan     if tipoPlan     else None,
                            estado       if estado       else None
                        )
                        if code == 200:
                            print(f"  [{code}] {obj}")
                            break
                        elif code in (400, 404):
                            print(f"  [{code}] {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "5":
                    # loop repete se o ID nao existir (404)
                    while True:
                        uid = input("  ID do utilizador: ")
                        print()
                        code, obj = remover_utilizador(uid)
                        if code == 200:
                            print(f"  [{code}] {obj}")
                            break
                        elif code == 404:
                            print(f"  [{code}] Not Found: {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "0":
                    break

                else:
                    print("  Opcao invalida.")

                input("\n  Pressiona ENTER para continuar...")

        # ── CONTEUDOS ────────────────────────────────────────────────────────
        elif opcao == "2":
            while True:
                menu_conteudos()
                op = input("  Opcao: ")
                print()

                if op == "1":
                    # loop repete se houver erro de validacao (400)
                    while True:
                        titulo    = input("  Titulo: ")
                        print("  Tipos disponiveis: filme, serie")
                        tipo      = input("  Tipo: ")
                        genero    = input("  Genero (ex: acao, drama, comedia): ")
                        anoLanc   = input("  Ano de lancamento: ")
                        print("  Classificacoes: g, pg, pg-13, m/12, m/16, m/18")
                        classif   = input("  Classificacao etaria: ")
                        aval      = input("  Avaliacao (0.0 a 10.0): ")
                        numAval   = input("  Numero de avaliadores: ")
                        if tipo.lower() == "filme":
                            dur_temp = input("  Duracao (minutos): ")
                        else:
                            dur_temp = input("  Numero de temporadas: ")
                        produtor  = input("  Produtor: ")
                        realiz    = input("  Realizador: ")
                        print()
                        code, obj = criar_conteudo(titulo, tipo, genero, anoLanc, classif,
                                                   aval, numAval, dur_temp, produtor, realiz)
                        if code == 201:
                            print(f"  [{code}] Conteudo criado com sucesso. ID: {obj}")
                            break
                        elif code == 400:
                            print(f"  [{code}] {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "2":
                    print()
                    code, obj = listar_conteudos()
                    if code == 404:
                        print(f"  [{code}] Not Found: {obj}")
                    elif code == 500:
                        print(f"  [{code}] Internal Error: {obj}")

                elif op == "3":
                    # loop repete se o ID nao existir (404)
                    while True:
                        cid = input("  ID do conteudo: ")
                        print()
                        code, dados = consultar_conteudo(cid)
                        if code == 200:
                            print(f"  ID: {cid}")
                            print(f"    Titulo:         {dados['titulo']}")
                            print(f"    Tipo:           {dados['tipo'].capitalize()}")
                            print(f"    Genero:         {dados['genero']}")
                            print(f"    Ano:            {dados['anoLancamento']}")
                            print(f"    Classificacao:  {dados['classificacaoEtaria'].upper()}")
                            print(f"    Avaliacao:      {dados['avaliacao']}/10 ({dados['numeroAvaliadores']} avaliadores)")
                            if dados["tipo"] == "filme":
                                print(f"    Duracao:        {dados.get('duracao', '?')} min")
                            else:
                                print(f"    Temporadas:     {dados.get('numeroTemporadas', '?')}")
                            print(f"    Produtor:       {dados['produtor']}")
                            print(f"    Realizador:     {dados['realizador']}")
                            break
                        elif code == 404:
                            print(f"  [{code}] Not Found: {dados}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {dados}")
                            break

                elif op == "4":
                    # loop repete se o ID nao existir (404) ou dados invalidos (400)
                    while True:
                        cid     = input("  ID do conteudo: ")
                        titulo  = input("  Novo titulo (enter para manter): ")
                        genero  = input("  Novo genero (enter para manter): ")
                        anoLanc = input("  Novo ano de lancamento (enter para manter): ")
                        classif = input("  Nova classificacao g/pg/pg-13/m12/m16/m18 (enter para manter): ")
                        aval    = input("  Nova avaliacao 0.0-10.0 (enter para manter): ")
                        numAval = input("  Novo numero de avaliadores (enter para manter): ")
                        dur_temp = input("  Nova duracao/temporadas (enter para manter): ")
                        produtor = input("  Novo produtor (enter para manter): ")
                        realiz   = input("  Novo realizador (enter para manter): ")
                        print()
                        # passa None nos campos que ficaram em branco
                        code, obj = atualizar_conteudo(
                            cid,
                            titulo   if titulo   else None,
                            genero   if genero   else None,
                            anoLanc  if anoLanc  else None,
                            classif  if classif  else None,
                            aval     if aval     else None,
                            numAval  if numAval  else None,
                            dur_temp if dur_temp else None,
                            produtor if produtor else None,
                            realiz   if realiz   else None
                        )
                        if code == 200:
                            print(f"  [{code}] {obj}")
                            break
                        elif code in (400, 404):
                            print(f"  [{code}] {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "5":
                    # loop repete se o ID nao existir (404)
                    while True:
                        cid = input("  ID do conteudo: ")
                        print()
                        code, obj = remover_conteudo(cid)
                        if code == 200:
                            print(f"  [{code}] {obj}")
                            break
                        elif code == 404:
                            print(f"  [{code}] Not Found: {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "0":
                    break

                else:
                    print("  Opcao invalida.")

                input("\n  Pressiona ENTER para continuar...")

        # ── HISTORICO ────────────────────────────────────────────────────────
        elif opcao == "3":
            while True:
                menu_historico()
                op = input("  Opcao: ")
                print()

                if op == "1":
                    # loop repete se houver erro de validacao (400) ou IDs invalidos (404)
                    while True:
                        uid      = input("  ID do utilizador: ")
                        cid      = input("  ID do conteudo: ")
                        progresso = input("  Progresso (0 a 100): ")
                        print()
                        code, obj = criar_historico(uid, cid, progresso, utilizadores, conteudos)
                        if code == 201:
                            print(f"  [{code}] Visualizacao registada com sucesso. ID: {obj}")
                            break
                        elif code in (400, 404):
                            print(f"  [{code}] {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "2":
                    print()
                    code, obj = listar_historico()
                    if code == 404:
                        print(f"  [{code}] Not Found: {obj}")
                    elif code == 500:
                        print(f"  [{code}] Internal Error: {obj}")

                elif op == "3":
                    # loop repete se o ID nao existir (404)
                    while True:
                        hid = input("  ID do registo: ")
                        print()
                        code, dados = consultar_historico(hid)
                        if code == 200:
                            print(f"  ID: {hid}")
                            print(f"    Utilizador:   {dados['idUtilizador']}")
                            print(f"    Conteudo:     {dados['idConteudo']}")
                            print(f"    Data:         {dados['dataVisualizacao']}")
                            print(f"    Progresso:    {dados['progresso']}%")
                            break
                        elif code == 404:
                            print(f"  [{code}] Not Found: {dados}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {dados}")
                            break

                elif op == "4":
                    # loop repete se o ID nao existir (404) ou dados invalidos (400)
                    while True:
                        hid       = input("  ID do registo: ")
                        progresso = input("  Novo progresso 0-100 (enter para manter): ")
                        print()
                        code, obj = atualizar_historico(
                            hid,
                            progresso if progresso else None
                        )
                        if code == 200:
                            print(f"  [{code}] {obj}")
                            break
                        elif code in (400, 404):
                            print(f"  [{code}] {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "5":
                    # loop repete se o ID nao existir (404)
                    while True:
                        hid = input("  ID do registo: ")
                        print()
                        code, obj = remover_historico(hid)
                        if code == 200:
                            print(f"  [{code}] {obj}")
                            break
                        elif code == 404:
                            print(f"  [{code}] Not Found: {obj}")
                        elif code == 500:
                            print(f"  [{code}] Internal Error: {obj}")
                            break

                elif op == "0":
                    break

                else:
                    print("  Opcao invalida.")

                input("\n  Pressiona ENTER para continuar...")

        # ── SAIR ─────────────────────────────────────────────────────────────
        elif opcao == "0":
            limpar()
            cabecalho()
            print("\n  Ate logo! 👋\n")
            break

        else:
            print("  Opcao invalida.")
            input("\n  Pressiona ENTER para continuar...")

# ponto de entrada - so executa main() se este ficheiro for corrido diretamente
if __name__ == "__main__":
    main()