const API = 'http://localhost:8000';

let mesCalendario = new Date().getMonth();
let anoCalendario = new Date().getFullYear();
let datasOcupadas = [];

const meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
const diasSemana = ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];

async function carregarChale() {
    const parametros = new URLSearchParams(window.location.search);
    const id = parametros.get('id');

    const resposta = await fetch(`${API}/chales/${id}`);
    const chale = await resposta.json();
    

    const main = document.getElementById('conteudoChale');

    const todasFotos = [chale.foto_capa, ...chale.fotos.map(f => f.url)];
    while (todasFotos.length < 6) {
        todasFotos.push(chale.foto_capa);
    }
    const fotosHtml = todasFotos.slice(0, 6)
        .map(url => `<img src="${url}" alt="foto">`)
        .join('');

    let mediaAvaliacao = '--';   // busca média de avaliação
    try {
        const respostaMedia = await fetch(`${API}/avaliacoes/chale/${chale.id}/media`);
        if (respostaMedia.ok) {
            const dadosMedia = await respostaMedia.json();
            mediaAvaliacao = dadosMedia.media ?? '--';
        }
    } catch (e) {}

    main.innerHTML = `
        <div class="cardFotos">
            <div class="cardInfo">
                <h2>${chale.nome}</h2>
                <p>Avaliação: ${mediaAvaliacao} / 5.0</p>
            </div>
            <div class="gridFotos">
                ${fotosHtml}
            </div>
        </div>

        <section class="secaoDescricao">
            <h3>Descrição</h3>
            <p>${chale.descricao}</p>
        </section>

        <section class="secaoCalendario">
            <h3>Disponibilidade</h3>
            <div class="calendarioNav">
                <button onclick="mudarMesChale(-1)">← Anterior</button>
                <span id="mesAnoChale"></span>
                <button onclick="mudarMesChale(1)">Próximo →</button>
            </div>
            <div class="legendaCalendario">
                <span class="legenda livre">Disponível</span>
                <span class="legenda ocupado">Ocupado</span>
            </div>
            <div class="calendarioGrid" id="calendarioChale"></div>
        </section>

        <section class="secaoReserva">
            <div class="campoReserva">
                <label for="checkin">Check-in:</label>
                <input type="date" id="checkin" onchange="calcularTotal(${chale.val_diaria})">
            </div>

            <div class="campoReserva">
                <label for="checkout">Check-out:</label>
                <input type="date" id="checkout" onchange="calcularTotal(${chale.val_diaria})">
            </div>

            <p class="totalReserva">Total: <span id="totalValor">--</span></p>
            <button class="btnConfirmar" onclick="confirmarReserva(${chale.id}, ${chale.val_diaria})">
                Reservar
            </button>
        </section>

        <section id="secaoAvaliacoes">
            
        </section>
    `;
    carregarDisponibilidade(chale.id);
    carregarAvaliacoes(chale.id);
}

async function carregarDisponibilidade(chaleId) {
    const resposta = await fetch(`${API}/reservas/chale/${chaleId}/disponibilidade`);
    const reservas = await resposta.json();
    
    datasOcupadas = [];
    reservas.forEach(r => {
        let atual = new Date(r.data_checkin + 'T00:00:00');
        const fim = new Date(r.data_checkout + 'T00:00:00');
        while (atual < fim) {
            datasOcupadas.push(atual.toISOString().split('T')[0]);
            atual.setDate(atual.getDate() + 1);
        }
    });
    renderizarCalendarioChale();
}
function renderizarCalendarioChale() {
    const grid = document.getElementById('calendarioChale');
    const titulo = document.getElementById('mesAnoChale');

    titulo.textContent = `${meses[mesCalendario]} ${anoCalendario}`;
    grid.innerHTML = '';

    diasSemana.forEach(dia => {
        const cell = document.createElement('div');
        cell.className = 'diaSemana';
        cell.textContent = dia;
        grid.appendChild(cell);
    });

    const primeiroDia = new Date(anoCalendario, mesCalendario, 1).getDay();
    const totalDias = new Date(anoCalendario, mesCalendario + 1, 0).getDate();
    const hoje = new Date().toISOString().split('T')[0];

    for (let i = 0; i < primeiroDia; i++) {
        const vazio = document.createElement('div');
        vazio.className = 'diaChale vazio';
        grid.appendChild(vazio);
    }
    for (let d = 1; d <= totalDias; d++) {
        const cell = document.createElement('div');
        const dataStr = `${anoCalendario}-${String(mesCalendario + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
        const ocupado = datasOcupadas.includes(dataStr);
        const passado = dataStr < hoje;

        cell.className = `diaChale ${ocupado ? 'ocupado' : passado ? 'passado' : 'livre'}`;
        cell.innerHTML = `<div class="diaNumero">${d}</div>`;
        grid.appendChild(cell);
    }
}
function mudarMesChale(direcao) {
    mesCalendario += direcao;
    if (mesCalendario > 11) { mesCalendario = 0; anoCalendario++; }
    if (mesCalendario < 0) { mesCalendario = 11; anoCalendario--; }
    renderizarCalendarioChale();
}

async function confirmarReserva(chaleId, valorDiaria) {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Você precisa estar logado para fazer uma reserva!');
        window.location.href = 'login.html';
        return;
    }

    const checkin = document.getElementById('checkin').value;
    const checkout = document.getElementById('checkout').value;
    const diaAtual = new Date().toISOString().split('T')[0];

    if (!checkin || !checkout) {
        alert('Escolha as datas de check-in e check-out!');
        return;
    }
    if(checkin < diaAtual){
        alert('Não é possivel reservar uma data no passado!');
        return;
    }
    if (checkout <= checkin) {
        alert('A data de check-out deve ser depois do check-in!');
        return;
    }

    const resposta = await fetch(`${API}/reservas/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            chale_id: chaleId,
            data_checkin: checkin,
            data_checkout: checkout
        })
    });

    const dados = await resposta.json();
    if (resposta.ok) {
        alert('Reserva realizada com sucesso!');
        window.location.href = 'perfil.html';
    } else {
        alert(dados.detail || 'Erro ao realizar reserva.');
    }
}

function calcularTotal(valorDiaria) {
    const checkin = document.getElementById('checkin').value;
    const checkout = document.getElementById('checkout').value;

    if (checkin && checkout && checkout > checkin) {
        const dias = Math.round((new Date(checkout) - new Date(checkin)) / (1000 * 60 * 60 * 24));
        document.getElementById('totalValor').textContent = 
            `${dias} noite${dias > 1 ? 's' : ''} × R$ ${valorDiaria} = R$ ${dias * valorDiaria}`;
    }
}

async function carregarAvaliacoes(chaleId){
    const respostaMedia = await fetch(`${API}/avaliacoes/chale/${chaleId}/media`);
    const media = await respostaMedia.json();
    const respostaComentarios = await fetch(`${API}/avaliacoes/chale/${chaleId}/lista`);
    const comentarios = await respostaComentarios.json();
    const secao = document.getElementById('secaoAvaliacoes');

    const comentariosHtml = comentarios.length === 0 ? '<p>Ainda não há nenhuma avaliação.</p>' : comentarios.map(
        a => `
            <div class="cardAvaliacao">
                <p class="notaAvaliacao">Avaliação: ${a.nota} / 5.0</p>
                <p>${a.comentario || ''}</p>
            </div>
        `).join('');

    secao.innerHTML = `
        <h3>Avaliações</h3>
        <p class="mediaGeral">Média: ${media.media ?? '--'} / 5.0</p>
        ${comentariosHtml}
    `;
}

carregarChale();