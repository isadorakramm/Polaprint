// Recebe o evento 'nova_imagem' enviado pelo servidor
socket.on("nova_imagem", (data) => {
    const fotosDiv = document.getElementById("fotos");

    // Cria a div para a nova imagem
    const novaDiv = document.createElement("div");
    novaDiv.classList.add("polaroid");

    // Adiciona a imagem
    const novaImg = document.createElement("img");
    novaImg.src = data.imagem;  // Caminho da imagem enviado pelo servidor
    novaDiv.appendChild(novaImg);

    // Adiciona um parágrafo vazio para a descrição manual (opcional)
    const descricao = document.createElement("p");
    descricao.textContent = ""; // A descrição será adicionada manualmente
    novaDiv.appendChild(descricao);

    // Adiciona a nova div ao site
    fotosDiv.appendChild(novaDiv);
});
