from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
import cv2
from PIL import Image
import unicodedata
import requests
import io

#from google.cloud import translate_v2 as translate
from googletrans import Translator

def traduzir(texto_em_ingles):
    tradutor = Translator()
    traducao = tradutor.translate(texto_em_ingles, src='en', dest='pt')
    return traducao.text

def remover_acentos(frase):
    return ''.join(
        c for c in unicodedata.normalize('NFD', frase)
        if unicodedata.category(c) != 'Mn'
    )
 
def gerar_poema(descricoes):
    modelo = pipeline('text-generation', model='gpt2')
    prompt = f"Write a poem about this description:  "
    tamanho = len(prompt)
    prompt += f"{descricoes}"
    poema = modelo(prompt, max_length=100)
    return poema[0]['generated_text'][tamanho:]
    

def le_imagem(caminho_imagem):
    print(caminho_imagem)
    # Carregar o modelo e o processador
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # Carregar a imagem (use uma URL ou caminho local)
    #image_url = "https://media.istockphoto.com/id/1284641915/photo/a-stray-dog-on-the-street-looks-with-sad-eyes.jpg?s=612x612&w=0&k=20&c=JFO1UIl7TxdSCqii8lFp_-KLzt-u2nQN-CNpSv9DtzM="
    #image = Image.open(requests.get(image_url, stream=True).raw)
    image = Image.open(caminho_imagem)

    # Processar a imagem e gerar a legenda
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    #poema = gerar_poema(description)
    #poema = traduzir_texto(description)
    descricao = traduzir(description)
    print(f"Descrição da imagem: {description}")
    
    return f'{remover_acentos(descricao)}'
  

