# ==============================
# utilizadores.py
# armazena e gere os utilizadores
# retorna tuplos (codigo_http, mensagem)
# ==============================
from utils import gerar_id_utilizador, validar_email, validar_plano, validar_nao_vazio

utilizadores = {}

# ── CREATE ──────────────────────────────────────────────────
def criar_utilizador(nome, email, palavrapasse, tipo_plano):
    # valida campos obrigatorios
    if not validar_nao_vazio(nome):
        return 400, "Nome nao pode estar vazio."
    if not validar_email(email):
        return 400, "Email invalido."
    if not validar_nao_vazio(palavrapasse):
        return 400, "Palavra-passe nao pode estar vazia."
    if not validar_plano(tipo_plano):
        return 400, "Plano invalido. Use 'basic' ou 'premium'."

    # verifica se o email ja existe
    for u in utilizadores.values():
        if u["email"] == email:
            return 409, "Ja existe um utilizador com esse email."

    uid = gerar_id_utilizador()
    utilizadores[uid] = {
        "idUtilizador": uid,
        "nome":         nome.strip(),
        "email":        email.strip(),
        "palavraPasse": palavrapasse.strip(),
        "tipoPlano":    tipo_plano.lower().strip(),
        "estado":       1
    }
    return 201, f"Utilizador '{nome}' criado com sucesso. ID: {uid}"

# ── READ (todos) ─────────────────────────────────────────────
def listar_utilizadores():
    if not utilizadores:
        return 404, "Nenhum utilizador registado."
    return 200, utilizadores

# ── READ (um) ────────────────────────────────────────────────
def obter_utilizador(uid):
    if uid not in utilizadores:
        return 404, f"Utilizador '{uid}' nao encontrado."
    return 200, utilizadores[uid]

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_utilizador(uid, nome=None, email=None, palavrapasse=None, tipo_plano=None, estado=None):
    if uid not in utilizadores:
        return 404, f"Utilizador '{uid}' nao encontrado."

    try:
        # atualiza apenas os campos que foram preenchidos (nao None)
        if nome:        utilizadores[uid]["nome"]        = nome.strip()
        if email:
            if not validar_email(email):
                return 400, "Email invalido."
            utilizadores[uid]["email"]       = email.strip()
        if palavrapasse: utilizadores[uid]["palavraPasse"] = palavrapasse.strip()
        if tipo_plano:
            if not validar_plano(tipo_plano):
                return 400, "Plano invalido. Use 'basic' ou 'premium'."
            utilizadores[uid]["tipoPlano"]   = tipo_plano.lower().strip()
        if estado is not None: utilizadores[uid]["estado"] = estado

        return 200, "Utilizador atualizado com sucesso."
    except Exception as e:
        return 500, str(e)

# ── DELETE ───────────────────────────────────────────────────
def remover_utilizador(uid):
    # retorna 404 se o ID nao existir
    if uid not in utilizadores:
        return 404, f"Utilizador '{uid}' nao encontrado."

    try:
        del utilizadores[uid]
        return 200, f"Utilizador '{uid}' removido com sucesso."
    except Exception as e:
        return 500, str(e)
