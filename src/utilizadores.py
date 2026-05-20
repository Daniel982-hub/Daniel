# ==============================
# utilizadores.py
# armazena e gere os utilizadores
# retorna tuplos (codigo_http, mensagem)
# ==============================
import json, os
from utils import gerar_id_utilizador, validar_email, validar_plano, validar_nao_vazio

FICHEIRO = "utilizadores.json"
utilizadores = {}

def guardar():
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(utilizadores, f, indent=4, ensure_ascii=False)

def carregar():
    global utilizadores
    if os.path.exists(FICHEIRO):
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            utilizadores = json.load(f)
    else:
        utilizadores = {}

# ── CREATE ──────────────────────────────────────────────────
def criar_utilizador(nome, email, palavrapasse, tipo_plano):
    carregar()
    if not validar_nao_vazio(nome):
        return 400, "Nome nao pode estar vazio."
    if not validar_email(email):
        return 400, "Email invalido."
    if not validar_nao_vazio(palavrapasse):
        return 400, "Palavra-passe nao pode estar vazia."
    if not validar_plano(tipo_plano):
        return 400, "Plano invalido. Use 'basic' ou 'premium'."
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
    guardar()
    return 201, uid

# ── READ (todos) ─────────────────────────────────────────────
def listar_utilizadores():
    carregar()
    if not utilizadores:
        return 404, "Nenhum utilizador registado."
    return 200, utilizadores

# ── READ (um) ────────────────────────────────────────────────
def obter_utilizador(uid):
    carregar()
    if uid not in utilizadores:
        return 404, f"Utilizador '{uid}' nao encontrado."
    return 200, uid

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_utilizador(uid, nome=None, email=None, palavrapasse=None, tipo_plano=None, estado=None):
    carregar()
    if uid not in utilizadores:
        return 404, f"Utilizador '{uid}' nao encontrado."
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
    guardar()
    return 200, uid

# ── DELETE ───────────────────────────────────────────────────
def remover_utilizador(uid):
    carregar()
    if uid not in utilizadores:
        return 404, f"Utilizador '{uid}' nao encontrado."
    del utilizadores[uid]
    guardar()
    return 200, uid
