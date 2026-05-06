# ==============================
# favoritos.py
# armazena e gere os favoritos
# retorna tuplos (codigo_http, mensagem)
# ==============================
from datetime import datetime
from utils import gerar_id_favorito
import utilizadores as bd_utilizadores
import conteudo as bd_conteudo

favoritos = {}

# ── CREATE ──────────────────────────────────────────────────
def adicionar_favorito(uid, lista_ids_conteudo):
    # valida se o utilizador existe
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    # aceita string separada por virgulas ou lista
    if isinstance(lista_ids_conteudo, str):
        lista_ids_conteudo = [c.strip() for c in lista_ids_conteudo.split(",") if c.strip()]

    if not lista_ids_conteudo:
        return 400, "A lista de conteudos nao pode estar vazia."

    # valida cada conteudo
    for cid in lista_ids_conteudo:
        codigo_c, _ = bd_conteudo.obter_conteudo(cid)
        if codigo_c == 404:
            return 404, f"Conteudo '{cid}' nao encontrado."

    # se o utilizador ja tem favoritos, atualiza a lista existente
    for fid, fav in favoritos.items():
        if fav["idUtilizador"] == uid:
            novos = [c for c in lista_ids_conteudo if c not in fav["lista_ids_Conteudo"]]
            if not novos:
                return 409, "Todos os conteudos ja estao nos favoritos deste utilizador."
            fav["lista_ids_Conteudo"].extend(novos)
            fav["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            return 200, f"Favoritos atualizados. Adicionados: {novos}"

    # cria novo registo de favoritos
    fid = gerar_id_favorito()
    favoritos[fid] = {
        "idFavorito":        fid,
        "idUtilizador":      uid,
        "lista_ids_Conteudo": list(lista_ids_conteudo),
        "data_criacao":      datetime.now().strftime("%d/%m/%Y %H:%M"),
        "data_atualizacao":  datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    return 201, f"Favoritos criados com sucesso. ID: {fid}"

# ── READ (todos) ─────────────────────────────────────────────
def listar_favoritos():
    if not favoritos:
        return 404, "Nenhum favorito registado."
    return 200, favoritos

# ── READ (por utilizador) ────────────────────────────────────
def obter_favoritos_utilizador(uid):
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    for fav in favoritos.values():
        if fav["idUtilizador"] == uid:
            return 200, fav

    return 404, f"Nenhum favorito encontrado para o utilizador '{uid}'."

# ── UPDATE ───────────────────────────────────────────────────
def remover_conteudo_favorito(uid, cid):
    """Remove um conteudo especifico da lista de favoritos."""
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    for fav in favoritos.values():
        if fav["idUtilizador"] == uid:
            if cid not in fav["lista_ids_Conteudo"]:
                return 404, f"Conteudo '{cid}' nao esta nos favoritos deste utilizador."
            fav["lista_ids_Conteudo"].remove(cid)
            fav["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            return 200, f"Conteudo '{cid}' removido dos favoritos."

    return 404, f"Nenhum favorito encontrado para o utilizador '{uid}'."

# ── DELETE ───────────────────────────────────────────────────
def remover_favoritos_utilizador(uid):
    """Remove todos os favoritos de um utilizador."""
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    for fid, fav in list(favoritos.items()):
        if fav["idUtilizador"] == uid:
            del favoritos[fid]
            return 200, f"Todos os favoritos do utilizador '{uid}' foram removidos."

    return 404, f"Nenhum favorito encontrado para o utilizador '{uid}'."
