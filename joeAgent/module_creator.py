import os
import tkinter.simpledialog
from ia import process_prompt

def extrair_codigo_python(texto):
    import re
    matches = re.findall(r"```python(.*?)```", texto, re.DOTALL)
    return matches[0].strip() if matches else None

def criar_modulo(nome_modulo):
    """
    Interage com o usuário para definir o módulo, gera um esqueleto via IA
    e salva em modules/nome_modulo.py se aprovado.
    """
    caminho = f"modules/{nome_modulo}.py"

    if os.path.exists(caminho):
        print(f"❌ O módulo '{nome_modulo}' já existe.")
        return

    print(f"📦 Iniciando criação do módulo: {nome_modulo}")

    descricao = tkinter.simpledialog.askstring(
        "Descrição do Módulo",
        f"O que o módulo '{nome_modulo}' deve fazer?",
    )
    if not descricao:
        print("❌ Cancelado pelo usuário.")
        return

    prompt = f"""Crie um script Python modular chamado '{nome_modulo}' com base na seguinte descrição:
\"\"\"{descricao}\"\"\"

O código deve estar completo e organizado, e conter funções nomeadas conforme o propósito.
Retorne somente o código dentro de um bloco ```python.
"""

    resposta = process_prompt(prompt)

    print("\n🤖 Código gerado:")
    print("-" * 60)
    print(resposta)
    print("-" * 60)

    # Extrair código Python da resposta
    codigo = extrair_codigo_python(resposta)
    if not codigo:
        print("❌ Nenhum código válido encontrado.")
        return

    salvar = tkinter.messagebox.askyesno(
        "Salvar Módulo?",
        f"Deseja salvar o módulo '{nome_modulo}' em modules/?"
    )

    if salvar:
        os.makedirs("modules", exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(codigo)
        print(f"✅ Módulo '{nome_modulo}' salvo com sucesso em {caminho}")
    else:
        print("❌ Módulo descartado.")

