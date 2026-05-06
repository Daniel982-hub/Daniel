# ==============================
# conteudos.py
# CRUD da entidade Conteudo
# armazenamento em dicionario
# validacoes feitas aqui (nao no main)
# retorna codigos de estado ao estilo HTTP
# ==============================
from utils import gerar_id_conteudo, validar_ano

# tipos de conteudo aceites
TIPOS_VALIDOS = ["filme", "serie"]

# classificacoes etarias aceites
CLASSIFICACOES_VALIDAS = ["g", "pg", "pg-13", "m/12", "m/16", "m/18"]

# dicionario principal onde ficam guardados todos os conteudos
# chave: ID gerado automaticamente (ex: C001)
# valor: dicionario com os dados do conteudo
conteudos = {}

# ── CREATE ───────────────────────────────────────────────────────────────────
def criar_conteudo(titulo, tipo, genero, anoLancamento, classificacaoEtaria,
                   avaliacao, numeroAvaliadores, duracao_ou_temporadas, produtor, realizador):

    # valida o tipo
    if tipo.lower() not in TIPOS_VALIDOS:
        return 400, f"Tipo invalido. Escolha: {', '.join(TIPOS_VALIDOS)}"

    # valida o ano de lancamento
    if not validar_ano(anoLancamento):
        return 400, "Ano de lancamento invalido. Deve ser um ano entre 1888 e o ano atual."

    # valida a classificacao etaria
    if classificacaoEtaria.lower() not in CLASSIFICACOES_VALIDAS:
        return 400, f"Classificacao invalida. Escolha: {', '.join(CLASSIFICACOES_VALIDAS)}"

    # valida a avaliacao (0.0 a 10.0)
    try:
        avaliacao = float(avaliacao)
        if avaliacao < 0.0 or avaliacao > 10.0:
            return 400, "Avaliacao invalida. Deve ser um valor entre 0.0 e 10.0."
    except ValueError:
        return 400, "Avaliacao invalida. Introduz um numero entre 0.0 e 10.0."

    # valida numero de avaliadores
    try:
        numeroAvaliadores = int(numeroAvaliadores)
        if numeroAvaliadores < 0:
            return 400, "Numero de avaliadores invalido. Deve ser um inteiro positivo."
    except ValueError:
        return 400, "Numero de avaliadores invalido. Introduz um numero inteiro."

    # valida duracao (filme em minutos) ou numero de temporadas (serie)
    try:
        duracao_ou_temporadas = int(duracao_ou_temporadas)
        if duracao_ou_temporadas <= 0:
            return 400, "Valor invalido. Deve ser um inteiro positivo."
    except ValueError:
        return 400, "Valor invalido. Introduz um numero inteiro."

    try:
        cid = gerar_id_conteudo()
        dados = {
            "titulo":              titulo,
            "tipo":                tipo.lower(),
            "genero":              genero,
            "anoLancamento":       int(anoLancamento),
            "classificacaoEtaria": classificacaoEtaria.lower(),
            "avaliacao":           avaliacao,
            "numeroAvaliadores":   numeroAvaliadores,
            "produtor":            produtor,
            "realizador":          realizador
        }
        # campo especifico conforme o tipo
        if tipo.lower() == "filme":
            dados["duracao"] = duracao_ou_temporadas          # minutos
        else:
            dados["numeroTemporadas"] = duracao_ou_temporadas

        conteudos[cid] = dados
        return 201, cid
    except Exception as e:
        return 500, str(e)

# ── READ - listar todos ──────────────────────────────────────────────────────
def listar_conteudos():
    if not conteudos:
        return 404, "Nao existem conteudos registados."

    try:
        for cid, d in conteudos.items():
            if d["tipo"] == "filme":
                extra = f"Duracao: {d.get('duracao', '?')} min"
            else:
                extra = f"Temporadas: {d.get('numeroTemporadas', '?')}"
            print(f"  ID: {cid} | {d['titulo']} ({d['tipo'].capitalize()}) | "
                  f"Genero: {d['genero']} | Ano: {d['anoLancamento']} | "
                  f"Avaliacao: {d['avaliacao']}/10 | {extra}")
        return 200, "Conteudos listados com sucesso."
    except Exception as e:
        return 500, str(e)

# ── READ - consultar individual ──────────────────────────────────────────────
def consultar_conteudo(cid):
    # retorna 404 se o ID nao existir
    if cid not in conteudos:
        return 404, "Conteudo nao encontrado."

    try:
        return 200, conteudos[cid]
    except Exception as e:
        return 500, str(e)

# ── UPDATE ───────────────────────────────────────────────────────────────────
def atualizar_conteudo(cid, titulo, genero, anoLancamento, classificacaoEtaria,
                       avaliacao, numeroAvaliadores, duracao_ou_temporadas, produtor, realizador):
    # retorna 404 se o ID nao existir
    if cid not in conteudos:
        return 404, "Conteudo nao encontrado."

    # valida os campos opcionais que foram preenchidos
    if anoLancamento and not validar_ano(anoLancamento):
        return 400, "Ano de lancamento invalido."

    if classificacaoEtaria and classificacaoEtaria.lower() not in CLASSIFICACOES_VALIDAS:
        return 400, f"Classificacao invalida. Escolha: {', '.join(CLASSIFICACOES_VALIDAS)}"

    if avaliacao:
        try:
            avaliacao = float(avaliacao)
            if avaliacao < 0.0 or avaliacao > 10.0:
                return 400, "Avaliacao invalida. Deve ser entre 0.0 e 10.0."
        except ValueError:
            return 400, "Avaliacao invalida."

    if numeroAvaliadores:
        try:
            numeroAvaliadores = int(numeroAvaliadores)
        except ValueError:
            return 400, "Numero de avaliadores invalido."

    if duracao_ou_temporadas:
        try:
            duracao_ou_temporadas = int(duracao_ou_temporadas)
            if duracao_ou_temporadas <= 0:
                return 400, "Valor invalido. Deve ser um inteiro positivo."
        except ValueError:
            return 400, "Valor invalido. Introduz um numero inteiro."

    try:
        # atualiza os campos que foram preenchidos (nao None)
        if titulo:               conteudos[cid]["titulo"]              = titulo
        if genero:               conteudos[cid]["genero"]              = genero
        if anoLancamento:        conteudos[cid]["anoLancamento"]       = int(anoLancamento)
        if classificacaoEtaria:  conteudos[cid]["classificacaoEtaria"] = classificacaoEtaria.lower()
        if avaliacao:            conteudos[cid]["avaliacao"]           = avaliacao
        if numeroAvaliadores:    conteudos[cid]["numeroAvaliadores"]   = numeroAvaliadores
        if duracao_ou_temporadas:
            campo = "duracao" if conteudos[cid]["tipo"] == "filme" else "numeroTemporadas"
            conteudos[cid][campo] = duracao_ou_temporadas
        if produtor:             conteudos[cid]["produtor"]            = produtor
        if realizador:           conteudos[cid]["realizador"]          = realizador

        return 200, "Conteudo atualizado com sucesso."
    except Exception as e:
        return 500, str(e)

# ── DELETE ───────────────────────────────────────────────────────────────────
def remover_conteudo(cid):
    # retorna 404 se o ID nao existir
    if cid not in conteudos:
        return 404, "Conteudo nao encontrado."

    try:
        del conteudos[cid]
        return 200, "Conteudo removido com sucesso."
    except Exception as e:
        return 500, str(e)