# src/app_tk.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.search import buscar_falhas_por_texto
from db import get_conn


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assistente de Manutenção - MVP")
        self.geometry("900x600")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        self.tab_auto = ttk.Frame(nb)
        self.tab_manual = ttk.Frame(nb)
        self.tab_camera = ttk.Frame(nb)

        nb.add(self.tab_auto, text="Busca automática (texto)")
        nb.add(self.tab_manual, text="Navegação manual")
        nb.add(self.tab_camera, text="Câmera (em breve)")

        self._build_tab_auto()
        self._build_tab_manual()
        self._build_tab_camera()

    # --- Aba Automática ---
    def _build_tab_auto(self):
        frm = ttk.Frame(self.tab_auto, padding=12)
        frm.pack(fill="both", expand=True)

        top = ttk.Frame(frm)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text="Descreva a falha:").pack(side="left")
        self.ent_busca = ttk.Entry(top)
        self.ent_busca.pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(top, text="Buscar",
                   command=self._on_buscar).pack(side="left")

        cols = ("id", "equipamento", "titulo", "descricao")
        self.tree_auto = ttk.Treeview(
            frm, columns=cols, show="headings", height=20)
        for c, w in zip(cols, (120, 220, 260, 260)):
            self.tree_auto.heading(c, text=c.capitalize())
            self.tree_auto.column(c, width=w, anchor="w")
        self.tree_auto.pack(fill="both", expand=True)

    def _on_buscar(self):
        q = self.ent_busca.get().strip()
        if not q:
            messagebox.showinfo(
                "Busca", "Digite um texto (ex.: 'não liga', 'alarme', 'sensor').")
            return
        self.tree_auto.delete(*self.tree_auto.get_children())
        try:
            resultados = buscar_falhas_por_texto(q)
            for fid, eq, tit, desc in resultados:
                self.tree_auto.insert(
                    "", "end", values=(fid, eq, tit, desc or ""))
            if not resultados:
                messagebox.showinfo(
                    "Busca", "Nada encontrado. Tente outras palavras.")
        except Exception as e:
            messagebox.showerror("Erro na busca", str(e))

    # --- Aba Manual ---
    def _build_tab_manual(self):
        frm = ttk.Frame(self.tab_manual, padding=12)
        frm.pack(fill="both", expand=True)

        # Combos
        combos = ttk.Frame(frm)
        combos.pack(fill="x", pady=(0, 8))

        self.cmb_amb = ttk.Combobox(combos, state="readonly")
        self.cmb_set = ttk.Combobox(combos, state="readonly")
        self.cmb_lin = ttk.Combobox(combos, state="readonly")
        self.cmb_eq = ttk.Combobox(combos, state="readonly")

        for w, lbl in [(self.cmb_amb, "Ambiente"), (self.cmb_set, "Setor"),
                       (self.cmb_lin, "Linha"), (self.cmb_eq, "Equipamento")]:
            c = ttk.Frame(combos)
            c.pack(side="left", padx=6)
            ttk.Label(c, text=lbl).pack(anchor="w")
            w.pack()

        ttk.Button(frm, text="Ver falhas", command=self._on_ver_falhas).pack(
            anchor="w", pady=6)

        # Tabela de falhas/soluções
        cols = ("id", "titulo", "descricao")
        self.tree_manual = ttk.Treeview(
            frm, columns=cols, show="headings", height=18)
        for c, w in zip(cols, (120, 240, 480)):
            self.tree_manual.heading(c, text=c.capitalize())
            self.tree_manual.column(c, width=w, anchor="w")
        self.tree_manual.pack(fill="both", expand=True)

        self._carregar_ambientes()
        self.cmb_amb.bind("<<ComboboxSelected>>",
                          lambda e: self._carregar_setores())
        self.cmb_set.bind("<<ComboboxSelected>>",
                          lambda e: self._carregar_linhas())
        self.cmb_lin.bind("<<ComboboxSelected>>",
                          lambda e: self._carregar_equipamentos())

    def _carregar_ambientes(self):
        with get_conn() as con:
            rows = con.execute(
                "SELECT id, nome FROM ambientes ORDER BY nome").fetchall()
        self._map_amb = {f"{r[1]} ({r[0]})": r[0] for r in rows}
        self.cmb_amb["values"] = list(self._map_amb.keys())

    def _carregar_setores(self):
        self.cmb_set.set("")
        self.cmb_lin.set("")
        self.cmb_eq.set("")
        amb_id = self._map_amb.get(self.cmb_amb.get())
        if not amb_id:
            return
        with get_conn() as con:
            rows = con.execute(
                "SELECT id, nome FROM setores WHERE ambiente_id=? ORDER BY nome", (
                    amb_id,)
            ).fetchall()
        self._map_set = {f"{r[1]} ({r[0]})": r[0] for r in rows}
        self.cmb_set["values"] = list(self._map_set.keys())

    def _carregar_linhas(self):
        self.cmb_lin.set("")
        self.cmb_eq.set("")
        set_id = self._map_set.get(self.cmb_set.get())
        if not set_id:
            return
        with get_conn() as con:
            rows = con.execute(
                "SELECT id, nome FROM linhas WHERE setor_id=? ORDER BY nome", (
                    set_id,)
            ).fetchall()
        self._map_lin = {f"{r[1]} ({r[0]})": r[0] for r in rows}
        self.cmb_lin["values"] = list(self._map_lin.keys())

    def _carregar_equipamentos(self):
        self.cmb_eq.set("")
        lin_id = self._map_lin.get(self.cmb_lin.get())
        if not lin_id:
            return
        with get_conn() as con:
            rows = con.execute(
                "SELECT id, nome FROM equipamentos WHERE linha_id=? ORDER BY nome", (
                    lin_id,)
            ).fetchall()
        self._map_eq = {f"{r[1]} ({r[0]})": r[0] for r in rows}
        self.cmb_eq["values"] = list(self._map_eq.keys())

    def _on_ver_falhas(self):
        self.tree_manual.delete(*self.tree_manual.get_children())
        eq_id = self._map_eq.get(self.cmb_eq.get())
        if not eq_id:
            messagebox.showinfo("Falhas", "Selecione um equipamento.")
            return
        with get_conn() as con:
            rows = con.execute(
                "SELECT id, titulo, COALESCE(descricao,'') FROM falhas WHERE equipamento_id=? ORDER BY titulo",
                (eq_id,)
            ).fetchall()
        for r in rows:
            self.tree_manual.insert("", "end", values=r)
        if not rows:
            messagebox.showinfo(
                "Falhas", "Nenhuma falha cadastrada para este equipamento.")

    # --- Aba Câmera (placeholder) ---
    def _build_tab_camera(self):
        frm = ttk.Frame(self.tab_camera, padding=12)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Módulo de câmera será adicionado quando o hardware chegar.").pack(
            anchor="w")


if __name__ == "__main__":
    App().mainloop()
