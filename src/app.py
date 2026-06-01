# ==============================
# app.py
# aplicacao tkinter — substitui main.py
# gestor de streaming
# ==============================
import tkinter as tk
from tkinter import ttk, messagebox
import utilizadores  as bd_utilizadores
import conteudo      as bd_conteudo
import historico     as bd_historico
import favoritos     as bd_favoritos
import recomendacoes as bd_recomendacoes

# ── cores e estilos ─────────────────────────────────────────
COR_FUNDO      = "#1a1a2e"
COR_PAINEL     = "#16213e"
COR_CARD       = "#0f3460"
COR_DESTAQUE   = "#e94560"
COR_TEXTO      = "#ffffff"
COR_TEXTO_SUB  = "#a0a0b0"
COR_ENTRADA    = "#0d2137"
COR_SUCESSO    = "#4caf50"
COR_AVISO      = "#ff9800"
FONTE_TITULO   = ("Segoe UI", 18, "bold")
FONTE_SUBTIT   = ("Segoe UI", 12, "bold")
FONTE_NORMAL   = ("Segoe UI", 10)
FONTE_PEQUENA  = ("Segoe UI", 9)

# ── helper global ───────────────────────────────────────────
def campo(pai, label, row, col=0, span=1, default=""):
    tk.Label(pai, text=label, bg=COR_PAINEL, fg=COR_TEXTO_SUB,
             font=FONTE_PEQUENA).grid(row=row, column=col*2, sticky="w", padx=6, pady=3)
    var = tk.StringVar(value=default)
    e = tk.Entry(pai, textvariable=var, bg=COR_ENTRADA, fg=COR_TEXTO,
                 insertbackground=COR_TEXTO, relief="flat", font=FONTE_NORMAL,
                 width=22)
    e.grid(row=row, column=col*2+1, sticky="ew", padx=6, pady=3, columnspan=span)
    return var

def botao(pai, texto, cmd, cor=COR_DESTAQUE, row=0, col=0, span=1):
    tk.Button(pai, text=texto, command=cmd, bg=cor, fg=COR_TEXTO,
              relief="flat", font=FONTE_NORMAL, cursor="hand2",
              activebackground=COR_CARD, activeforeground=COR_TEXTO,
              padx=10, pady=5).grid(row=row, column=col, columnspan=span,
                                     padx=6, pady=8, sticky="ew")

def tabela(pai, colunas, row=0, col=0, span=1, height=12):
    frame = tk.Frame(pai, bg=COR_PAINEL)
    frame.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=6, pady=6)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dark.Treeview",
                    background=COR_CARD, foreground=COR_TEXTO,
                    fieldbackground=COR_CARD, rowheight=26,
                    font=FONTE_PEQUENA)
    style.configure("Dark.Treeview.Heading",
                    background=COR_PAINEL, foreground=COR_DESTAQUE,
                    font=("Segoe UI", 9, "bold"))
    style.map("Dark.Treeview", background=[("selected", COR_DESTAQUE)])
    tv = ttk.Treeview(frame, columns=colunas, show="headings",
                      style="Dark.Treeview", height=height)
    for c in colunas:
        tv.heading(c, text=c)
        tv.column(c, width=max(80, 120 if c in ("titulo","nome","email","motivo") else 80),
                  anchor="center")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=sb.set)
    tv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return tv

def aviso(msg, erro=False):
    if erro:
        messagebox.showerror("Erro", msg)
    else:
        messagebox.showinfo("Sucesso", msg)

