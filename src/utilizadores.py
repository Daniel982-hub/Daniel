# ==============================
# utilizadores.py
# CRUD da entidade Utilizador
# armazenamento em dicionario
# validacoes feitas aqui (nao no main)
# retorna codigos de estado ao estilo HTTP
# ==============================
from utils import gerar_id_utilizador, validar_email

# tipos de plano aceites
TIPOS_PLANO_VALIDOS = ["basico", "standard", "premium"]

# estados aceites
ESTADOS_VALIDOS = ["ativo", "inativo", "suspenso"]

# dicionario principal onde ficam guardados todos os utilizadores
# chave: ID gerado automaticamente (ex: U001)
# valor: dicionario com os dados do utilizador
utilizadores = {}

# ── CREATE ───────────────────────────────────────────────────────────────────
def criar_utilizador(nome, email, palavraPasse, tipoPlan, estado):

    # valida o email
    if not validar_email(email):
        return 400, "Email invalido. Deve conter '@' e '.' apos o '@'."

    # verifica se o email ja esta em uso
    for u in utilizadores.values():
        if u["email"] == email:
            return 400, "Ja existe um utilizador com esse email."

    # valida o tipo de plano
    if tipoPlan.lower() not in TIPOS_PLANO_VALIDOS:
        return 400, f"Tipo de plano invalido. Escolha: {', '.join(TIPOS_PLANO_VALIDOS)}"

    # valida o estado
    if estado.lower() not in ESTADOS_VALIDOS:
        return 400, f"Estado invalido. Escolha: {', '.join(ESTADOS_VALIDOS)}"

    # valida a password (minimo 6 caracteres)
    if len(palavraPasse) < 6:
        return 400, "Password invalida. Deve ter pelo menos 6 caracteres."

    try:
        uid = gerar_id_utilizador()
        utilizadores[uid] = {
            "nome":        nome,
            "email":       email,
            "palavraPasse": palavraPasse,
            "tipoPlan":    tipoPlan.lower(),   # guarda sempre em minusculas
            "estado":      estado.lower()
        }
        return 201, utilizadores[uid]
    except Exception as e:
        return 500, str(e)

# ── READ - listar todos ──────────────────────────────────────────────────────
def listar_utilizadores():
    if not utilizadores:
        return 404, "Nao existem utilizadores registados."

    try:
        return 200, utilizadores
    except Exception as e:
        return 500, str(e)

# ── READ - consultar individual ──────────────────────────────────────────────
def consultar_utilizador(uid):
    # retorna 404 se o ID nao existir
    if uid not in utilizadores:
        return 404, "Utilizador nao encontrado."

    try:
        return 200, utilizadores[uid]
    except Exception as e:
        return 500, str(e)

# ── UPDATE ───────────────────────────────────────────────────────────────────
def atualizar_utilizador(uid, nome, email, palavraPasse, tipoPlan, estado):
    # retorna 404 se o ID nao existir
    if uid not in utilizadores:
        return 404, "Utilizador nao encontrado."

    # valida os campos opcionais que foram preenchidos
    if email and not validar_email(email):
        return 400, "Email invalido."

    if email:
        for oid, u in utilizadores.items():
            if u["email"] == email and oid != uid:
                return 400, "Ja existe um utilizador com esse email."

    if tipoPlan and tipoPlan.lower() not in TIPOS_PLANO_VALIDOS:
        return 400, f"Tipo de plano invalido. Escolha: {', '.join(TIPOS_PLANO_VALIDOS)}"

    if estado and estado.lower() not in ESTADOS_VALIDOS:
        return 400, f"Estado invalido. Escolha: {', '.join(ESTADOS_VALIDOS)}"

    if palavraPasse and len(palavraPasse) < 6:
        return 400, "Password invalida. Deve ter pelo menos 6 caracteres."

    try:
        # atualiza os campos que foram preenchidos (nao None)
        if nome:         utilizadores[uid]["nome"]        = nome
        if email:        utilizadores[uid]["email"]       = email
        if palavraPasse: utilizadores[uid]["palavraPasse"] = palavraPasse
        if tipoPlan:     utilizadores[uid]["tipoPlan"]    = tipoPlan.lower()
        if estado:       utilizadores[uid]["estado"]      = estado.lower()

        return 200, "Utilizador atualizado com sucesso."
    except Exception as e:
        return 500, str(e)

# ── DELETE ───────────────────────────────────────────────────────────────────
def remover_utilizador(uid):
    # retorna 404 se o ID nao existir
    if uid not in utilizadores:
        return 404, "Utilizador nao encontrado."

    try:
        del utilizadores[uid]
        return 200, "Utilizador removido com sucesso."
    except Exception as e:
        return 500, str(e)