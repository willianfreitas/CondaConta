# CondaConta
### Descrição
Repositório para o projeto do Desafio CondaConta

### Requisitos

Para instalar os requisitos basicos, basta executar:
    ```
    pip install -r requirements.txt
    ```
Os requisitos para que este projeto funcione são:
    - flask
    - python-dotenv
    - tinyDB
    - flask_pydantic_spec

### Como Utilizar

Após clonar o projeto me instalar os requisitos, basta acessar o terminal dentro da pasta onde você clonou o projeto e executar o seguinte comando:

    ```
    flask run
    ```
Isso fará com que o Flask inicie sua instancia na porta: _localhost:5000/_
Automaticamente o programa irá subir junto do flask o TinyDB e irá adicionar a database os dois primeiros usuários para testes.

### Endpoints

Para facilitar a utilização do projeto, acesse a url:
    ```
    localhost:5000/apidoc/swagger/
    ```
Assim, você irá acessar a home da documentação via Swagger do projeto e terá acesso as URL's do mesmo.

#### /saldo

Com esse endpoint, você consegue consultar o saldo de uma conta, para utiliza-lo, deve-se passar via body os seguintes parâmetros:
    ```
    "tipo":"string" -> Tipo da conta que deseja consultar, pode ser Poupanca ou Corrente
    "titularidade":"string" -> Titular da conta que deseja consultar, atualmente no banco o titular é Willian Freitas.
    ```

O retorno da função será:
    ```
    "saldo": int -> O valor do saldo cadastrado
    "tipo de conta": string -> O tipo da conta selecionado
    "titular": string -> O titular da conta consultada
    ```

#### /transferencia

Com esse endpoint, você consegue efetuar transferências de uma conta Corrente para Poupança e vice-versa, para utiliza-lo, deve-se passar via body os seguintes parâmetros:

    ```
    "tipo": string -> tipo da operação a ser feita, pode ser Investimento (transferencia da Corrente para Poupanca) ou Resgate (transferencia da Poupanca para Corrente)
    "titularidade": string -> titular das contas que serão feitas as movimentações
    "valor": string -> valor da transferencia a ser realizada
    ```

Atualmente o projeto apenas faz transferencias para mesma titularidade.

### Considerações Finais

O projeto não conta com uma checagem caso uma conta já foi adicionada ao banco de dados, então, porfavor, caso pare a execução do programa, antes de iniciar novamente a execução do mesmo, delete o arquivo _database.json_ de sua pasta do projeto.