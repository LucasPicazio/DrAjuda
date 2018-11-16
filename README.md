# DrAjuda
Aplicativo para conectar pessoas em vulnerabilidade social com médicos dispostos a ajudar.

 - **Python** (após instalação do python, instalar libraries abaixo)
	 - pip install flask
	 - pip install flask-marshmallow
	 - pip install flask-login
   - pip install flask-sqlalchemy
   - pip install flask-basicauth
   
   
## Executar

 1. Instalar o Banco MYSQL e rodar o script SQL -> [Script](https://github.com/LucasPicazio/DrAjuda/blob/master/mydb.db.sql)
 2. Defina a URI de acordo com o exemplo abaixo
 3. Defina uma chave secreta
 4. Defina um usuario e senha para serem feitas requisições administrativas
 
 ~~~~
MySQL and Flask configurations
  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@server/db'
app.config['SECRET_KEY'] = 'D8SD47'
app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

~~~~

## Rotas
 ### GET
 #### Autenticação Básica necessária
 **/rest/{tabela}/{id}**  
 
 Retorna os dados de tupla de ID e tabela definidos  
 
 
 ### POST
 #### Autenticação Básica necessária
 **/rest/{tabela}**  
 Insere tupla de JSON na tabela 
 **O nome das chaves dp JSON deve ser igual ao nome das colunas da tabela**
 
 ### GET
 #### Autenticação Básica necessária
 **/rest/espec_med/{usr_id}/{esp_id}**  
 Designa uma especialidade a um usuario.

 
 ### POST
 **/login**  
 Loga o usuario  
 Enviar no JSON email de usuario e senha

 ### GET
 ### Login necessário
 **/logout**  
 Desloga usuario atualmente logado
 
 ### GET
 ### Login necessário
 **/rest/agendamentos**  
 Retorna todos agendamentos do usuario atualmente logado
 
 ### GET
 #### Autenticação Básica necessária
  **rest/horarios/{med_id}**  
  Retorna horarios disponiveis de um médico de acordo com seu ID.
 
 
