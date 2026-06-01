# ==============================
# utilizadores.py
# armazena e gere os utilizadores
# retorna tuplos (codigo_http, mensagem)
# ==============================
import json, os, logging
from utils import gerar_id_utilizador, validar_email, validar_plano, validar_nao_vazio

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        logging.warning(f"Tentativa de criar utilizador com nome vazio.")
        return 400, "Nome nao pode estar vazio."
    if not validar_email(email):
        logging.warning(f"Tentativa de criar utilizador com email invalido: '{email}'.")
        return 400, "Email invalido."
    if not validar_nao_vazio(palavrapasse):
        logging.warning(f"Tentativa de criar utilizador sem palavra-passe.")
        return 400, "Palavra-passe nao pode estar vazia."
    if not validar_plano(tipo_plano):
        logging.warning(f"Tentativa de criar utilizador com plano invalido: '{tipo_plano}'.")
        return 400, "Plano invalido. Use 'basic' ou 'premium'."
    for u in utilizadores.values():
        if u["email"] == email:
            logging.warning(f"Tentativa de criar conta com email duplicado: '{email}'.")
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
    logging.info(f"Conta criada com sucesso: '{uid}' ({email}).")
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
        logging.warning(f"Utilizador nao encontrado: '{uid}'.")
        return 404, f"Utilizador '{uid}' nao encontrado."
    return 200, uid

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_utilizador(uid, nome=None, email=None, palavrapasse=None, tipo_plano=None, estado=None):
    carregar()
    if uid not in utilizadores:
        logging.warning(f"Tentativa de atualizar utilizador inexistente: '{uid}'.")
        return 404, f"Utilizador '{uid}' nao encontrado."
    if nome:        utilizadores[uid]["nome"]        = nome.strip()
    if email:
        if not validar_email(email):
            logging.warning(f"Email invalido na atualizacao do utilizador '{uid}': '{email}'.")
            return 400, "Email invalido."
        utilizadores[uid]["email"]       = email.strip()
    if palavrapasse: utilizadores[uid]["palavraPasse"] = palavrapasse.strip()
    if tipo_plano:
        if not validar_plano(tipo_plano):
            logging.warning(f"Plano invalido na atualizacao do utilizador '{uid}': '{tipo_plano}'.")
            return 400, "Plano invalido. Use 'basic' ou 'premium'."
        utilizadores[uid]["tipoPlano"]   = tipo_plano.lower().strip()
    if estado is not None: utilizadores[uid]["estado"] = estado
    guardar()
    logging.info(f"Utilizador '{uid}' atualizado com sucesso.")
    return 200, uid

# ── DELETE ───────────────────────────────────────────────────
def remover_utilizador(uid):
    carregar()
    if uid not in utilizadores:
        logging.warning(f"Tentativa de remover utilizador inexistente: '{uid}'.")
        return 404, f"Utilizador '{uid}' nao encontrado."
    del utilizadores[uid]
    guardar()
    logging.info(f"Utilizador '{uid}' removido com sucesso.")
    return 200, uid
