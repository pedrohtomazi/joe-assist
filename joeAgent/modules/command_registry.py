import os
import json

COMMANDS_PATH = "memory/commands.json"

def registrar_comando(comando: str, modulo: str, funcao: str):
    """
    Registra um comando no arquivo commands.json com a estrutura:
    {
      "/comando": {
        "modulo": "nome_do_modulo",
        "funcao": "nome_da_funcao"
      }
    }
    """
    if not comando.startswith("/"):
        raise ValueError("O comando deve começar com '/'")

    if not os.path.exists("memory"):
        os.makedirs("memory")

    if not os.path.exists(COMMANDS_PATH):
        with open(COMMANDS_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

    with open(COMMANDS_PATH, "r", encoding="utf-8") as f:
        comandos = json.load(f)

    # Valida se já existe
    if comando in comandos:
        if comandos[comando]["modulo"] == modulo and comandos[comando]["funcao"] == funcao:
            print(f"⚠️ Comando '{comando}' já está registrado com o mesmo destino.")
            return
        else:
            print(f"🔁 Atualizando comando '{comando}' para novo destino.")
    
    # Registra ou atualiza
    comandos[comando] = {
        "modulo": modulo,
        "funcao": funcao
    }

    with open(COMMANDS_PATH, "w", encoding="utf-8") as f:
        json.dump(comandos, f, indent=2, ensure_ascii=False)

    print(f"✅ Comando '{comando}' registrado em {COMMANDS_PATH}")
