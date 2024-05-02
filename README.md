# Ingestão de base de CEP

@since 2024-05-02

### Objetivo

Colocar em prática os estudos sobre Engenharia de Dados.

Nesse projeto é exercitado o Airflow em conjunto com a biblioteca Pandas e o operador Postgres.

Esse projeto é auto-contido, para executá-lo é necessário ter instalado o Docker, bastando executar:

    docker-compose up -d
ou
    docker compose up -d

No caso de usuários Windows, aconselho usar o wsl

Como objetivo desse pipeline, realizar a ingestão da base de cep para uma base de dados PostgreSQL (utilizando o próprio banco de dados que o Airflow utiliza)

O pipe line segue os seguintes passos:

1. Extrai o arquivo cep.zip no diretório */opt/airflow/input* colocando o conteúdo em */opt/airflow/output/cep*;
2. Exclui todos os arquivos não necessários, deixando apenas os arquivos *.txt* os quais são as fontes de dados de cep;
3. Renomeia os arquivos e diretórios restantes em minúsculo;
4. Move os arquivos de fontes de dados (*.txt*) para a raiz */opt/airflow/output/cep*;
5. Executa o script sql *schema.sql* para gerar as tabelas de CEP;
6. Executa a ETL, gravando os dados de CEP no banco de dados;
7. Remove o diretório */opt/airflow/output/cep*

A DAG *cep_dag* foi configurada para ter início de execução a partir de 27/04/2024, com execução diária.

Ao realizar a execução da dag, ocorreram erros de processos zumbis, no *docker-compose.yml* não configurei nada sobre timeout de processos.

Para contornar esses erros, transformei a task *etl()* em: etl_1(), etl_2(), etl_3(), etl_4() e etl_5(), dividindo a carga dos dados nessas 5 tasks, desse modo completou-se a DAG sem mais erros.

Pontos interessantes no projeto:

* Uso dos decorators @dag e @task, fica mais sucinta as funções, deixando o código mais limpo;
* Separação das funções, deixei as funções fora do arquivo de dag (cep_dag.py) colocando em func_cep.py e func_utils.py, deixando a leitura da dag mais fácil de entender;
* Uso do BashOperator, facilitando o tratamento dos arquivos (descompactação, remoção de arquivos, etc);
* Uso do PostgreOperator e separação do sql em arquivo separado (cep_schema.sql), mais uma vez deixando um código mais limpo e aproveitando o operator para realizar a tarefa;
* Utilização do pandas para leitura dos arquivos de dados e escrita em banco de dados, usando o separador correto de colunas e o encode correto (ISO-8859-1).

Vale lembrar que a base de CEP está desatualizada (2016), caso queira utilizar esse projeto para uma carga em produção, recomendo comprar a versão mais atualizada da base de ceps dos Correios.

### **Não utilize o arquivo cep.zip desse projeto em produção ou fins comerciais**

## Executando o projeto

Para executar basta rodar o docker compose, vá até a pasta do projeto, no terminal (bash, powershell, wsl):

    docker-compose up -d
ou

    docker compose up -d

Para acessar o Airflow, abra o browser nessa url http://localhost:8080


Usuário: airflow
Senha: airflow

Vá até *DAGs*, habilite a DAG *cep_dag*, clique em *cep_dag* e depois clique em *Graph*

Desse modo você irá acompanhar a execução das tarefas do pipeline

### Visualizando os registros

No browser, acesse: http://localhost:8086

Usuário: user@gmail.com
Senha: 123456So

Desse modo você acessa a página do *PgAdmin*, é um cliente para o PostGreSQL

Navegue Servers -> db-cep -> Databases -> airflow -> Schemas -> public -> Tables

As seguintes tabelas fazem parte desse projeto:

* ect_pais;
* log_bairro;
* log_cpc;
* log_faixa_bairro;
* log_faixa_cpc;
* log_faixa_localidade;
* log_faixa_uf;
* log_faixa_uop;
* log_grande_usuario;
* log_localidade;
* log_logradouro;
* log_num_sec;
* log_unid_oper;
* log_var_bai;
* log_var_loc;
* log_var_log;

Após navegar até aqui, clique em *Query Tool*, abrirá a ferramenta de query, nela pode-se realizar comandos SQL.

## Terminando o projeto

Para encerrar:

    docker-compose down
ou

    docker compose down

