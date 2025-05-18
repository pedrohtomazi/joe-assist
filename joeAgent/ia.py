import requests
from memory_manager import adicionar_interacao
from context_injector import montar_prompt_contextual

def process_prompt(prompt):
    try:
        # Injeta memória, conhecimento, histórico
        contexto = montar_prompt_contextual(prompt)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "dolphin-mistral",
                "system": "Você é o joeAgent, um assistente pessoal técnico e direto. Responda sempre em português do Brasil. Comece com código sempre que possível, use no máximo 2 frases explicando. Nunca use emojis, saudações ou floreios.",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            return f"[Erro] Resposta do modelo falhou: {response.text}"

        data = response.json()
        resposta = data.get("response", "").strip()

        adicionar_interacao(prompt, resposta)
        return resposta

    except requests.exceptions.RequestException as e:
        return f"[Erro de conexão com o Ollama]: {str(e)}"

    except Exception as e:
        return f"[Erro inesperado]: {str(e)}"
