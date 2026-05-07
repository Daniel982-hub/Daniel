# ==============================
# recomendacoes.py
# armazena e gere as recomendacoes
# retorna tuplos (codigo_http, mensagem)
#
# Logica automatica diaria:
#   cada utilizador recebe 1 recomendacao
#   por dia de forma automatica
# ==============================
from datetime import datetime
import random
from utils import gerar_id_recomendacao
import utilizadores as bd_utilizadores
import conteudo as bd_conteudo

recomendacoes = {}

# motivos possiveis gerados automaticamente
MOTIVOS_AUTO = [
    "Baseado nas tendencias do dia",
    "Muito popular entre utilizadores com o mesmo plano",
    "Altamente avaliado pela comunidade",
    "Novidade em destaque na plataforma",
    "Escolha do editor",
    "Baseado no genero mais visualizado hoje"
]

# ── helper: calcula score de relevancia ─────────────────────
def _calcular_score(dados_conteudo):
    """Score baseado na avaliacao e numero de avaliadores (0.0 - 10.0)."""
    avaliacao  = dados_conteudo.get("avaliacao", 5.0)
    num_aval   = dados_conteudo.get("numeroAvaliadores", 0)
    bonus      = min(num_aval / 10000, 1.0)   # bonus max de 1.0
    score      = round((avaliacao * 0.9) + bonus, 1)
    return min(score, 10.0)

# ── CREATE (manual) ──────────────────────────────────────────
def criar_recomendacao(uid, cid, motivo=None):
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    codigo_c, dados_c = bd_conteudo.obter_conteudo(cid)
    if codigo_c == 404:
        return 404, f"Conteudo '{cid}' nao encontrado."

    if not motivo or not str(motivo).strip():
        motivo = random.choice(MOTIVOS_AUTO)

    rid   = gerar_id_recomendacao()
    score = _calcular_score(dados_c)

    recomendacoes[rid] = {
        "idRecomendacao":  rid,
        "idUtilizador":    uid,
        "idConteudo":      cid,
        "dataGeracao":     datetime.now().strftime("%d/%m/%Y %H:%M"),
        "scoreRelevancia": score,
        "motivo":          motivo.strip()
    }
    return 201, [rid]

# ── CREATE (automatica diaria) ───────────────────────────────
def gerar_recomendacoes_diarias():
    """
    Percorre todos os utilizadores e gera 1 recomendacao por dia
    para cada um que ainda nao tenha recebido recomendacao hoje.
    """
    codigo_u, utilizadores_data = bd_utilizadores.listar_utilizadores()
    if codigo_u == 404:
        return 404, "Nenhum utilizador registado."

    codigo_c, conteudos_data = bd_conteudo.listar_conteudos()
    if codigo_c == 404:
        return 404, "Nenhum conteudo disponivel para recomendar."

    hoje    = datetime.now().strftime("%d/%m/%Y")
    geradas = 0
    ja_tinham = 0

    lista_conteudos = list(conteudos_data.values())

    for uid in utilizadores_data:
        # verifica se o utilizador ja recebeu recomendacao hoje
        ja_recebeu = any(
            r["idUtilizador"] == uid and r["dataGeracao"].startswith(hoje)
            for r in recomendacoes.values()
        )
        if ja_recebeu:
            ja_tinham += 1
            continue

        # escolhe o conteudo com maior score (com alguma aleatoriedade)
        escolhido = max(lista_conteudos,
                        key=lambda c: _calcular_score(c) + random.uniform(0, 1.5))

        rid   = gerar_id_recomendacao()
        score = _calcular_score(escolhido)

        recomendacoes[rid] = {
            "idRecomendacao":  rid,
            "idUtilizador":    uid,
            "idConteudo":      escolhido["idConteudo"],
            "dataGeracao":     datetime.now().strftime("%d/%m/%Y %H:%M"),
            "scoreRelevancia": score,
            "motivo":          random.choice(MOTIVOS_AUTO)
        }
        geradas += 1

    return 200, f"Recomendacoes diarias geradas: {geradas} | Utilizadores ja com recomendacao hoje: {ja_tinham}"

# ── READ (todas) ─────────────────────────────────────────────
def listar_recomendacoes():
    if not recomendacoes:
        return 404, [rid]
    return 200, recomendacoes

# ── READ (uma por ID) ────────────────────────────────────────
def obter_recomendacao(rid):
    if rid not in recomendacoes:
        return 404, [rid]
    return 200, recomendacoes[rid]

# ── READ (por utilizador) ────────────────────────────────────
def obter_recomendacoes_utilizador(uid):
    codigo, _ = bd_utilizadores.obter_utilizador(uid)
    if codigo == 404:
        return 404, f"Utilizador '{uid}' nao encontrado."

    registos = {rid: r for rid, r in recomendacoes.items() if r["idUtilizador"] == uid}
    if not registos:
        return 404, [rid]
    return 200, registos

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_recomendacao(rid, motivo=None, score_relevancia=None):
    if rid not in recomendacoes:
        return 404, f"Recomendacao '{rid}' nao encontrada."

    try:
        if motivo and str(motivo).strip():
            recomendacoes[rid]["motivo"] = motivo.strip()

        if score_relevancia is not None:
            score = round(float(score_relevancia), 1)
            if not (0.0 <= score <= 10.0):
                return 400, "Score invalido. Use um valor entre 0 e 10."
            recomendacoes[rid]["scoreRelevancia"] = score

        return 200, [rid]
    except Exception as e:
        return 500, str(e)

# ── DELETE ───────────────────────────────────────────────────
def remover_recomendacao(rid):
    if rid not in recomendacoes:
        return 404, [rid]
    try:
        del recomendacoes[rid]
        return 200, [rid]
    except Exception as e:
        return 500, str(e)
