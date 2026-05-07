#!/usr/bin/env python3
# ======================================================
# recomendacoes_server.py — porta 8001
# Terminal 2 -> python recomendacoes_server.py
# ======================================================
import sys, os, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import utilizadores as bd_u, conteudo as bd_c, favoritos as bd_f, recomendacoes as bd_r

HOST, PORT = "localhost", 8001

def enviar_json(h, codigo, dados):
    corpo = json.dumps(dados, ensure_ascii=False, indent=2).encode()
    h.send_response(codigo)
    h.send_header("Content-Type", "application/json; charset=utf-8")
    h.send_header("Content-Length", len(corpo))
    h.end_headers()
    h.wfile.write(corpo)

def ler_json(h):
    n = int(h.headers.get("Content-Length", 0))
    return json.loads(h.rfile.read(n)) if n else {}

def escolher_conteudo(uid):
    """Recomenda por genero dos favoritos; se nao tiver, recomenda o mais avaliado."""
    _, conteudos = bd_c.listar_conteudos()
    lista = list(conteudos.values()) if isinstance(conteudos, dict) else []
    if not lista:
        return None, "Sem conteudos"

    codigo, fav = bd_f.obter_favoritos_utilizador(uid)
    if codigo == 200:
        ids_fav  = fav["lista_ids_Conteudo"]
        generos  = {bd_c.obter_conteudo(c)[1]["genero"].lower() for c in ids_fav if bd_c.obter_conteudo(c)[0] == 200}
        candidatos = [c for c in lista if c["genero"].lower() in generos and c["idConteudo"] not in ids_fav]
        if candidatos:
            escolhido = max(candidatos, key=lambda c: c["avaliacao"])
            return escolhido, f"Baseado nos seus favoritos ({escolhido['genero']})"

    escolhido = max(lista, key=lambda c: c["avaliacao"])
    return escolhido, "Mais popular da plataforma"

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): print(f"[{self.command}] {self.path}")
    def _p(self): return [x for x in self.path.strip("/").split("/") if x]

    def do_GET(self):
        p = self._p()
        if p == ["recomendacoes"]:
            c, d = bd_r.listar_recomendacoes()
        elif len(p) == 2 and p[0] == "recomendacoes":
            c, d = bd_r.obter_recomendacao(p[1])
        else:
            c, d = 404, "Endpoint nao encontrado"
        enviar_json(self, c, d if isinstance(d, dict) else {"mensagem": d})

    def do_POST(self):
        p = self._p()
        if p == ["recomendacoes", "diarias"]:
            _, utilizadores = bd_u.listar_utilizadores()
            geradas, hoje = [], datetime.now().strftime("%d/%m/%Y")
            for uid in (utilizadores or {}):
                ja_tem = any(r["idUtilizador"] == uid and r["dataGeracao"].startswith(hoje) for r in bd_r.recomendacoes.values())
                if ja_tem: continue
                cont, motivo = escolher_conteudo(uid)
                if cont:
                    _, rec = bd_r.criar_recomendacao(uid, cont["idConteudo"], motivo)
                    if isinstance(rec, dict): geradas.append(rec)
            enviar_json(self, 200, {"geradas": len(geradas), "recomendacoes": geradas})
        elif p == ["recomendacoes"]:
            b = ler_json(self)
            c, d = bd_r.criar_recomendacao(b.get("idUtilizador",""), b.get("idConteudo",""), b.get("motivo"))
            enviar_json(self, c, d if isinstance(d, dict) else {"mensagem": d})
        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado"})

    def do_PUT(self):
        p = self._p()
        if len(p) == 2 and p[0] == "recomendacoes":
            b = ler_json(self)
            c, d = bd_r.atualizar_recomendacao(p[1], b.get("motivo"), b.get("scoreRelevancia"))
            enviar_json(self, c, d if isinstance(d, dict) else {"mensagem": d})
        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado"})

    def do_DELETE(self):
        p = self._p()
        if len(p) == 2 and p[0] == "recomendacoes":
            c, d = bd_r.remover_recomendacao(p[1])
            enviar_json(self, c, {"mensagem": d})
        else:
            enviar_json(self, 404, {"mensagem": "Endpoint nao encontrado"})

if __name__ == "__main__":
    print(f"Servidor a correr em http://{HOST}:{PORT} — CTRL+C para parar")
    s = HTTPServer((HOST, PORT), Handler)
    try: s.serve_forever()
    except KeyboardInterrupt: s.server_close()
