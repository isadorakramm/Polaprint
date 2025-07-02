from flask import Flask, request
import base64
import os
import banco
import shutil
from datetime import datetime
from seeImage import le_imagem
from image_monitor import ImageMonitor

ime = ImageMonitor()

def get_timestamp():
    """ Retorna a data e hora atual formatada como dd-mm-aaaa hh-mm-ss """
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H-%M-%S")

app = Flask(__name__)

@app.route('/')
def home():
    # Chama o método estático da classe HomePage
    return ime.home()



@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.data
    with open("received_image.jpg", "wb") as file:
        file.write(base64.b64decode(data))
    filename = "imagem"+get_timestamp()+".jpg"
    os.rename("received_image.jpg",filename)
    
    # Verificar se o diretório de destino existe
    diretorio_destino = '\\img'
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)  # Cria o diretório, se não existir
    
    txt = le_imagem(filename)
    
    shutil.move(filename, diretorio_destino)
    
    txt = banco.extrair_palavras_chave(txt)
    txt = banco.encontrar_melhor_resultado(txt)
    txt = txt['poema']
    return txt, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)