import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Carrega o modelo (o mais leve, rápido e bom)
modelo = SentenceTransformer('all-MiniLM-L6-v2')

EMBED_PATH = "embeddings"

def gerar_embedding(texto):
    return modelo.encode([texto])[0].tolist()

def salvar_embedding(texto, assunto):
    vetor = gerar_embedding(texto)
    caminho = os.path.join(EMBED_PATH, f"{assunto}.json")

    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = []

    dados.append({"texto": texto, "embedding": vetor})

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def buscar_similares(texto, assunto, top_k=3):
    caminho = os.path.join(EMBED_PATH, f"{assunto}.json")
    if not os.path.exists(caminho):
        return []

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    vetores = [d["embedding"] for d in dados]
    textos = [d["texto"] for d in dados]

    entrada = gerar_embedding(texto)
    sim = cosine_similarity([entrada], vetores)[0]
    indices = np.argsort(sim)[::-1][:top_k]

    return [{"texto": textos[i], "similaridade": float(sim[i])} for i in indices]

def classificar_assunto(texto, assuntos_disponiveis):
    melhores = []
    for assunto in assuntos_disponiveis:
        similares = buscar_similares(texto, assunto, top_k=1)
        if similares:
            melhores.append((assunto, similares[0]["similaridade"]))

    if not melhores:
        return None

    melhores.sort(key=lambda x: x[1], reverse=True)
    return melhores[0][0] if melhores[0][1] > 0.4 else None  # ajustável
