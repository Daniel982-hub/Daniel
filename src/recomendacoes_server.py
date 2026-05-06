# ======================================================
# recomendacoes_server.py
# servidor HTTP para as Recomendacoes — porta 8001
#
# Corre num terminal SEPARADO:
#   Terminal 1 -> python main.py
#   Terminal 2 -> python recomendacoes_server.py
#
# Logica de recomendacao:
#   verifica os favoritos do utilizador e recomenda
#   um conteudo com base nos generos favoritos.
#   Se nao tiver favoritos, recomenda por score global.
#
# Endpoints:
#   GET    /recomendacoes
#   GET    /recomendacoes/<rid>
#   GET    /recomendacoes/utilizador/<uid>
#   POST   /recomendacoes                  -> cria manual
#   POST   /recomendacoes/diarias          -> gera automaticas
#   PUT    /recomendacoes/<rid>
#   DELETE /recomendacoes/<rid>
# ======================================================
import sys, os, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import utilizadores  as bd_utilizadores
import conteudo      as bd_conteudo
import favoritos     as bd_favoritos
import recomendacoes as bd_rec

HOST = "localhost"
PORT = 8001

# ── helpers ─────────────────────────────────────────────────
def enviar_json(handler, codigo_http, dados):
    corpo = json.dumps(dados, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(codigo_http)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(corpo)))
    handler.end_headers()
    handler.wfile.write(corpo)

def ler_json(handler):
    tamanho = int(handler.headers.get("Content-Length", 0))
    if tamanho == 0:
        return {}
    try:
        return json.loads(handler.rfile.read(tamanho).decode("utf-8"))
    except json.JSONDecodeError:
        return None

def recomendar_por_favoritos(uid):
    """
    Verifica os favoritos do utilizador e recomenda um conteudo
    do mesmo genero dos que tem nos favoritos.
    Se nao tiver favoritos, recomenda pelo score global.
    """
    import random

    # obtem todos os conteudos disponiveis
    codigo_c, conteudos_data = bd_conteudo.listar_conteudos()
    if codigo_c == 404:
        return None, "Nenhum conteudo disponivel."

    lista_conteudos = list(conteudos_data.values())

    # verifica se o utilizador tem favoritos
    codigo_f, fav_data = bd_favoritos.obter_favoritos_utilizador(uid)

    if codigo_f == 200:
        # recolhe os generos dos conteudos favoritos
        ids_favoritos = fav_data.get("lista_ids_Conteudo", [])
        generos_favoritos = set()
        for cid in ids_favoritos:
            c_codigo, c_dados = bd_conteudo.obter_conteudo(cid)
            if c_codigo == 200:
                generos_favoritos.add(c_dados.get("genero", "").lower())

        # filtra conteudos do mesmo genero que nao estejam ja nos favoritos
        candidatos = [
            c for c in lista_conteudos
            if c.get("genero", "").lower() in generos_favoritos
            and c["idConteudo"] not in ids_favoritos
        ]

        if candidatos:
            # escolhe o de maior avaliacao entre os candidatos
            escolhido = max(candidatos, key=lambda c: c.get("avaliacao", 0))
            motivo = f"Baseado nos seus favoritos do genero '{escolhido.get('genero')}'"
            return escolhido, motivo

    # fallback: sem favoritos ou sem candidatos -> recomenda pelo score global
    escolhido = max(lista_conteudos, key=lambda c: c.get("avaliacao", 0) + random.uniform(0, 0.5))
    motivo = "Tendencia popular na plataforma"
    return escolhido, motivo

def popular_dados_exemplo():
    bd_utilizadores.criar_utilizador("Ana Silva",  "ana@email.com",  "pass123", "premium")
    bd_utilizadores.criar_utilizador("Rui Costa",  "rui@email.com",  "pass456", "basic")
    bd_conteudo.criar_conteudo("Inception",    "filme",  "Ficcao Cientifica", 2010, "M/12", 8.8, 2500000, "Emma Thomas",  "Christopher Nolan", duracao=148)
    bd_conteudo.criar_conteudo("Interstellar", "filme",  "Ficcao Cientifica", 2014, "M/12", 8.6, 1900000, "Emma Thomas",  "Christopher Nolan", duracao=169)
    bd_conteudo.criar_conteudo("Breaking Bad", "serie",  "Drama",             2008, "M/18", 9.5, 1800000, "Mark Johnson", "Vince Gilligan",    numero_temporadas=5)
    bd_conteudo.criar_conteudo("Ozark",        "serie",  "Drama",             2017, "M/16", 8.4,  900000, "Chris Mundy",  "Jason Bateman",     numero_temporadas=4)
    # Ana tem favoritos de Ficcao Cientifica
    bd_favoritos.adicionar_favorito("U001", "C001")
    print("[INFO] Dados de exemplo carregados.")
    print("[INFO] U001=Ana (favorito: Inception/Ficcao Cientifica), U002=Rui (sem favoritos)")

