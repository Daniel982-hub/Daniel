# ======================================================
# recomendacoes_server.py
# a cada 10 segundos gera uma recomendacao para
# cada utilizador com base nos seus favoritos
# Terminal 2 -> python recomendacoes_server.py
# ======================================================
import sys, os, time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import utilizadores as bd_u, conteudo as bd_c, favoritos as bd_f, recomendacoes as bd_r

def gerar_recomendacoes():
    _, utilizadores = bd_u.listar_utilizadores()
    if not isinstance(utilizadores, dict):
        print("Sem utilizadores registados.")
        return

    _, conteudos = bd_c.listar_conteudos()
    if not isinstance(conteudos, dict):
        print("Sem conteudos disponiveis.")
        return

    lista = list(conteudos.values())

    for uid in utilizadores:
        # obtem os favoritos do utilizador
        codigo, fav = bd_f.obter_favoritos_utilizador(uid)

        if codigo == 200:
            ids_fav = fav["lista_ids_Conteudo"]
            generos = {bd_c.obter_conteudo(c)[1]["genero"].lower() for c in ids_fav if bd_c.obter_conteudo(c)[0] == 200}
            candidatos = [c for c in lista if c["genero"].lower() in generos and c["idConteudo"] not in ids_fav]
            if candidatos:
                escolhido = max(candidatos, key=lambda c: c["avaliacao"])
                motivo = f"Baseado nos seus favoritos ({escolhido['genero']})"
            else:
                escolhido = max(lista, key=lambda c: c["avaliacao"])
                motivo = "Mais popular da plataforma"
        else:
            escolhido = max(lista, key=lambda c: c["avaliacao"])
            motivo = "Mais popular da plataforma"

        _, rid = bd_r.criar_recomendacao(uid, escolhido["idConteudo"], motivo)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {uid} -> {rid} ({motivo})")

if __name__ == "__main__":
    print("Servidor de recomendacoes iniciado — gera a cada 10 segundos. CTRL+C para parar.\n")
    while True:
        gerar_recomendacoes()
        time.sleep(10)
