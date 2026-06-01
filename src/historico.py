# ==============================
# historico.py
# armazena e gere o historico de visualizacoes
# retorna tuplos (codigo_http, mensagem)
# ==============================
import json, os, logging
from datetime import datetime
from utils import gerar_id_historico, validar_progresso
import utilizadores as bd_utilizadores
import conteudo as bd_conteudo

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

FICHEIRO = "historico.json"
historico = {}

def guardar():
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

def carregar():
    global historico
    if os.path.exists(FICHEIRO):
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = {}

# ── CREATE ──────────────────────────────────────────────────
def registar_visualizacao(uid, cid, progresso):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    codigo, _ = bd_conteudo.obter_conteudo(cid)
    if codigo == 404:
        return 404, f"Conteudo '{cid}' nao encontrado."
    if not validar_progresso(str(progresso)):
        logging.warning(f"Progresso invalido registado pelo utilizador '{uid}': '{progresso}'.")
        return 400, "Progresso invalido. Use um valor entre 0 e 100."

    hid = gerar_id_historico()
    historico[hid] = {
        "idHistorico":      hid,
        "idUtilizador":     uid,
        "idConteudo":       cid,
        "dataVisualizacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "progresso":        round(float(progresso), 1)
    }
    guardar()
    logging.info(f"Utilizador '{uid}' visualizou conteudo '{cid}' com progresso {progresso}%.")
    return 201, hid

# ── READ (todos) ─────────────────────────────────────────────
def listar_historico():
    carregar()
    if not historico:
        return 404, "Nenhuma visualizacao registada."
    return 200, historico

# ── READ (por utilizador) ────────────────────────────────────
def obter_historico_utilizador(uid):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    registos = [hid for hid, h in historico.items() if h["idUtilizador"] == uid]
    if not registos:
        return 404, f"Nenhuma visualizacao registada para o utilizador '{uid}'."
    logging.info(f"Historico do utilizador '{uid}' consultado: {len(registos)} registo(s).")
    return 200, registos

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_historico(hid, progresso=None):
    carregar()
    if hid not in historico:
        logging.warning(f"Tentativa de atualizar registo de historico inexistente: '{hid}'.")
        return 404, f"Registo '{hid}' nao encontrado."
    if progresso is not None:
        if not validar_progresso(str(progresso)):
            logging.warning(f"Progresso invalido na atualizacao do registo '{hid}': '{progresso}'.")
            return 400, "Progresso invalido. Use um valor entre 0 e 100."
        historico[hid]["progresso"] = round(float(progresso), 1)
    guardar()
    logging.info(f"Registo de historico '{hid}' atualizado para progresso {progresso}%.")
    return 200, hid

# ── DELETE ───────────────────────────────────────────────────
def remover_historico(hid):
    carregar()
    if hid not in historico:
        logging.warning(f"Tentativa de remover registo de historico inexistente: '{hid}'.")
        return 404, f"Registo '{hid}' nao encontrado."
    del historico[hid]
    guardar()
    logging.info(f"Registo de historico '{hid}' removido.")
    return 200, hid
