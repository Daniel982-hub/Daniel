# ==============================
# recomendacoes.py
# armazena e gere as recomendacoes
# retorna tuplos (codigo_http, mensagem)
# ==============================
import json, os
from datetime import datetime
import random
from utils import gerar_id_recomendacao
import utilizadores as bd_utilizadores
import conteudo as bd_conteudo

FICHEIRO = "recomendacoes.json"
recomendacoes = {}

MOTIVOS_AUTO = [
    "Baseado nas tendencias do dia",
    "Muito popular entre utilizadores com o mesmo plano",
    "Altamente avaliado pela comunidade",
    "Novidade em destaque na plataforma",
    "Escolha do editor",
    "Baseado no genero mais visualizado hoje"
]

def guardar():
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(recomendacoes, f, indent=4, ensure_ascii=False)

def carregar():
    global recomendacoes
    if os.path.exists(FICHEIRO):
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            recomendacoes = json.load(f)
    else:
        recomendacoes = {}

def _calcular_score(dados_conteudo):
    avaliacao = dados_conteudo.get("avaliacao", 5.0)
    bonus     = min(dados_conteudo.get("numeroAvaliadores", 0) / 10000, 1.0)
    return min(round((avaliacao * 0.9) + bonus, 1), 10.0)

# ── CREATE ──────────────────────────────────────────────────
def criar_recomendacao(uid, cid, motivo=None):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    codigo_c, dados_c = bd_conteudo.obter_conteudo(cid)
    if codigo_c == 404:
        return 404, f"Conteudo '{cid}' nao encontrado."
    if not motivo or not str(motivo).strip():
        motivo = random.choice(MOTIVOS_AUTO)

    rid = gerar_id_recomendacao()
    recomendacoes[rid] = {
        "idRecomendacao":  rid,
        "idUtilizador":    uid,
        "idConteudo":      cid,
        "dataGeracao":     datetime.now().strftime("%d/%m/%Y %H:%M"),
        "scoreRelevancia": _calcular_score(dados_c),
        "motivo":          motivo.strip()
    }
    guardar()
    return 201, rid

# ── READ (todas) ─────────────────────────────────────────────
def listar_recomendacoes():
    carregar()
    if not recomendacoes:
        return 404, "Nenhuma recomendacao registada."
    return 200, recomendacoes

# ── READ (uma) ───────────────────────────────────────────────
def obter_recomendacao(rid):
    carregar()
    if rid not in recomendacoes:
        return 404, f"Recomendacao '{rid}' nao encontrada."
    return 200, rid

# ── READ (por utilizador) ────────────────────────────────────
def obter_recomendacoes_utilizador(uid):
    carregar()
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."
    registos = [rid for rid, r in recomendacoes.items() if r["idUtilizador"] == uid]
    if not registos:
        return 404, f"Nenhuma recomendacao encontrada para o utilizador '{uid}'."
    return 200, registos

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_recomendacao(rid, motivo=None, score_relevancia=None):
    carregar()
    if rid not in recomendacoes:
        return 404, f"Recomendacao '{rid}' nao encontrada."
    if motivo and str(motivo).strip():
        recomendacoes[rid]["motivo"] = motivo.strip()
    if score_relevancia is not None:
        score = round(float(score_relevancia), 1)
        if not (0.0 <= score <= 10.0):
            return 400, "Score invalido. Use um valor entre 0 e 10."
        recomendacoes[rid]["scoreRelevancia"] = score
    guardar()
    return 200, rid

# ── DELETE ───────────────────────────────────────────────────
def remover_recomendacao(rid):
    carregar()
    if rid not in recomendacoes:
        return 404, f"Recomendacao '{rid}' nao encontrada."
    del recomendacoes[rid]
    guardar()
    return 200, rid
