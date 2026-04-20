# ==============================
# historico.py
# armazena e gere o historico de visualizacoes
# retorna tuplos (codigo_http, mensagem)
# ==============================
from datetime import datetime
from utils import gerar_id_historico, validar_progresso
import utilizadores as bd_utilizadores
import conteudo as bd_conteudo

historico = {}

# ── CREATE ──────────────────────────────────────────────────
def registar_visualizacao(uid, cid, progresso):
    # valida se o utilizador existe
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    # valida se o conteudo existe
    codigo, _ = bd_conteudo.obter_conteudo(cid)
    if codigo == 404:
        return 404, f"Conteudo '{cid}' nao encontrado."

    # valida o progresso
    if not validar_progresso(str(progresso)):
        return 400, "Progresso invalido. Use um valor entre 0 e 100."

    hid = gerar_id_historico()
    historico[hid] = {
        "idHistorico":      hid,
        "idUtilizador":     uid,
        "idConteudo":       cid,
        "dataVisualizacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "progresso":        round(float(progresso), 1)
    }
    return 201, f"Visualizacao registada com sucesso. ID: {hid}"

# ── READ (todos) ─────────────────────────────────────────────
def listar_historico():
    if not historico:
        return 404, "Nenhuma visualizacao registada."
    return 200, historico

# ── READ (por utilizador) ────────────────────────────────────
def obter_historico_utilizador(uid):
    # valida se o utilizador existe
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    registos = {hid: h for hid, h in historico.items() if h["idUtilizador"] == uid}
    if not registos:
        return 404, f"Nenhuma visualizacao registada para o utilizador '{uid}'."
    return 200, registos

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_historico(hid, progresso=None):
    if hid not in historico:
        return 404, f"Registo '{hid}' nao encontrado."

    try:
        # atualiza apenas os campos que foram preenchidos (nao None)
        if progresso is not None:
            if not validar_progresso(str(progresso)):
                return 400, "Progresso invalido. Use um valor entre 0 e 100."
            historico[hid]["progresso"] = round(float(progresso), 1)

        return 200, "Registo atualizado com sucesso."
    except Exception as e:
        return 500, str(e)

# ── DELETE ───────────────────────────────────────────────────
def remover_historico(hid):
    # retorna 404 se o ID nao existir
    if hid not in historico:
        return 404, f"Registo '{hid}' nao encontrado."

    try:
        del historico[hid]
        return 200, f"Registo '{hid}' removido com sucesso."
    except Exception as e:
        return 500, str(e)
