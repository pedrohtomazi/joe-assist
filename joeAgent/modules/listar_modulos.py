import os

def listar_modulos():
    """Retorna uma lista com os nomes dos arquivos .py na pasta modules/, exceto os especiais."""
    modulos = []
    for arquivo in os.listdir("modules"):
        if arquivo.endswith(".py") and not arquivo.startswith("__"):
            modulos.append(arquivo[:-3])
    return modulos

from modules.command_registry import registrar_comando
registrar_comando("/listarmodulos", "listar_modulos", "listar_modulos")

if __name__ == "__main__":
    print("Módulos encontrados:")
    for nome in listar_modulos():
        print("-", nome)