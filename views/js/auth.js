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
    } else {
        alert('Erro ao carregar perfil. Faça login novamente.');
        window.location.href = 'login.html';
    }

    

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
        lista.innerHTML += `
            <div class="cardReserva">
                <p><strong>Chalé:</strong> ${r.chale_id}</p>
                <p><strong>Check-in:</strong> ${r.data_checkin}</p>
                <p><strong>Check-out:</strong> ${r.data_checkout}</p>
                <p><strong>Status:</strong> ${r.status}</p>
            </div>
        `;
    });
}

async function salvarPerfil() {
    const token = localStorage.getItem('token');
    const nome = document.getElementById('nome').value;
    const telefone = document.getElementById('telefone').value;
    const senha = document.getElementById('senha').value;
    const fotoInput = document.getElementById('foto');

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
        carregarPerfil();
    } else {
        alert(dados.detail || 'Erro ao atualizar perfil.');
    }
}

function logout(){
    localStorage.removeItem('token');
    localStorage.removeItem('tipo_usuario'); // limpa p sair
    window.location.href = 'index.html';
}