# ── handler HTTP ─────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  [{self.command}] {self.path}  ->  {args[1] if len(args) > 1 else '?'}")

    def _partes(self):
        return [p for p in urlparse(self.path).path.strip("/").split("/") if p]

    # ── GET ─────────────────────────────────────────────────
    def do_GET(self):
        p = self._partes()

        # GET /recomendacoes
        if p == ["recomendacoes"]:
            codigo, dados = bd_rec.listar_recomendacoes()
            enviar_json(self, codigo, dados if isinstance(dados, dict) else {"mensagem": dados})

        # GET /recomendacoes/utilizador/<uid>
        elif len(p) == 3 and p[:2] == ["recomendacoes", "utilizador"]:
            codigo, dados = bd_rec.obter_recomendacoes_utilizador(p[2])
            enviar_json(self, codigo, dados if isinstance(dados, dict) else {"mensagem": dados})

        # GET /recomendacoes/<rid>
        elif len(p) == 2 and p[0] == "recomendacoes":
            codigo, dados = bd_rec.obter_recomendacao(p[1])
            enviar_json(self, codigo, dados if isinstance(dados, dict) else {"mensagem": dados})

        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado."})

    # ── POST ────────────────────────────────────────────────
    def do_POST(self):
        p = self._partes()

        # POST /recomendacoes/diarias -> gera automaticamente com base em favoritos
        if p == ["recomendacoes", "diarias"]:
            codigo_u, utilizadores_data = bd_utilizadores.listar_utilizadores()
            if codigo_u == 404:
                enviar_json(self, 404, {"mensagem": "Nenhum utilizador registado."})
                return

            from datetime import datetime
            hoje = datetime.now().strftime("%d/%m/%Y")
            geradas = []
            ignoradas = 0

            for uid in utilizadores_data:
                ja_recebeu = any(
                    r["idUtilizador"] == uid and r["dataGeracao"].startswith(hoje)
                    for r in bd_rec.recomendacoes.values()
                )
                if ja_recebeu:
                    ignoradas += 1
                    continue

                conteudo_escolhido, motivo = recomendar_por_favoritos(uid)
                if conteudo_escolhido is None:
                    continue

                codigo_r, rec = bd_rec.criar_recomendacao(uid, conteudo_escolhido["idConteudo"], motivo)
                if codigo_r == 201:
                    geradas.append(rec)

            enviar_json(self, 200, {
                "geradas": len(geradas),
                "ignoradas_ja_tinham_hoje": ignoradas,
                "recomendacoes": geradas
            })

        # POST /recomendacoes -> cria manualmente
        elif p == ["recomendacoes"]:
            corpo = ler_json(self)
            if corpo is None:
                enviar_json(self, 400, {"mensagem": "JSON invalido."})
                return
            uid    = corpo.get("idUtilizador", "")
            cid    = corpo.get("idConteudo", "")
            motivo = corpo.get("motivo", "")
            if not uid or not cid:
                enviar_json(self, 400, {"mensagem": "idUtilizador e idConteudo sao obrigatorios."})
                return
            codigo, dados = bd_rec.criar_recomendacao(uid, cid, motivo or None)
            enviar_json(self, codigo, dados if isinstance(dados, dict) else {"mensagem": dados})

        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado."})

    # ── PUT ─────────────────────────────────────────────────
    def do_PUT(self):
        p = self._partes()

        # PUT /recomendacoes/<rid>
        if len(p) == 2 and p[0] == "recomendacoes":
            corpo = ler_json(self)
            if corpo is None:
                enviar_json(self, 400, {"mensagem": "JSON invalido."})
                return
            motivo = corpo.get("motivo", None)
            score  = corpo.get("scoreRelevancia", None)
            codigo, dados = bd_rec.atualizar_recomendacao(p[1], motivo, score)
            enviar_json(self, codigo, dados if isinstance(dados, dict) else {"mensagem": dados})

        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado."})

    # ── DELETE ──────────────────────────────────────────────
    def do_DELETE(self):
        p = self._partes()

        # DELETE /recomendacoes/<rid>
        if len(p) == 2 and p[0] == "recomendacoes":
            codigo, dados = bd_rec.remover_recomendacao(p[1])
            enviar_json(self, codigo, {"mensagem": dados})

        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado."})


# ── arranque ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  SERVIDOR DE RECOMENDACOES — http://localhost:8001")
    print("=" * 55)
    popular_dados_exemplo()
    print("\nEndpoints:")
    print("  GET    /recomendacoes")
    print("  GET    /recomendacoes/<rid>")
    print("  GET    /recomendacoes/utilizador/<uid>")
    print("  POST   /recomendacoes          {idUtilizador, idConteudo, motivo?}")
    print("  POST   /recomendacoes/diarias  (gera com base em favoritos)")
    print("  PUT    /recomendacoes/<rid>    {motivo?, scoreRelevancia?}")
    print("  DELETE /recomendacoes/<rid>")
    print("\nPrime CTRL+C para parar.\n")

    servidor = HTTPServer((HOST, PORT), Handler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Servidor parado.")
        servidor.server_close()
