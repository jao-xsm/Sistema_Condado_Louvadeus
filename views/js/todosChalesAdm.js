const API = 'http://localhost:8000';

const tipoUsuario = localStorage.getItem('tipo_usuario');

async function carregarChales() {
    const token = localStorage.getItem('token');
    const resposta = await fetch(`${API}/chales/todos`, {
        headers: { 'Authorization': `Bearer ${token}`}
    });
    const chales = await resposta.json();
    if (!resposta.ok) {
        console.log('Erro:', chales);
        return;
    }
    
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

        if (!chale.ativo) {
            card.classList.add('inativo');
        }

        card.innerHTML = `
            <div class="cardInfo">
                <h3>${chale.nome}</h3>
                ${!chale.ativo ? '<span class="tagInativo">Indisponível</span>' : ''}
                <button class="btnReservarChale" onclick="window.location.href='chaleAdm.html?id=${chale.id}'">Editar</button>
                <p class="cardAvaliacao">Avaliação: __ / 5.0</p>
            </div>
            <div class="gridFotos">
                ${fotosHtml}
            </div>
        `;

        container.appendChild(card);
    });

    const btnAdd = document.createElement('div');
    btnAdd.style.textAlign = 'center';
    btnAdd.innerHTML = `
        <button class="btnReservarChale" onclick="window.location.href = 'chaleAdm.html'">
            Adicionar novo Chalé
        </button>
    `;
    container.appendChild(btnAdd);

}
carregarChales();