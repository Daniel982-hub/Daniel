# ==============================
# favoritos.py
# armazena e gere os favoritos
# retorna tuplos (codigo_http, mensagem)
# ==============================
import json, os, logging
from datetime import datetime
from utils import gerar_id_favorito
import utilizadores as bd_utilizadores
import conteudo as bd_conteudo

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

FICHEIRO = "favoritos.json"
favoritos = {}

def guardar():
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(favoritos, f, indent=4, ensure_ascii=False)

def carregar():
    global favoritos
    if os.path.exists(FICHEIRO):
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            favoritos = json.load(f)
    else:
        favoritos = {}

# ── CREATE ──────────────────────────────────────────────────
def adicionar_favorito(uid, lista_ids_conteudo):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    if isinstance(lista_ids_conteudo, str):
        lista_ids_conteudo = [c.strip() for c in lista_ids_conteudo.split(",") if c.strip()]
    if not lista_ids_conteudo:
        return 400, "A lista de conteudos nao pode estar vazia."
    for cid in lista_ids_conteudo:
        codigo_c, _ = bd_conteudo.obter_conteudo(cid)
        if codigo_c == 404:
            return 404, f"Conteudo '{cid}' nao encontrado."

    for fid, fav in favoritos.items():
        if fav["idUtilizador"] == uid:
            novos = [c for c in lista_ids_conteudo if c not in fav["lista_ids_Conteudo"]]
            if not novos:
                logging.warning(f"Conteudos duplicados nos favoritos do utilizador '{uid}': {lista_ids_conteudo}.")
                return 409, "Todos os conteudos ja estao nos favoritos deste utilizador."
            fav["lista_ids_Conteudo"].extend(novos)
            fav["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            guardar()
            logging.info(f"Favoritos do utilizador '{uid}' atualizados. Adicionados: {novos}.")
            return 200, fid

    fid = gerar_id_favorito()
    favoritos[fid] = {
        "idFavorito":         fid,
        "idUtilizador":       uid,
        "lista_ids_Conteudo": list(lista_ids_conteudo),
        "data_criacao":       datetime.now().strftime("%d/%m/%Y %H:%M"),
        "data_atualizacao":   datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    guardar()
    logging.info(f"Favoritos criados para o utilizador '{uid}': {lista_ids_conteudo}.")
    return 201, fid

# ── READ (todos) ─────────────────────────────────────────────
def listar_favoritos():
    carregar()
    if not favoritos:
        return 404, "Nenhum favorito registado."
    return 200, favoritos

# ── READ (por utilizador) ────────────────────────────────────
def obter_favoritos_utilizador(uid):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    for fid, fav in favoritos.items():
        if fav["idUtilizador"] == uid:
            return 200, fid
    return 404, f"Nenhum favorito encontrado para o utilizador '{uid}'."

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_favorito(uid, lista_ids_conteudo):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    if isinstance(lista_ids_conteudo, str):
        lista_ids_conteudo = [c.strip() for c in lista_ids_conteudo.split(",") if c.strip()]
    if not lista_ids_conteudo:
        return 400, "A lista de conteudos nao pode estar vazia."
    for cid in lista_ids_conteudo:
        codigo_c, _ = bd_conteudo.obter_conteudo(cid)
        if codigo_c == 404:
            return 404, f"Conteudo '{cid}' nao encontrado."
    for fid, fav in favoritos.items():
        if fav["idUtilizador"] == uid:
            fav["lista_ids_Conteudo"] = list(lista_ids_conteudo)
            fav["data_atualizacao"]   = datetime.now().strftime("%d/%m/%Y %H:%M")
            guardar()
            logging.info(f"Lista de favoritos do utilizador '{uid}' substituida por: {lista_ids_conteudo}.")
            return 200, fid
    return 404, f"Nenhum favorito encontrado para o utilizador '{uid}'."

# ── DELETE ───────────────────────────────────────────────────
def remover_favoritos_utilizador(uid):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    for fid, fav in list(favoritos.items()):
        if fav["idUtilizador"] == uid:
            del favoritos[fid]
            guardar()
            logging.info(f"Favoritos do utilizador '{uid}' removidos.")
            return 200, uid
    return 404, f"Nenhum favorito encontrado para o utilizador '{uid}'."
