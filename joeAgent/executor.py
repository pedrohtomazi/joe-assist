import traceback

def execute_code(codigo):
    """
    Executa código Python passado como string, com proteção de erro.
    """
    try:
        # Define um contexto de execução isolado
        contexto = {}
        exec(codigo, contexto)

    except Exception as e:
        print("\n⚠️ Erro ao executar o código gerado:")
        print("-" * 60)
        print(f"{type(e).__name__}: {e}")
        traceback.print_exc()
        print("-" * 60)
