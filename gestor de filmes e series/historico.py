# ==============================
# historico.py
# CRUD da entidade HistoricoVisualizacao
# armazenamento em dicionario
# validacoes feitas aqui (nao no main)
# retorna codigos de estado ao estilo HTTP
# ==============================
from utils import gerar_id_historico, validar_progresso
from datetime import datetime

# dicionario principal onde ficam guardados todos os registos de historico
# chave: ID gerado automaticamente (ex: H001)
# valor: dicionario com os dados do historico
historico = {}

# ── CREATE ───────────────────────────────────────────────────────────────────
def criar_historico(idUtilizador, idConteudo, progresso, utilizadores_dict, conteudos_dict):

    # verifica se o utilizador existe
    if idUtilizador not in utilizadores_dict:
        return 404, "Utilizador nao encontrado."

    # verifica se o conteudo existe
    if idConteudo not in conteudos_dict:
        return 404, "Conteudo nao encontrado."

    # valida o progresso (0 a 100)
    if not validar_progresso(progresso):
        return 400, "Progresso invalido. Deve ser um valor inteiro entre 0 e 100."

    try:
        hid = gerar_id_historico()
        historico[hid] = {
            "idUtilizador":     idUtilizador,
            "idConteudo":       idConteudo,
            "dataVisualizacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "progresso":        int(progresso)
        }
        return 201, hid
    except Exception as e:
        return 500, str(e)

# ── READ - listar todos ──────────────────────────────────────────────────────
def listar_historico():
    if not historico:
        return 404, "Nao existem registos de historico."

    try:
        for hid, d in historico.items():
            print(f"  ID: {hid} | Utilizador: {d['idUtilizador']} | "
                  f"Conteudo: {d['idConteudo']} | "
                  f"Data: {d['dataVisualizacao']} | "
                  f"Progresso: {d['progresso']}%")
        return 200, "Historico listado com sucesso."
    except Exception as e:
        return 500, str(e)

# ── READ - consultar individual ──────────────────────────────────────────────
def consultar_historico(hid):
    # retorna 404 se o ID nao existir
    if hid not in historico:
        return 404, "Registo de historico nao encontrado."

    try:
        return 200, historico[hid]
    except Exception as e:
        return 500, str(e)

# ── UPDATE ───────────────────────────────────────────────────────────────────
def atualizar_historico(hid, progresso):
    # retorna 404 se o ID nao existir
    if hid not in historico:
        return 404, "Registo de historico nao encontrado."

    if progresso and not validar_progresso(progresso):
        return 400, "Progresso invalido. Deve ser um valor inteiro entre 0 e 100."

    try:
        if progresso:
            historico[hid]["progresso"]        = int(progresso)
            # atualiza a data para registar quando foi visto pela ultima vez
            historico[hid]["dataVisualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        return 200, "Registo de historico atualizado com sucesso."
    except Exception as e:
        return 500, str(e)

# ── DELETE ───────────────────────────────────────────────────────────────────
def remover_historico(hid):
    # retorna 404 se o ID nao existir
    if hid not in historico:
        return 404, "Registo de historico nao encontrado."

    try:
        del historico[hid]
        return 200, "Registo de historico removido com sucesso."
    except Exception as e:
        return 500, str(e)