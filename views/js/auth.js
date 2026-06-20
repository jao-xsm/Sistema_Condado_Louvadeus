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