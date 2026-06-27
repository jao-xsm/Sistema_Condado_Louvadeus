const API = 'http://localhost:8000';

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

        <section class="secaoDescricao">
            <h3>Descrição</h3>
            <p>${chale.descricao}</p>
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
    `;
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

carregarChale();