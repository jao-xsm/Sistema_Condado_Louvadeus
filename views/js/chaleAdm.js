const API = 'http://localhost:8000';

async function iniciar() {
    const parametros = new URLSearchParams(window.location.search);
    const id = parametros.get('id');

    if(id){
        carregarChaleAdm(id);
    } else{
        criacaoChaleAdm();
    }
}

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

async function criacaoChaleAdm() {
    const main = document.getElementById('conteudoAdm');
    main.innerHTML = `
        <h2>Adicionar novo Chalé</h2>

        <section class="secaoEditar">
            <div class="campoEditar">
                <label>Nome:</label>
                <input type="text" id="nomeChale" placeholder="Nome do chalé">
            </div>
            <div class="campoEditar">
                <label>Preço por dia:</label>
                <input type="number" id="novoPreco" placeholder="Ex: 350">
            </div>
            <div class="campoEditar">
                <label>Nº de camas:</label>
                <input type="number" id="quantCamas" placeholder="Ex: 2">
            </div>
            <div class="campoEditar">
                <label>Descrição:</label>
                <textarea id="novaDescricao" placeholder="Descreva o chalé..."></textarea>
            </div>
            <div class="campoEditar">
                <label>Foto capa:</label>
                <input type="file" id="fotoCapa" accept="image/*">
            </div>
            <div class="campoEditar">
                <label>Fotos extras:</label>
                <input type="file" id="fotosExtras" accept="image/*" multiple>
            </div>

            <button class="btnSalvar" onclick="criarChale()">
                Adicionar Chalé
            </button>
        </section>
    `
}

async function criarChale() {
    const token = localStorage.getItem('token');
    const nome = document.getElementById('nomeChale').value;
    const camas = document.getElementById('quantCamas').value;
    const preco = document.getElementById('novoPreco').value;
    const descricao = document.getElementById('novaDescricao').value;
    const fotoCapaInput = document.getElementById('fotoCapa');
    const fotosExtrasInput = document.getElementById('fotosExtras');

    let fotoCapaBase64 = "";
    if(fotoCapaInput.files.length > 0){
        fotoCapaBase64 = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.readAsDataURL(fotoCapaInput.files[0]);
        });
    }  //converte ft capa

    const fotosExtrasBase64 = [];
    for (const arquivo of fotosExtrasInput.files){
        const base64 = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.readAsDataURL(arquivo);
        });
        fotosExtrasBase64.push(base64);
    }


    if(!nome || !camas || !preco || !descricao || fotoCapaInput.files.length === 0){
        alert('Preencha todos os campos e adicione uma foto de capa!');
        return;
    }

    if (descricao.length < 15) {
        alert('A descrição deve ter pelo menos 15 caracteres!');
        return;
    }

    const resposta = await fetch(`${API}/chales/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            nome: nome,
            val_diaria: parseFloat(preco),
            quant_camas: parseInt(camas),
            descricao: descricao,
            foto_capa: fotoCapaBase64,
            galeria_fotos: fotosExtrasBase64,
            ativo: true
        })
    });

    const dados = await resposta.json();
    
    if(resposta.ok){
        alert('Chalé criado com sucesso!');
        window.location.href = 'acomodacoes.html';
    } else{
        alert(JSON.stringify(dados.detail) || 'Erro ao criar chalé.');
    }
}

async function salvarEdicao(chaleId) {
    const token = localStorage.getItem('token');
    const novoPreco = document.getElementById('novoPreco').value;
    const novaDescricao = document.getElementById('novaDescricao').value;

    const resposta = await fetch(`${API}/chales/${chaleId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            val_diaria: parseFloat(novoPreco),
            descricao: novaDescricao
        })
    });

    if(resposta.ok){
        alert('Chalé atualizado com sucesso!');
    } else {
        const dados = await resposta.json();
        alert(dados.detail || 'Erro ao atualizar.');
    }
}

async function excluirChale(chaleId) {
    if(!confirm('Tem certeza que deseja excluir esta chalé?')) return;
    
    const token = localStorage.getItem('token');

    const resposta = await fetch(`${API}/chales/${chaleId}`, {
        method: 'DELETE',
        headers: {'Authorization': `Bearer ${token}`}
    });

    if(resposta.ok){
        alert('Chalé excluido com sucesso"');
        window.location.href = 'acomodacoes.html';
    } else{
        const dados = await resposta.json();
        alert(dados.detail || 'Erro ao excluir.');
    }
}

iniciar();