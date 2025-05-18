import os
import json
from embedding_engine import salvar_embedding

LONG_TERM_PATH = "memory/long_term.json"
KNOWLEDGE_PATH = "knowledge"

def aprender_com_long_term(assunto="autoaprendizado"):
    if not os.path.exists(LONG_TERM_PATH):
        return "❌ Nenhuma memória encontrada em long_term.json"

    with open(LONG_TERM_PATH, "r", encoding="utf-8") as f:
        interacoes = json.load(f)

    caminho_knowledge = os.path.join(KNOWLEDGE_PATH, f"{assunto}.json")
    if os.path.exists(caminho_knowledge):
        with open(caminho_knowledge, "r", encoding="utf-8") as f:
            blocos = json.load(f)
    else:
        blocos = []

    novos = 0
    for item in interacoes:
        entrada = f"Pergunta: {item['pergunta']}\nResposta: {item['resposta']}"
        if entrada not in blocos:
            blocos.append(entrada)
            salvar_embedding(entrada, assunto)
            novos += 1

    with open(caminho_knowledge, "w", encoding="utf-8") as f:
        json.dump(blocos, f, indent=2, ensure_ascii=False)

    return f"✅ {novos} entradas aprendidas da memória longa no assunto '{assunto}'."
