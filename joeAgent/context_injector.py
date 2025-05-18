import json
import os
from memory_manager import carregar_short_term
from embedding_engine import classificar_assunto

def carregar_knowledge(assunto):
    caminho = f"knowledge/{assunto}.json"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def montar_prompt_contextual(pergunta, assuntos_disponiveis=["python", "lua"]):
    # Detecta o assunto com base nos embeddings salvos
    assunto = classificar_assunto(pergunta, assuntos_disponiveis)

    # Carrega memória recente (short-term)
    short_term = carregar_short_term()
    if not isinstance(short_term, list):
        short_term = []

    historico = "\n".join([
        f"Usuário: {x.get('pergunta', '')}\nIA: {x.get('resposta', '')}"
        for x in short_term[-5:]
    ])

    # Carrega ensinamentos se o assunto for reconhecido
    conhecimento = []
    if assunto:
        conhecimento = carregar_knowledge(assunto)

    # Monta o prompt completo
    prompt = f"""Você é o joeAgent, um assistente pessoal direto e impessoal para o Pedro.

REGRAS:
- Sempre responda em português do Brasil.
- NÃO use saudações, emojis ou linguagem emocional.
- NÃO trate o usuário como "meu amigo", "olá", ou qualquer coisa parecida.
- Comece com um exemplo de código quando for o caso.
- Depois, use no máximo 2 frases curtas de explicação.
- NÃO repita a pergunta.
- NÃO elogie o usuário.
- NÃO use palavras como "pode", "resultará", "por exemplo".
- Nunca seja informal ou simpático.

Objetivo: ser direto, técnico, seco. Como um terminal de referência técnica."""



    if conhecimento:
        prompt += f"\nAprendizados sobre {assunto}:\n"
        for item in conhecimento:
            prompt += f"- {item}\n"

    if historico:
        prompt += f"\nÚltimas conversas:\n{historico}\n"

    prompt += f"\nNova pergunta do usuário:\n{pergunta}\n"

    return prompt.strip()
