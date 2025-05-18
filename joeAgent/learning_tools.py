import os
import json
import fitz  # PyMuPDF
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract
import torch
import io
from embedding_engine import salvar_embedding

# Carrega modelo BLIP uma única vez
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def interpretar_imagem_bytes(imagem_bytes):
    imagem = Image.open(io.BytesIO(imagem_bytes)).convert("RGB")
    texto_ocr = pytesseract.image_to_string(imagem, lang="por")

    inputs = processor(images=imagem, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs)
    legenda = processor.decode(output[0], skip_special_tokens=True)

    return texto_ocr.strip(), legenda.strip()

def extrair_texto_pdf_com_interpretacao(caminho_pdf):
    texto_total = ""

    with fitz.open(caminho_pdf) as doc:
        for i, pagina in enumerate(doc):
            texto_total += pagina.get_text()

            for img_index, img in enumerate(pagina.get_images(full=True)):
                base_image = doc.extract_image(img[0])
                imagem_bytes = base_image["image"]
                texto_ocr, legenda = interpretar_imagem_bytes(imagem_bytes)

                bloco = f"[Imagem na página {i+1}]\nTexto OCR: {texto_ocr}\nLegenda IA: {legenda}\n"
                texto_total += "\n" + bloco

    return texto_total.strip()

def learning_from_archive(nome_arquivo, assunto):
    caminho = os.path.expanduser(f"~/Downloads/{nome_arquivo}")

    if not os.path.exists(caminho):
        return f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta Downloads."

    ext = os.path.splitext(caminho)[1].lower()

    try:
        if ext == ".txt":
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
        elif ext == ".pdf":
            conteudo = extrair_texto_pdf_com_interpretacao(caminho)
        else:
            return f"❌ Formato '{ext}' não suportado. Use .txt ou .pdf"
    except Exception as e:
        return f"❌ Erro ao ler o arquivo: {str(e)}"

    blocos = [b.strip() for b in conteudo.split("\n\n") if b.strip()]
    caminho_knowledge = f"knowledge/{assunto}.json"

    if os.path.exists(caminho_knowledge):
        with open(caminho_knowledge, "r", encoding="utf-8") as f:
            conhecimentos = json.load(f)
    else:
        conhecimentos = []

    novos = 0
    for bloco in blocos:
        if bloco not in conhecimentos:
            conhecimentos.append(bloco)
            salvar_embedding(bloco, assunto)
            novos += 1

    with open(caminho_knowledge, "w", encoding="utf-8") as f:
        json.dump(conhecimentos, f, indent=2, ensure_ascii=False)

    return f"✅ {novos} blocos aprendidos de '{nome_arquivo}' no assunto '{assunto}'."
