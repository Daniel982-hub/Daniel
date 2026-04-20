# ==============================
# utils.py
# funcoes auxiliares partilhadas
# por todos os outros ficheiros
# ==============================
from datetime import datetime

# contadores globais para gerar IDs unicos automaticamente
contador_utilizadores = 1
contador_conteudos    = 1
contador_historico    = 1

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
    global contador_historico
    novo_id = f"H{contador_historico:03d}"
    contador_historico += 1
    return novo_id

# valida se o email tem formato basico correto (contem @ e . apos o @)
def validar_email(email):
    return "@" in email and "." in email.split("@")[-1]

# valida se o ano esta entre 1888 e o ano atual
def validar_ano(ano_texto):
    try:
        ano = int(ano_texto)
        ano_atual = datetime.now().year
        if ano < 1888 or ano > ano_atual:
            return False
        return True
    except ValueError:
        return False

# valida se a avaliacao esta entre 0.0 e 10.0
def validar_avaliacao(valor_texto):
    try:
        v = float(valor_texto)
        return 0.0 <= v <= 10.0
    except ValueError:
        return False

# valida se o progresso esta entre 0 e 100
def validar_progresso(valor_texto):
    try:
        v = float(valor_texto)
        return 0.0 <= v <= 100.0
    except ValueError:
        return False

# valida se o plano e basic ou premium
def validar_plano(plano):
    return plano.lower() in ["basic", "premium"]

# valida se o tipo e filme ou serie
def validar_tipo(tipo):
    return tipo.lower() in ["filme", "série", "serie"]

# valida se a string nao esta vazia
def validar_nao_vazio(valor):
    return bool(valor.strip())
