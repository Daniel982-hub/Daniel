# ==============================
# conteudo.py
# armazena e gere os conteudos
# retorna tuplos (codigo_http, mensagem)
# ==============================
import json, os
from utils import gerar_id_conteudo, validar_nao_vazio, validar_tipo, validar_ano, validar_avaliacao

FICHEIRO = "conteudos.json"
conteudos = {}

def guardar():
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(conteudos, f, indent=4, ensure_ascii=False)

def carregar():
    global conteudos
    if os.path.exists(FICHEIRO):
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            conteudos = json.load(f)
    else:
        conteudos = {}

# ── CREATE ──────────────────────────────────────────────────
def criar_conteudo(titulo, tipo, genero, ano_lancamento, classificacao_etaria,
                   avaliacao, numero_avaliadores, produtor, realizador,
                   duracao=0, numero_temporadas=0):
    carregar()
    if not validar_nao_vazio(titulo):
        return 400, "Titulo nao pode estar vazio."
    if not validar_tipo(tipo):
        return 400, "Tipo invalido. Use 'filme' ou 'serie'."
    if not validar_nao_vazio(genero):
        return 400, "Genero nao pode estar vazio."
    if not validar_ano(str(ano_lancamento)):
        return 400, "Ano de lancamento invalido."
    if not validar_nao_vazio(classificacao_etaria):
        return 400, "Classificacao etaria nao pode estar vazia."
    if not validar_avaliacao(str(avaliacao)):
        return 400, "Avaliacao invalida. Use um valor entre 0 e 10."
    if not validar_nao_vazio(produtor):
        return 400, "Produtor nao pode estar vazio."
    if not validar_nao_vazio(realizador):
        return 400, "Realizador nao pode estar vazio."

    cid = gerar_id_conteudo()
    conteudos[cid] = {
        "idConteudo":          cid,
        "titulo":              titulo.strip(),
        "tipo":                tipo.lower().strip(),
        "genero":              genero.strip(),
        "anoLancamento":       int(ano_lancamento),
        "classificacaoEtaria": classificacao_etaria.strip(),
        "avaliacao":           round(float(avaliacao), 1),
        "numeroAvaliadores":   int(numero_avaliadores),
        "duracao":             int(duracao),
        "numeroTemporadas":    int(numero_temporadas),
        "produtor":            produtor.strip(),
        "realizador":          realizador.strip()
    }
    guardar()
    return 201, cid

# ── READ (todos) ─────────────────────────────────────────────
def listar_conteudos():
    carregar()
    if not conteudos:
        return 404, "Nenhum conteudo registado."
    return 200, conteudos

# ── READ (um) ────────────────────────────────────────────────
def obter_conteudo(cid):
    carregar()
    if cid not in conteudos:
        return 404, f"Conteudo '{cid}' nao encontrado."
    return 200, cid

# ── UPDATE ───────────────────────────────────────────────────
def atualizar_conteudo(cid, titulo=None, tipo=None, genero=None, ano_lancamento=None,
                        classificacao_etaria=None, avaliacao=None, numero_avaliadores=None,
                        duracao=None, numero_temporadas=None, produtor=None, realizador=None):
    carregar()
    if cid not in conteudos:
        return 404, f"Conteudo '{cid}' nao encontrado."
    if titulo:               conteudos[cid]["titulo"]              = titulo.strip()
    if tipo:
        if not validar_tipo(tipo):
            return 400, "Tipo invalido. Use 'filme' ou 'serie'."
        conteudos[cid]["tipo"]                = tipo.lower().strip()
    if genero:               conteudos[cid]["genero"]              = genero.strip()
    if ano_lancamento:
        if not validar_ano(str(ano_lancamento)):
            return 400, "Ano de lancamento invalido."
        conteudos[cid]["anoLancamento"]       = int(ano_lancamento)
    if classificacao_etaria: conteudos[cid]["classificacaoEtaria"] = classificacao_etaria.strip()
    if avaliacao is not None:
        if not validar_avaliacao(str(avaliacao)):
            return 400, "Avaliacao invalida. Use um valor entre 0 e 10."
        conteudos[cid]["avaliacao"]           = round(float(avaliacao), 1)
    if numero_avaliadores:   conteudos[cid]["numeroAvaliadores"]   = int(numero_avaliadores)
    if duracao is not None:  conteudos[cid]["duracao"]             = int(duracao)
    if numero_temporadas is not None: conteudos[cid]["numeroTemporadas"] = int(numero_temporadas)
    if produtor:             conteudos[cid]["produtor"]            = produtor.strip()
    if realizador:           conteudos[cid]["realizador"]          = realizador.strip()
    guardar()
    return 200, cid

# ── DELETE ───────────────────────────────────────────────────
def remover_conteudo(cid):
    carregar()
    if cid not in conteudos:
        return 404, f"Conteudo '{cid}' nao encontrado."
    del conteudos[cid]
    guardar()
    return 200, cid
