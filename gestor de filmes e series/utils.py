# ==============================
# utils.py
# funcoes auxiliares partilhadas
# por todos os outros ficheiros
# ==============================
from datetime import datetime

# contadores globais para gerar IDs unicos automaticamente
contador_utilizadores = 1
contador_conteudos    = 1
contador_historicos   = 1

# gera um ID para utilizador no formato U001, U002, ...
def gerar_id_utilizador():
    global contador_utilizadores
    novo_id = f"U{contador_utilizadores:03d}"
    contador_utilizadores += 1
    return novo_id

# gera um ID para conteudo no formato C001, C002, ...
def gerar_id_conteudo():
    global contador_conteudos
    novo_id = f"C{contador_conteudos:03d}"
    contador_conteudos += 1
    return novo_id

# gera um ID para historico no formato H001, H002, ...
def gerar_id_historico():
    global contador_historicos
    novo_id = f"H{contador_historicos:03d}"
    contador_historicos += 1
    return novo_id

# valida se o email tem formato basico correto (contem @ e . apos o @)
def validar_email(email):
    return "@" in email and "." in email.split("@")[-1]

# valida se o ano esta entre 1888 (primeiro filme da historia) e o ano atual
def validar_ano(ano_texto):
    try:
        ano = int(ano_texto)
        ano_atual = datetime.now().year
        if ano < 1888 or ano > ano_atual:
            return False
        return True
    except ValueError:
        return False

# valida se o progresso esta entre 0 e 100
def validar_progresso(progresso_texto):
    try:
        p = int(progresso_texto)
        return 0 <= p <= 100
    except ValueError:
        return False
        # ── Adiciona estas 2 funcoes ao teu utils.py existente ──────

# contador para favoritos e recomendacoes (junta aos que ja tens)
contador_favoritos     = 1
contador_recomendacoes = 1

# gera um ID para favorito no formato F001, F002, ...
def gerar_id_favorito():
    global contador_favoritos
    novo_id = f"F{contador_favoritos:03d}"
    contador_favoritos += 1
    return novo_id

# gera um ID para recomendacao no formato R001, R002, ...
def gerar_id_recomendacao():
    global contador_recomendacoes
    novo_id = f"R{contador_recomendacoes:03d}"
    contador_recomendacoes += 1
    return novo_id
