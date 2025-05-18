import sys
import os
import traceback
from ia import process_prompt
from executor import execute_code

def print_header():
    print("="*60)
    print("  JOE AGENT • Inteligência Local Modular")
    print("  Digite comandos em linguagem natural. 'sair' para encerrar.")
    print("="*60)

def main():
    print_header()

    while True:
        try:
            comando = input("\nVocê: ").strip()
            if comando.lower() in ["sair", "exit", "quit"]:
                print("Encerrando joeAgent...")
                break

            resposta = process_prompt(comando)

            print("\n🤖 Resposta da IA:")
            print("-" * 60)
            print(resposta)
            print("-" * 60)

            if "```python" in resposta:
                codigo = extrair_codigo_python(resposta)
                if codigo:
                    print("\nExecutando código gerado...")
                    execute_code(codigo)
                else:
                    print("Nenhum código Python encontrado.")
            else:
                print("\nNenhum código executável detectado. Somente resposta textual.")

        except Exception as e:
            print(f"\n[Erro no joeAgent]: {e}")
            traceback.print_exc()

def extrair_codigo_python(texto):
    import re

    # Prioridade 1: procurar bloco markdown correto
    matches = re.findall(r"```python(.*?)```", texto, re.DOTALL)
    if matches:
        return matches[0].strip()

    # Prioridade 2: detectar código mesmo sem markdown (fallback)
    linhas = texto.strip().split("\n")
    provavel_codigo = []
    for linha in linhas:
        if linha.strip().startswith(("import ", "def ", "for ", "if ", "while ", "print(", "#", "class ")):
            provavel_codigo.append(linha)

    if len(provavel_codigo) >= 2:
        print("\n⚠️ Detectei um possível bloco de código Python:")
        print("-" * 60)
        print("\n".join(provavel_codigo))
        escolha = input("\nDeseja executar esse código? (s/n): ").lower()
        if escolha == "s":
            return "\n".join(provavel_codigo)

    return None

if __name__ == "__main__":
    main()