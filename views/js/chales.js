const API = 'http://localhost:8000';

async function carregarChales() {
    const resposta = await fetch(`${API}/chales/`);
    const chales = await resposta.json();
    
    const container = document.getElementById('listaChales');

    chales.forEach((chale, index) => {
        const card = document.createElement('div');
        card.className = 'cardChale';
        if(index %2 !== 0){  //se par inverte ne
            card.classList.add('invertido');
        }
    
        // monta array com ate 6 fotos
        const todasFotos = [chale.foto_capa, ...chale.fotos.map(f => f.url)];
        while (todasFotos.length < 6) {
            todasFotos.push(chale.foto_capa); // preenche com a capa se faltar
        }
        const fotosHtml = todasFotos.slice(0, 6)
            .map(url => `<img src="${url}" alt="foto do chalé">`)
            .join('');

        const tipoUsuario = localStorage.getItem('tipo_usuario');
        const botao = tipoUsuario === 'anfitriao'
            ? `<button class="btnReservarChale" onclick="window.location.href='chaleAdm.html?id=${chale.id}'">Editar</button>`
            : `<button class="btnReservarChale" onclick="window.location.href='chale.html?id=${chale.id}'">Reservar agora</button>`;

        card.innerHTML = `
            <div class="cardInfo">
                <h3>${chale.nome}</h3>
                ${botao}
                <p class="cardAvaliacao">Avaliação: __ / 5.0</p>
            </div>
            <div class="gridFotos">
                ${fotosHtml}
            </div>
        `;  //corpo do html

        container.appendChild(card);
    }); //criando um novo chal
}
carregarChales();