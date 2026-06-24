const API = 'http://localhost:8000';

async function carregarChaleAdm() {
    const parametros = new URLSearchParams(window.location.search);
    const id = parametros.get('id');

    const resposta = await fetch(`${API}/chales/${id}`);
    const chale = await resposta.json();
     
    const main = document.getElementById('conteudoAdm');

    const todasFotos = [chale.foto_capa, ...chale.fotos.map(f => f.url)];
    while (todasFotos.length < 6) todasFotos.push(chale.foto_capa);
    const fotosHtml = todasFotos.slice(0, 6)
        .map(url => `<img src="${url}" alt="foto">`)
        .join('');

    main.innerHTML = `
        <div class="cardFotos">
            <div class="cardInfo">
                <h2>${chale.nome}</h2>
                <p>Avaliação: __ / 5.0</p>
            </div>
            <div class="gridFotos">
                ${fotosHtml}
            </div>
        </div>

        <section class="secaoEditar">
            <div class="campoEditar">
                <label>Preço por dia:</label>
                <input type="number" id="novoPreco" value="${chale.val_diaria}">
            </div>
            <div class="campoEditar">
                <label>Descrição:</label>
                <textarea id="novaDescricao">${chale.descricao}</textarea>
            </div>
            <button class="btnSalvar" onclick="salvarEdicao(${chale.id})">Salvar alterações</button>
        </section>

        <section class="secaoPerigo">
            <button class="btnExcluir" onclick="excluirChale(${chale.id})">Excluir Chalé</button>
        </section>
    `;

}

carregarChaleAdm();