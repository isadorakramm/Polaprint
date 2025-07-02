import os
import time

class ImageMonitor:
    def __init__(self, image_folder= r'C:\Users\Isadora\Documents\GitHub\server'):
        #self.socketio = socketio
        self.image_folder = image_folder  # Caminho da pasta monitorada
        self.last_seen_images = set()  # Imagens já vistas
        self.count=0

    def get_images(self):
        # Lista apenas arquivos com extensões de imagem no diretório monitorado
        return {img for img in os.listdir(self.image_folder) if img.lower().endswith(('jpg', 'jpeg', 'png'))}

    def monitor_new_images(self):
        # Obtem as imagens atuais no diretório
        current_images = self.get_images()

        # Identifica novas imagens
        new_images = current_images - self.last_seen_images

        #for img in new_images:
        #    # Envia uma mensagem para o cliente via SocketIO
        #    self.socketio.emit('new_image', {'image_path': os.path.join(self.image_folder, img)})

        # Atualiza a lista de imagens vistas
        self.last_seen_images = current_images
        return self.last_seen_images
 

    def home(self):
        self.count += 1
        

        # Gera o conteúdo dinâmico das imagens
        content = "".join(
            f"""
            <div class="polaroid">
                <img src="Imagens/foto{i}.jpg" alt="Foto {i}">
                <p>alguma coisa{i}</p>
            </div>
            """ for i in range(1, self.count + 1)
        )

        # Carrega o HTML base
        with open("C:\\Users\\Isadora\\Documents\\GitHub\\Polaprint\\index.html", "r") as file:
            html_template = file.read()

        # Insere o conteúdo dinâmico no template
        return render_template_string(html_template, content=content)