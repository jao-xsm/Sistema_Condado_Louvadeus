const API = 'http://localhost:8000';
// endereço do API

// (async function) func p esperar resposta do servidor
async function fazerLogin() {
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    if(!email || !senha){
        alert('Preencha todos os campos!');
        return;
    }

    //fetch -> manda os dados p o servidor
    const resposta = await fetch(`${API}/usuarios/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({
            email: email, 
            senha: senha})
    });

    const dados = await resposta.json();

    if (resposta.ok) {
        localStorage.setItem('token', dados.access_token);  // salva o token no navegador p usar nas outras paginas
        localStorage.setItem('tipo_usuario', dados.tipo_usuario);
        window.location.href = 'index.html';   //redireciona p outra pagina
    } else {
        alert(dados.detail);
        //erro falha de login, mostra mensagem de erro do servidor
    }
}

async function cadastrar() {
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const telefone = document.getElementById('telefone').value;
    const data = document.getElementById('dataNt').value;
    const fotoInput = document.getElementById('foto');

    if(!nome || !email || !senha || !telefone || !data){
        alert('Preencha todos os campos obrigatórios!');
        return;
    }

    // converte a foto para base64 se tiver sido escolhida
    let fotoBase64 = null;
    if (fotoInput.files.length > 0) {
        const arquivo = fotoInput.files[0];
        fotoBase64 = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.readAsDataURL(arquivo);
        });
    }

    const resposta = await fetch(`${API}/usuarios/cadastro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({
            nome: nome,
            email: email,
            senha: senha,
            telefone: telefone,
            data_nascimento: data,
            foto: fotoBase64
        })
    });

    const dados = await resposta.json();

    if(resposta.ok){
        alert('Cadastro realizado com sucesso!');
        window.location.href = 'login.html';
    } else {
        alert (dados.detail);
    }
}

async function carregarPerfil() {
    const token = localStorage.getItem('token');
    
    const resposta = await fetch(`${API}/usuarios/me`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    const dados = await resposta.json();

    if (resposta.ok){
        document.getElementById('nome').value = dados.nome;
        document.getElementById('email').value = dados.email;
        document.getElementById('telefone').value = dados.telefone || '';
        document.getElementById('dataNt').value = dados.data_nascimento;
        const fotoAtual = document.getElementById('fotoAtual');
        if(dados.foto){
            fotoAtual.src = dados.foto;
        }
        const nomeAdm = document.getElementById('nomeAdm');
        if (nomeAdm) {
            nomeAdm.value = dados.nome;
            document.getElementById('emailAdm').value = dados.email;
            document.getElementById('telefoneAdm').value = dados.telefone || '';
            document.getElementById('dataNtAdm').value = dados.data_nascimento || '';
            const fotoAdm = document.getElementById('fotoAtualAdm');
            if (dados.foto) fotoAdm.src = dados.foto;
        }
    } else {
        alert('Erro ao carregar perfil. Faça login novamente.');
        window.location.href = 'login.html';
    }
}

async function salvarPerfil() {
    const token = localStorage.getItem('token');
    const tipo = localStorage.getItem('tipo_usuario');

    const prefixo = tipo == 'anfitriao' ? 'Adm' : '';

    const nome = document.getElementById(`nome${prefixo}`).value;
    const telefone = document.getElementById(`telefone${prefixo}`).value;
    const senha = document.getElementById(`senha${prefixo}`).value;
    const fotoInput = document.getElementById(`foto${prefixo}`);

    let fotoBase64 = null;
    if(fotoInput.files.length > 0){
        const arquivo = fotoInput.files[0];
        fotoBase64 = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.readAsDataURL(arquivo);
        })
    }

    const corpo = {};
    if(nome) corpo.nome = nome;
    if(telefone) corpo.telefone = telefone;
    if(senha && senha.trim() != '') corpo.senha = senha;
    if(fotoBase64) corpo.foto_url = fotoBase64;

    if(Object.keys(corpo).length === 0){
        alert('Nenhuma alteração feita!');
        return;
    }

    const resposta = await fetch(`${API}/usuarios/perfil`, {
        method: 'PATCH',
        headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(corpo)
    });

    const dados = await resposta.json();

    if (resposta.ok) {
        alert('Perfil atualizado com sucesso!');
        setTimeout(() => carregarPerfil(), 500);
    } else {
        alert(dados.detail || 'Erro ao atualizar perfil.');
    }
}

function logout(){
    localStorage.removeItem('token');
    localStorage.removeItem('tipo_usuario'); // limpa p sair
    window.location.href = 'index.html';
}

