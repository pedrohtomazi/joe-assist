import json
import os
from datetime import datetime

SHORT_TERM_PATH = "memory/short_term.json"
LONG_TERM_PATH = "memory/long_term.json"
SHORT_TERM_MAX = 10

def carregar_short_term():
    if not os.path.exists(SHORT_TERM_PATH):
        return []

    with open(SHORT_TERM_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)
        if isinstance(dados, list):
            return dados
        return []  # evita erro de tipo errado
    
def salvar_short_term(memoria):
    memoria = memoria[-SHORT_TERM_MAX:]  # garante que não passa do limite
    with open(SHORT_TERM_PATH, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

def adicionar_interacao(pergunta, resposta):
    nova_entrada = {
        "timestamp": datetime.now().isoformat(),
        "pergunta": pergunta.strip(),
        "resposta": resposta.strip()
    }

    # Atualiza short term
    memoria = carregar_short_term()
    memoria.append(nova_entrada)
    salvar_short_term(memoria)

    # Atualiza long term
    if not os.path.exists(LONG_TERM_PATH):
        long_term = []
    else:
        with open(LONG_TERM_PATH, "r", encoding="utf-8") as f:
            long_term = json.load(f)

    long_term.append(nova_entrada)
    with open(LONG_TERM_PATH, "w", encoding="utf-8") as f:
        json.dump(long_term, f, indent=2, ensure_ascii=False)