# ════════════════════════════════════════════════════════════
# JANELA PRINCIPAL
# ════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Streaming")
        self.configure(bg=COR_FUNDO)
        self.geometry("1100x700")
        self.resizable(True, True)
        self._construir()

    def _construir(self):
        # barra lateral
        sidebar = tk.Frame(self, bg=COR_PAINEL, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🎬", bg=COR_PAINEL, fg=COR_DESTAQUE,
                 font=("Segoe UI", 28)).pack(pady=(24, 4))
        tk.Label(sidebar, text="Streaming", bg=COR_PAINEL, fg=COR_TEXTO,
                 font=FONTE_SUBTIT).pack(pady=(0, 24))

        self.frames = {}
        secoes = [
            ("👤  Utilizadores",  FrameUtilizadores),
            ("🎥  Conteúdos",     FrameConteudos),
            ("📋  Histórico",     FrameHistorico),
            ("❤️  Favoritos",     FrameFavoritos),
            ("⭐  Recomendações", FrameRecomendacoes),
        ]

        container = tk.Frame(self, bg=COR_FUNDO)
        container.pack(side="right", fill="both", expand=True)

        for nome, cls in secoes:
            f = cls(container)
            f.place(relwidth=1, relheight=1)
            self.frames[nome] = f

        def mostrar(nome):
            self.frames[nome].tkraise()
            self.frames[nome].atualizar()

        for nome, _ in secoes:
            btn = tk.Button(sidebar, text=nome, bg=COR_PAINEL, fg=COR_TEXTO,
                            relief="flat", font=FONTE_NORMAL, anchor="w",
                            cursor="hand2", padx=16, pady=8,
                            activebackground=COR_CARD, activeforeground=COR_DESTAQUE,
                            command=lambda n=nome: mostrar(n))
            btn.pack(fill="x")

        mostrar("👤  Utilizadores")


# ════════════════════════════════════════════════════════════
# FRAME BASE
# ════════════════════════════════════════════════════════════
class FrameBase(tk.Frame):
    def __init__(self, pai):
        super().__init__(pai, bg=COR_FUNDO)

    def atualizar(self):
        pass

    def _titulo(self, texto):
        tk.Label(self, text=texto, bg=COR_FUNDO, fg=COR_TEXTO,
                 font=FONTE_TITULO).pack(anchor="w", padx=20, pady=(16, 8))

    def _painel(self, titulo=None):
        if titulo:
            tk.Label(self, text=titulo, bg=COR_FUNDO, fg=COR_TEXTO_SUB,
                     font=FONTE_SUBTIT).pack(anchor="w", padx=20, pady=(8, 0))
        p = tk.Frame(self, bg=COR_PAINEL, bd=0)
        p.pack(fill="x", padx=20, pady=4)
        return p

    def _resultado(self, codigo, dados, tv=None, mapa=None):
        if codigo not in (200, 201):
            aviso(str(dados), erro=True)
            return
        if tv and mapa:
            self.atualizar()
        else:
            aviso(f"[{codigo}] {dados}")


