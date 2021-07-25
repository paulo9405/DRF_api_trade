<h2>INSTRUNÇÕES PARA RODAR A API</h2>

1 - Clonar o projeto do GitHub.

2 - Cria o ambiente de trabalho e ativa ele.

3 - Instala os requirements 'pip install -r requirements-dev.txt'.

4 - Faz as migrações do db.

5 - Cria o usuariosuperuser.

6 - Roda o sistema 'runserver'.

7 - Loga no admin com o usuario que criou e coloca as taxas em 'Configuraçoes', 'http://localhost:8000/admin/'.

8 - Cadastra os ativos, 'http://localhost:8000/ativos/'.

10 - Faz as operações, 'http://localhost:8000/operacoes/'.

11 - Consulta saldo total, 'http://localhost:8000/users/'.

12 - Consulta saldo por ativo, 'http://localhost:8000/users/1/saldo_por_ativo/?ativo=bitcoin' caso queira consultar outro ativo é só setar o nome dele depois de ativo onde esta o bitcoin.
