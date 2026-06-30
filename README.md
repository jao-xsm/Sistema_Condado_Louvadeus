<div align="center">
  <h1> Condado Louvadeus</h1>
  <h3>Sistema de Gerenciamento de Hospedagens</h3>
  <p>Trabalho Acadêmico de Modelagem de Sistemas</p>
</div>

---

##  Autores
* **João Victor Soares Monteiro** (Matrícula: 202465046AB) - *Back-end (Python/FastAPI, PostgreSQL)*
* **Manuela Grimaldi Hansel** (Matrícula: 202465063AB) - *Front-end (HTML5, CSS3, JavaScript)*

---

##  Sobre o Projeto
O **Condado Louvadeus** é um sistema completo de reservas de chalés, inspirado em plataformas como o Airbnb. Desenvolvido como projeto prático para a disciplina de Modelagem de Sistemas, o software abrange desde a interface com o usuário até a persistência de dados em nuvem, garantindo segurança, validações rigorosas e regras de negócio inteligentes.

---

##  Arquitetura e Tecnologias

O projeto foi estruturado utilizando o padrão arquitetural **MVC (Model-View-Controller)** adaptado para APIs RESTful, garantindo a separação de responsabilidades.

### Stack Tecnológica:
* **Linguagem Back-end:** Python 3
* **Framework Web:** FastAPI (com Uvicorn como servidor ASGI)
* **Banco de Dados:** PostgreSQL (Hospedado na nuvem via Neon)
* **ORM:** SQLAlchemy
* **Validação de Dados:** Pydantic V2
* **Segurança e Autenticação:**
  * JWT (JSON Web Tokens) via `PyJWT` para controle de sessão inviolável.
  * Hashing de senhas via `passlib` (Bcrypt) atendendo a requisitos não-funcionais de segurança.
* **Front-end:** HTML5, CSS3 e JavaScript puro.

> ** Nota sobre o Banco de Dados:** A migração do planejamento inicial em SQLite para o **PostgreSQL** na nuvem foi decidida para suportar concorrência de acessos (evitando *database is locked*) e garantir a integridade das transações de reservas simulando um ambiente real de produção.

---