# ════════════════════════════════════════════════════════════
# UTILIZADORES
# ════════════════════════════════════════════════════════════
class FrameUtilizadores(FrameBase):
    def __init__(self, pai):
        super().__init__(pai)
        self._titulo("👤 Utilizadores")

        # formulário
        p = self._painel("Novo Utilizador")
        p.columnconfigure((1, 3), weight=1)
        self.v_nome  = campo(p, "Nome",         0, 0)
        self.v_email = campo(p, "Email",         0, 1)
        self.v_passe = campo(p, "Palavra-passe", 1, 0)
        self.v_plano = campo(p, "Plano (basic/premium)", 1, 1)

        pf = tk.Frame(self, bg=COR_FUNDO)
        pf.pack(fill="x", padx=20, pady=4)
        botao(pf, "➕ Criar",    self._criar,    row=0, col=0)
        botao(pf, "✏️  Atualizar", self._atualizar, cor=COR_CARD, row=0, col=1)
        botao(pf, "🗑️  Remover",  self._remover,  cor="#6b2737", row=0, col=2)
        botao(pf, "🔄 Atualizar Lista", self.atualizar, cor=COR_PAINEL, row=0, col=3)

        self.tv = tabela(self,
            ("ID", "Nome", "Email", "Plano", "Estado"), row=0)
        self.tv.pack(fill="both", expand=True, padx=20, pady=8)

    def atualizar(self):
        for i in self.tv.get_children(): self.tv.delete(i)
        c, d = bd_utilizadores.listar_utilizadores()
        if c == 200:
            for uid, u in d.items():
                estado = "Ativo" if u["estado"] == 1 else "Inativo"
                self.tv.insert("", "end", values=(uid, u["nome"], u["email"],
                                                   u["tipoPlano"], estado))

    def _criar(self):
        c, d = bd_utilizadores.criar_utilizador(
            self.v_nome.get(), self.v_email.get(),
            self.v_passe.get(), self.v_plano.get())
        if c == 201:
            aviso(f"Utilizador criado: {d}")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _atualizar(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona um utilizador na tabela.", erro=True); return
        uid = self.tv.item(sel[0])["values"][0]
        c, d = bd_utilizadores.atualizar_utilizador(
            uid,
            nome       = self.v_nome.get()  or None,
            email      = self.v_email.get() or None,
            palavrapasse = self.v_passe.get() or None,
            tipo_plano = self.v_plano.get() or None)
        if c == 200:
            aviso(f"Utilizador '{uid}' atualizado.")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _remover(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona um utilizador na tabela.", erro=True); return
        uid = self.tv.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"Remover utilizador '{uid}'?"):
            return
        c, d = bd_utilizadores.remover_utilizador(uid)
        if c == 200:
            aviso(f"Utilizador '{uid}' removido.")
            self.atualizar()
        else:
            aviso(d, erro=True)


# ════════════════════════════════════════════════════════════
# CONTEUDOS
# ════════════════════════════════════════════════════════════
class FrameConteudos(FrameBase):
    def __init__(self, pai):
        super().__init__(pai)
        self._titulo("🎥 Conteúdos")

        p = self._painel("Novo Conteúdo")
        p.columnconfigure((1, 3, 5), weight=1)
        self.v_titulo    = campo(p, "Título",          0, 0)
        self.v_tipo      = campo(p, "Tipo (filme/serie)", 0, 1)
        self.v_genero    = campo(p, "Género",          0, 2)
        self.v_ano       = campo(p, "Ano",             1, 0)
        self.v_class_et  = campo(p, "Class. Etária",   1, 1)
        self.v_aval      = campo(p, "Avaliação (0-10)",1, 2)
        self.v_num_aval  = campo(p, "Nº Avaliadores",  2, 0)
        self.v_produtor  = campo(p, "Produtor",        2, 1)
        self.v_realiz    = campo(p, "Realizador",      2, 2)
        self.v_duracao   = campo(p, "Duração (min)",   3, 0)
        self.v_tempor    = campo(p, "Nº Temporadas",   3, 1)

        pf = tk.Frame(self, bg=COR_FUNDO)
        pf.pack(fill="x", padx=20, pady=4)
        botao(pf, "➕ Criar",    self._criar,    row=0, col=0)
        botao(pf, "✏️  Atualizar", self._atualizar, cor=COR_CARD, row=0, col=1)
        botao(pf, "🗑️  Remover",  self._remover,  cor="#6b2737", row=0, col=2)
        botao(pf, "🔄 Atualizar Lista", self.atualizar, cor=COR_PAINEL, row=0, col=3)

        self.tv = tabela(self,
            ("ID", "Título", "Tipo", "Género", "Ano", "Avaliação", "Realizador"))
        self.tv.pack(fill="both", expand=True, padx=20, pady=8)

    def atualizar(self):
        for i in self.tv.get_children(): self.tv.delete(i)
        c, d = bd_conteudo.listar_conteudos()
        if c == 200:
            for cid, ct in d.items():
                self.tv.insert("", "end", values=(
                    cid, ct["titulo"], ct["tipo"], ct["genero"],
                    ct["anoLancamento"], ct["avaliacao"], ct["realizador"]))

    def _criar(self):
        c, d = bd_conteudo.criar_conteudo(
            self.v_titulo.get(), self.v_tipo.get(), self.v_genero.get(),
            self.v_ano.get(), self.v_class_et.get(), self.v_aval.get(),
            self.v_num_aval.get(), self.v_produtor.get(), self.v_realiz.get(),
            self.v_duracao.get() or 0, self.v_tempor.get() or 0)
        if c == 201:
            aviso(f"Conteúdo criado: {d}")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _atualizar(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona um conteúdo na tabela.", erro=True); return
        cid = self.tv.item(sel[0])["values"][0]
        c, d = bd_conteudo.atualizar_conteudo(
            cid,
            titulo     = self.v_titulo.get()   or None,
            avaliacao  = float(self.v_aval.get()) if self.v_aval.get() else None,
            produtor   = self.v_produtor.get() or None,
            realizador = self.v_realiz.get()   or None)
        if c == 200:
            aviso(f"Conteúdo '{cid}' atualizado.")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _remover(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona um conteúdo na tabela.", erro=True); return
        cid = self.tv.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"Remover conteúdo '{cid}'?"):
            return
        c, d = bd_conteudo.remover_conteudo(cid)
        if c == 200:
            aviso(f"Conteúdo '{cid}' removido.")
            self.atualizar()
        else:
            aviso(d, erro=True)


# ════════════════════════════════════════════════════════════
# HISTORICO
# ════════════════════════════════════════════════════════════
class FrameHistorico(FrameBase):
    def __init__(self, pai):
        super().__init__(pai)
        self._titulo("📋 Histórico de Visualizações")

        p = self._painel("Registar Visualização")
        p.columnconfigure((1, 3, 5), weight=1)
        self.v_uid       = campo(p, "ID Utilizador", 0, 0)
        self.v_cid       = campo(p, "ID Conteúdo",   0, 1)
        self.v_progresso = campo(p, "Progresso (%)", 0, 2)

        pf = tk.Frame(self, bg=COR_FUNDO)
        pf.pack(fill="x", padx=20, pady=4)
        botao(pf, "➕ Registar",   self._registar,  row=0, col=0)
        botao(pf, "✏️  Atualizar",  self._atualizar, cor=COR_CARD, row=0, col=1)
        botao(pf, "🗑️  Remover",   self._remover,   cor="#6b2737", row=0, col=2)
        botao(pf, "🔄 Atualizar Lista", self.atualizar, cor=COR_PAINEL, row=0, col=3)

        self.tv = tabela(self,
            ("ID", "Utilizador", "Conteúdo", "Data", "Progresso (%)"))
        self.tv.pack(fill="both", expand=True, padx=20, pady=8)

    def atualizar(self):
        for i in self.tv.get_children(): self.tv.delete(i)
        c, d = bd_historico.listar_historico()
        if c == 200:
            for hid, h in d.items():
                self.tv.insert("", "end", values=(
                    hid, h["idUtilizador"], h["idConteudo"],
                    h["dataVisualizacao"], h["progresso"]))

    def _registar(self):
        c, d = bd_historico.registar_visualizacao(
            self.v_uid.get(), self.v_cid.get(), self.v_progresso.get())
        if c == 201:
            aviso(f"Visualização registada: {d}")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _atualizar(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona um registo na tabela.", erro=True); return
        hid = self.tv.item(sel[0])["values"][0]
        prog = self.v_progresso.get()
        if not prog:
            aviso("Preenche o novo progresso.", erro=True); return
        c, d = bd_historico.atualizar_historico(hid, prog)
        if c == 200:
            aviso(f"Registo '{hid}' atualizado.")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _remover(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona um registo na tabela.", erro=True); return
        hid = self.tv.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"Remover registo '{hid}'?"):
            return
        c, d = bd_historico.remover_historico(hid)
        if c == 200:
            aviso(f"Registo '{hid}' removido.")
            self.atualizar()
        else:
            aviso(d, erro=True)


# ════════════════════════════════════════════════════════════
# FAVORITOS
# ════════════════════════════════════════════════════════════
class FrameFavoritos(FrameBase):
    def __init__(self, pai):
        super().__init__(pai)
        self._titulo("❤️ Favoritos")

        p = self._painel("Gerir Favoritos")
        p.columnconfigure((1, 3), weight=1)
        self.v_uid  = campo(p, "ID Utilizador",               0, 0)
        self.v_cids = campo(p, "IDs Conteúdo (ex: C001,C002)", 0, 1)

        pf = tk.Frame(self, bg=COR_FUNDO)
        pf.pack(fill="x", padx=20, pady=4)
        botao(pf, "➕ Adicionar",   self._adicionar,  row=0, col=0)
        botao(pf, "✏️  Atualizar",   self._atualizar,  cor=COR_CARD, row=0, col=1)
        botao(pf, "🗑️  Remover",    self._remover,    cor="#6b2737", row=0, col=2)
        botao(pf, "🔄 Atualizar Lista", self.atualizar, cor=COR_PAINEL, row=0, col=3)

        self.tv = tabela(self,
            ("ID", "Utilizador", "Conteúdos Favoritos", "Criado em", "Atualizado em"))
        self.tv.pack(fill="both", expand=True, padx=20, pady=8)

    def atualizar(self):
        for i in self.tv.get_children(): self.tv.delete(i)
        c, d = bd_favoritos.listar_favoritos()
        if c == 200:
            for fid, f in d.items():
                self.tv.insert("", "end", values=(
                    fid, f["idUtilizador"],
                    ", ".join(f["lista_ids_Conteudo"]),
                    f["data_criacao"], f["data_atualizacao"]))

    def _adicionar(self):
        c, d = bd_favoritos.adicionar_favorito(
            self.v_uid.get(), self.v_cids.get())
        if c in (200, 201):
            aviso(f"Favoritos atualizados: {d}")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _atualizar(self):
        uid = self.v_uid.get()
        cids = self.v_cids.get()
        if not uid or not cids:
            aviso("Preenche o ID Utilizador e a nova lista.", erro=True); return
        c, d = bd_favoritos.atualizar_favorito(uid, cids)
        if c == 200:
            aviso(f"Favoritos de '{uid}' atualizados.")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _remover(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona um registo na tabela.", erro=True); return
        uid = self.tv.item(sel[0])["values"][1]
        if not messagebox.askyesno("Confirmar", f"Remover todos os favoritos de '{uid}'?"):
            return
        c, d = bd_favoritos.remover_favoritos_utilizador(uid)
        if c == 200:
            aviso(f"Favoritos de '{uid}' removidos.")
            self.atualizar()
        else:
            aviso(d, erro=True)


# ════════════════════════════════════════════════════════════
# RECOMENDACOES
# ════════════════════════════════════════════════════════════
class FrameRecomendacoes(FrameBase):
    def __init__(self, pai):
        super().__init__(pai)
        self._titulo("⭐ Recomendações")

        p = self._painel("Criar Recomendação Manual")
        p.columnconfigure((1, 3, 5), weight=1)
        self.v_uid    = campo(p, "ID Utilizador", 0, 0)
        self.v_cid    = campo(p, "ID Conteúdo",   0, 1)
        self.v_motivo = campo(p, "Motivo (opcional)", 0, 2)

        pf = tk.Frame(self, bg=COR_FUNDO)
        pf.pack(fill="x", padx=20, pady=4)
        botao(pf, "➕ Criar",           self._criar,    row=0, col=0)
        botao(pf, "✏️  Atualizar",       self._atualizar, cor=COR_CARD, row=0, col=1)
        botao(pf, "🗑️  Remover",        self._remover,  cor="#6b2737", row=0, col=2)
        botao(pf, "🔄 Atualizar Lista", self.atualizar, cor=COR_PAINEL, row=0, col=3)

        self.tv = tabela(self,
            ("ID", "Utilizador", "Conteúdo", "Data", "Score", "Motivo"))
        self.tv.pack(fill="both", expand=True, padx=20, pady=8)

    def atualizar(self):
        for i in self.tv.get_children(): self.tv.delete(i)
        c, d = bd_recomendacoes.listar_recomendacoes()
        if c == 200:
            for rid, r in d.items():
                self.tv.insert("", "end", values=(
                    rid, r["idUtilizador"], r["idConteudo"],
                    r["dataGeracao"], r["scoreRelevancia"], r["motivo"]))

    def _criar(self):
        c, d = bd_recomendacoes.criar_recomendacao(
            self.v_uid.get(), self.v_cid.get(),
            self.v_motivo.get() or None)
        if c == 201:
            aviso(f"Recomendação criada: {d}")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _atualizar(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona uma recomendação na tabela.", erro=True); return
        rid = self.tv.item(sel[0])["values"][0]
        c, d = bd_recomendacoes.atualizar_recomendacao(
            rid, motivo=self.v_motivo.get() or None)
        if c == 200:
            aviso(f"Recomendação '{rid}' atualizada.")
            self.atualizar()
        else:
            aviso(d, erro=True)

    def _remover(self):
        sel = self.tv.selection()
        if not sel:
            aviso("Seleciona uma recomendação na tabela.", erro=True); return
        rid = self.tv.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"Remover recomendação '{rid}'?"):
            return
        c, d = bd_recomendacoes.remover_recomendacao(rid)
        if c == 200:
            aviso(f"Recomendação '{rid}' removida.")
            self.atualizar()
        else:
            aviso(d, erro=True)


# ── arranque ─────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
