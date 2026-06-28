const API = 'http://localhost:8000';

const tipoUsuario = localStorage.getItem('tipo_usuario');

async function carregarChales() {
    const resposta = await fetch(`${API}/chales/`);
    const chales = await resposta.json();
    
    const container = document.getElementById('listaChales');

    for (const [index, chale] of chales.entries()) {
        const card = document.createElement('div');
        card.className = 'cardChale';
        if (index % 2 !== 0){
            card.classList.add('invertido');
        }

        const todasFotos = [chale.foto_capa, ...chale.fotos.map(f => f.url)];
        while (todasFotos.length < 6) todasFotos.push(chale.foto_capa);
        const fotosHtml = todasFotos.slice(0, 6)
            .map(url => `<img src="${url}" alt="foto do chalé">`)
            .join('');

        const botao = tipoUsuario === 'anfitriao'
            ? `<button class="btnReservarChale" onclick="window.location.href='chaleAdm.html?id=${chale.id}'">Editar</button>`
            : `<button class="btnReservarChale" onclick="window.location.href='chale.html?id=${chale.id}'">Reservar agora</button>`;

        let mediaAvaliacao = '--';
        try {
            const respostaMedia = await fetch(`${API}/avaliacoes/chale/${chale.id}/media`);
            if (respostaMedia.ok) {
                const dadosMedia = await respostaMedia.json();
                mediaAvaliacao = dadosMedia.media ?? '--';
            }
        } catch (e) {}

        card.innerHTML = `
            <div class="cardInfo">
                <h3>${chale.nome}</h3>
                ${botao}
                <p class="cardAvaliacao">Avaliação: ${mediaAvaliacao} / 5.0</p>
            </div>
            <div class="gridFotos">
                ${fotosHtml}
            </div>
        `;
        container.appendChild(card);
    }

    if(tipoUsuario === 'anfitriao'){
        const btnAdd = document.createElement('div');
        btnAdd.style.textAlign = 'center';
        btnAdd.innerHTML = `
            <button class="btnReservarChale" onclick="window.location.href = 'chaleAdm.html'">
                Adicionar novo Chalé
            </button>
        `;
        container.appendChild(btnAdd);
    }

}
carregarChales();