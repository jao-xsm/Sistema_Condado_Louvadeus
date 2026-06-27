const API = 'http://localhost:8000';

let mesAtual = new Date().getMonth();
let anoAtual = new Date().getFullYear();
let reservas = []; // p ser preenchido pela API depois

const meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
const diasSemana = ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];

function renderizarCalendario() {
    const grid = document.getElementById('calendarioGrid');
    const titulo = document.getElementById('mesAno');

    titulo.textContent = `${meses[mesAtual]} ${anoAtual}`;
    grid.innerHTML = '';

    // cabeçalho com os dias da semana
    diasSemana.forEach(dia => {
        const cell = document.createElement('div');
        cell.className = 'diaSemana';
        cell.textContent = dia;
        grid.appendChild(cell);
    });

    const primeiroDia = new Date(anoAtual, mesAtual, 1).getDay();
    const totalDias = new Date(anoAtual, mesAtual + 1, 0).getDate();
    const hoje = new Date();

    // células vazias antes do primeirodia
    for (let i = 0; i < primeiroDia; i++) {
        const vazio = document.createElement('div');
        vazio.className = 'dia vazio';
        grid.appendChild(vazio);
    }

    for (let d = 1; d <= totalDias; d++) {
        const cell = document.createElement('div');
        cell.className = 'dia';

        if (d === hoje.getDate() && mesAtual === hoje.getMonth() && anoAtual === hoje.getFullYear()) {
            cell.classList.add('hoje');
        }   // marca o dia de hoje

        const dataStr = `${anoAtual}-${String(mesAtual + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;

        const reservasDoDia = reservas.filter(r => {   
            return dataStr >= r.data_checkin && dataStr < r.data_checkout;
        });   // verifica reservas nesse dia

        cell.innerHTML = `<div class="diaNumero">${d}</div>`;
        reservasDoDia.forEach(r => {
            cell.innerHTML += `<div class="reservaTag">Chalé ${r.chale_id}</div>`;
        });
        grid.appendChild(cell);
    }
}

function mudarMes(direcao) {
    mesAtual += direcao;
    if (mesAtual > 11) {
        mesAtual = 0; 
        anoAtual++; 
    }
    if (mesAtual < 0){
        mesAtual = 11;
        anoAtual--; 
    }
    renderizarCalendario();
}

async function carregarReservas() {
    const token = localStorage.getItem('token');
    const resposta = await fetch(`${API}/reservas/todas`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    reservas = await resposta.json();
    renderizarCalendario();
}

carregarReservas();