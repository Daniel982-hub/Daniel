# ======================================================
# recomendacoes_server.py
# servidor HTTP para as Recomendacoes — porta 8001
#
# Corre num terminal SEPARADO:
#   Terminal 1 -> python main.py
#   Terminal 2 -> python recomendacoes_server.py
# Endpoints:
#   GET    /recomendacoes
#   GET    /recomendacoes/<rid>
#   GET    /recomendacoes/utilizador/<uid>
#   POST   /recomendacoes                  -> cria manual
#   POST   /recomendacoes/diarias          -> gera automaticas
#   PUT    /recomendacoes/<rid>            -> atualiza
#   DELETE /recomendacoes/<rid>            -> remove
# ======================================================
import sys, os, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# garante que os modulos do projeto sao encontrados
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import utilizadores as bd_utilizadores
import conteudo     as bd_conteudo
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

def popular_dados_exemplo():
    """Cria dados de exemplo para testar o servidor de forma autonoma."""
    bd_utilizadores.criar_utilizador("Ana Silva", "ana@email.com", "pass123", "premium")
    bd_utilizadores.criar_utilizador("Rui Costa", "rui@email.com", "pass456", "basic")
    bd_conteudo.criar_conteudo("Inception", "filme", "Ficcao Cientifica", 2010,
                               "M/12", 8.8, 2500000, "Emma Thomas", "Christopher Nolan",
                               duracao=148)
    bd_conteudo.criar_conteudo("Breaking Bad", "serie", "Drama", 2008,
                               "M/18", 9.5, 1800000, "Mark Johnson", "Vince Gilligan",
                               numero_temporadas=5)
    print("[INFO] Dados de exemplo carregados (U001, U002, C001, C002).")

# ── handler HTTP ─────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        metodo = self.command
        caminho = self.path
        estado  = args[1] if len(args) > 1 else "?"
        print(f"  [{metodo}] {caminho}  ->  {estado}")

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

        # POST /recomendacoes/diarias  -> gera automaticamente
        if p == ["recomendacoes", "diarias"]:
            codigo, msg = bd_rec.gerar_recomendacoes_diarias()
            enviar_json(self, codigo, {"mensagem": msg})

        # POST /recomendacoes  -> cria manualmente
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
            codigo, msg = bd_rec.criar_recomendacao(uid, cid, motivo or None)
            enviar_json(self, codigo, {"mensagem": msg})

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
            codigo, msg = bd_rec.atualizar_recomendacao(p[1], motivo, score)
            enviar_json(self, codigo, {"mensagem": msg})

        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado."})

    # ── DELETE ──────────────────────────────────────────────
    def do_DELETE(self):
        p = self._partes()

        # DELETE /recomendacoes/<rid>
        if len(p) == 2 and p[0] == "recomendacoes":
            codigo, msg = bd_rec.remover_recomendacao(p[1])
            enviar_json(self, codigo, {"mensagem": msg})

        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado."})


# ── arranque ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 52)
    print("  SERVIDOR DE RECOMENDACOES — http://localhost:8001")
    print("=" * 52)
    popular_dados_exemplo()
    print(f"\nEndpoints disponiveis:")
    print("  GET    /recomendacoes")
    print("  GET    /recomendacoes/<rid>")
    print("  GET    /recomendacoes/utilizador/<uid>")
    print("  POST   /recomendacoes          {idUtilizador, idConteudo, motivo?}")
    print("  POST   /recomendacoes/diarias  (sem corpo — gera automaticamente)")
    print("  PUT    /recomendacoes/<rid>    {motivo?, scoreRelevancia?}")
    print("  DELETE /recomendacoes/<rid>")
    print("\nPrime CTRL+C para parar.\n")

    servidor = HTTPServer((HOST, PORT), Handler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Servidor parado.")
        servidor.server_close()
