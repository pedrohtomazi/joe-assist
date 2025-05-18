import tkinter as tk
from tkinter import scrolledtext, messagebox
from ia import process_prompt
from executor import execute_code
from main import extrair_codigo_python
from modules.auto_learn import aprender_com_long_term
import module_creator
import re
import tkinter.simpledialog
import json
import os

# 🎨 Estilo visual
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#d4d4d4"
INPUT_BG = "#2d2d2d"
BTN_BG = "#3c3c3c"
BTN_ACTIVE_BG = "#555"
FONT = ("Consolas", 12)

def carregar_comandos_dinamicos():
    caminho = "memory/commands.json"
    if not os.path.exists("memory"):
        os.makedirs("memory")

    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
comandos_dinamicos = carregar_comandos_dinamicos()

def enviar_mensagem():
    comando = entrada_usuario.get().strip()
    if not comando:
        return

    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, f"👤 Você:\n{comando}\n\n")
    chat_text.config(state=tk.DISABLED)
    chat_text.see(tk.END)
    entrada_usuario.delete(0, tk.END)

    # 📦 Execução de comandos registrados dinamicamente
    if comando.lower() in comandos_dinamicos:
        info = comandos_dinamicos[comando.lower()]
        try:
            modulo = __import__(f"modules.{info['modulo']}", fromlist=[info['funcao']])
            funcao = getattr(modulo, info['funcao'])
            resposta = funcao()
        except Exception as e:
            resposta = f"❌ Erro ao executar comando '{comando}': {e}"
    
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, f"🤖 joeAgent:\n{resposta}\n\n")
        chat_text.config(state=tk.DISABLED)
        chat_text.see(tk.END)
        return

    # Comando: /autolearn
    if comando.lower().startswith("/autolearn"):
        resposta = aprender_com_long_term()

    # Comando: /lfta nome_do_arquivo sobre assunto
    elif comando.lower().startswith("/lfta"):
        partes = comando.split()
        if len(partes) < 4 or "sobre" not in comando:
            resposta = "⚠️ Use assim: /lfta nome_do_arquivo sobre assunto"
        else:
            nome = partes[1]
            assunto = partes[-1]
            from learning_tools import learning_from_archive
            resposta = learning_from_archive(nome, assunto)

    # Comando: /criar_modulo nome_do_modulo
    elif comando.lower().startswith("/criar_modulo "):
        nome_modulo = comando.split("/criar_modulo ", 1)[-1].strip()
        if nome_modulo:
            from module_creator import criar_modulo
            criar_modulo(nome_modulo)
            return
        else:
            messagebox.showwarning("Comando Inválido", "Informe o nome do módulo após /criar_modulo.")
            return

    # Comando comum
    else:
        resposta = process_prompt(comando)

    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "🤖 joeAgent:\n")

    # Formatação de blocos de código
    partes = re.split(r"```(?:\w+)?\n|```", resposta)
    for i, parte in enumerate(partes):
        if i % 2 == 0:
            chat_text.insert(tk.END, parte.strip() + "\n\n")
        else:
            chat_text.insert(tk.END, parte.strip() + "\n\n", "codigo")

    chat_text.config(state=tk.DISABLED)
    chat_text.see(tk.END)

    # Execução de código (opcional)
    codigo = extrair_codigo_python(resposta)
    if codigo:
        confirmar = messagebox.askyesno("Executar Código", "Detectei um código Python. Deseja executar?")
        if confirmar:
            execute_code(codigo)

# 🖼️ Interface principal
janela = tk.Tk()
janela.title("joeAgent")
janela.geometry("900x650")
janela.configure(bg=BG_COLOR)

chat_text = scrolledtext.ScrolledText(
    janela,
    state=tk.DISABLED,
    wrap=tk.WORD,
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    font=FONT,
    insertbackground=TEXT_COLOR,
    borderwidth=0,
    highlightthickness=0
)
chat_text.tag_config(
    "codigo",
    background="#2b2b2b",
    foreground="#9cdcfe",
    font=("Consolas", 11),
    lmargin1=10,
    lmargin2=10,
    spacing3=10
)
chat_text.pack(padx=12, pady=12, fill=tk.BOTH, expand=True)

frame_input = tk.Frame(janela, bg=BG_COLOR)
frame_input.pack(fill=tk.X, padx=12, pady=8)

entrada_usuario = tk.Entry(
    frame_input,
    bg=INPUT_BG,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    font=FONT,
    relief=tk.FLAT
)
entrada_usuario.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=6)
entrada_usuario.bind("<Return>", lambda event: enviar_mensagem())

botao_enviar = tk.Button(
    frame_input,
    text="Enviar",
    command=enviar_mensagem,
    bg=BTN_BG,
    fg="#ffffff",
    activebackground=BTN_ACTIVE_BG,
    activeforeground="#ffffff",
    relief=tk.FLAT,
    padx=14,
    pady=6
)
botao_enviar.pack(side=tk.RIGHT)

janela.mainloop()