async function carregarReservas() {
    const token = localStorage.getItem('token');
    const resposta = await fetch(`${API}/reservas/`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    const reservas = await resposta.json();
    const lista = document.getElementById('listaReservas');
    if (!resposta.ok || reservas.length === 0) {
        lista.innerHTML = '<p>Nenhuma reserva encontrada.</p>';
        return;
    }

    lista.innerHTML = '';
    reservas.forEach(r => {
        const podeCancelar = r.status !== 'CANCELADA' && r.status !== 'FINALIZADA';
        const podeAvaliar = r.status === 'Concluída';

        lista.innerHTML += `
            <div class="cardReserva">
                <p><strong>Chalé:</strong> ${r.chale_id}</p>
                <p><strong>Check-in:</strong> ${formatacaoData(r.data_checkin)}</p>
                <p><strong>Check-out:</strong> ${formatacaoData(r.data_checkout)}</p>
                <p><strong>Status:</strong> ${r.status}</p>
                <p><strong>Total:</strong> R$ ${r.valor_total}</p>
                <div class="botoesReserva">
                    ${podeCancelar ? `
                        <button class="btnEditarReserva" onclick="abrirEdicaoReserva(${r.id}, '${r.data_checkin}', '${r.data_checkout}')">Editar datas </button>
                        <button class="btnCancelarReserva" onclick="cancelarReserva(${r.id})">Cancelar reserva </button>  
                    ` : ''}
                    ${podeAvaliar ? `
                        <button class= "btnAvaliarReserva" onclick="abrirAvaliacaoReserva(${r.chale_id})">Avaliar estadia</button>    
                    ` : ''}
                </div>
            </div>
        `;
    });
}

function abrirAvaliacaoReserva(chaleId) {
    document.getElementById('modalChaleId').value = chaleId;
    document.getElementById('modalNota').value = '';
    document.getElementById('modalComentario').value = '';
    document.getElementById('overlayAvaliacao').classList.remove('hidden');
}
function fecharModalAvaliacao() {
    document.getElementById('overlayAvaliacao').classList.add('hidden');
}
async function enviarAvaliacao() {
    const token = localStorage.getItem('token');
    const chaleId = document.getElementById('modalChaleId').value;
    const nota = document.getElementById('modalNota').value;
    const comentario = document.getElementById('modalComentario').value;

    if (!nota || nota < 1 || nota > 5) {
        alert('Dê uma nota de 1 a 5!');
        return;
    }

    const resposta = await fetch(`${API}/avaliacoes/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            chale_id: parseInt(chaleId),
            nota: parseInt(nota),
            comentario: comentario || null
        })
    });

    const dados = await resposta.json();
    if (resposta.ok) {
        alert('Avaliação enviada com sucesso!');
        fecharModalAvaliacao();
    } else {
        alert(dados.detail || 'Erro ao enviar avaliação.');
    }
}

async function cancelarReserva(reservaId){
    if (!confirm('Tem certeza que deseja cancelar esta reserva?')) return;

    const token = localStorage.getItem('token');
    const resposta = await fetch(`${API}/reservas/${reservaId}/cancelar`, {
        method: 'PATCH',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    const dados = await resposta.json();
    if (resposta.ok) {
        alert('Reserva cancelada com sucesso!');
        carregarReservas(); // att a lista
    } else {
        alert(dados.detail || 'Erro ao cancelar reserva.');
    }
}

function abrirEdicaoReserva(reservaId, checkinAtual, checkoutAtual){
    document.getElementById('modalReservaId').value = reservaId;
    document.getElementById('modalCheckin').value = checkinAtual;
    document.getElementById('modalCheckout').value = checkoutAtual;
    document.getElementById('overlayEdicao').classList.remove('hidden');
}
async function confirmarEdicaoReserva() {
    const reservaId = document.getElementById('modalReservaId').value;
    const checkin = document.getElementById('modalCheckin').value;
    const checkout = document.getElementById('modalCheckout').value;
    const diaAtual = new Date().toISOString().split('T')[0];

    if (!checkin || !checkout) {
        alert('Preencha as duas datas!');
        return;
    }
    if(checkin < diaAtual){
        alert('Não é possivel reservar uma data no passado!');
        return;
    }
    if (checkout <= checkin) {
        alert('Check-out deve ser depois do check-in!');
        return;
    }
    await editarReserva(reservaId, checkin, checkout);
    fecharModalEdicao();
}
function fecharModalEdicao() {
    document.getElementById('overlayEdicao').classList.add('hidden');
}

async function editarReserva(reservaId, checkin, checkout) {
    const token = localStorage.getItem('token');
    const resposta = await fetch(`${API}/reservas/${reservaId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            data_checkin: checkin,
            data_checkout: checkout
        })
    });

    const dados = await resposta.json();
    if (resposta.ok) {
        alert('Reserva atualizada com sucesso!');
        carregarReservas();
    } else {
        alert(dados.detail || 'Erro ao editar reserva.');
    }
}

function formatacaoData(dataStr) {
    const [ano, mes, dia] = dataStr.split('-');
    return `${dia}/${mes}/${ano}`;
}