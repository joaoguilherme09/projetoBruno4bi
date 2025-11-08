O Cofre de Doces Criptografado é um aplicativo feito com CustomTkinter, MongoDB e criptografia Fernet.
Ele permite adicionar, atualizar e remover doces guardados por crianças, mantendo os dados seguros e criptografados.
Tudo é armazenado em um banco de dados MongoDB na nuvem, com interface moderna e interativa.

⚙️ Tecnologias Utilizadas

🐍 Python 3.11+

🧱 MongoDB Atlas (banco de dados na nuvem)

🔐 Criptografia Fernet (para proteger os tipos de doces)

🖥️ CustomTkinter (interface gráfica moderna)

------------------------------------------------------------------------------------------------------------------------------------------------------

🧠 Como o Código Funciona

🔑 Criptografia:
Os tipos de doces são criptografados antes de serem salvos no banco, garantindo que ninguém veja o conteúdo sem a chave secreta (chave.key).

☁️ Banco de Dados:
Os dados são salvos em uma coleção do MongoDB chamada CofreDeDoces.

🧱 Interface Gráfica:
Usa CustomTkinter com tema escuro e botões personalizados, criando uma experiência moderna e intuitiva.


funções e suas ações:
adicionar_ou_atualizar() → adiciona ou atualiza um doce

listar_doces() → lista todos os doces cadastrados

deletar_doce() → remove um item do cofre

criptografar() e descriptografar() → protegem os dados sensíveis

------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Como Executar o Projeto
1️⃣ Instale as dependências:

No terminal, dentro da pasta do projeto, digite:

pip install customtkinter pymongo cryptography pillow

2️⃣ Configure o Banco de Dados:

O código já vem com uma conexão padrão:

exemplo:
cliente = MongoClient("mongodb+srv://root:joao20012009@projetobruno.xwma2xg.mongodb.net/")

3️⃣ Rode o Programa:

Execute o arquivo principal:

python cofre_doces.py

4️⃣ Use a Interface:

Preencha o nome da criança 👧

O tipo de doce 🍫

E a quantidade 🍭

Clique em “Salvar no Cofre” para guardar os dados.

Você pode editar ou excluir doces a qualquer momento.

------------------------------------------------------------------------------------------------------------------------------------------------------

