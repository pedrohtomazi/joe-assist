import os
import json

def limpar_conhecimento(caminho):
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return

    with open(caminho, "r", encoding="utf-8") as f:
        raw = f.read().replace("\\u0000", "").replace("\\x00", "")
        try:
            dados = json.loads(raw)
        except Exception as e:
            print(f"Erro ao carregar JSON: {e}")
            return

    if not isinstance(dados, list):
        print("Formato inválido. Esperado: lista de blocos.")
        return

    limpos = [b for b in dados if isinstance(b, str) and "\\u0000" not in b and "\\x00" not in b]

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(limpos, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(limpos)} blocos salvos em {caminho} (limpeza concluída)")

if __name__ == "__main__":
    caminho = "knowledge/python.json"  # você pode trocar isso
    limpar_conhecimento(caminho)
