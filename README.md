
# The Online Judge

 
O Online Judge é uma api desenvolvida em python/django que permitem com que professores criem exercícios de programação em python, informado um enunciado com uma descrição e conjunto de entradas que devem ser processadas por um programa e as saídas que esse programa devem produzir. Esses exercícios podem ser resolvidos por alunos, que irão submeter seu código e obter um resultado. 

A api foi construída com 4 microsserviços principais:

 - Users: Responsável por amarzenar dados do usuário e prover mecanismos de autenticação baseado em JWT
 - Problems: Responsável por armazenar os dados dos problemas e por receber as submissões dos alunos e enviá-las ao serviço de execução
 - Runner: Responsável por executar o código python em uma sandboxe determinar a corretude.
 - Score: Responsável por manter um sumário das execuções e contador de exercícios acertados/tenatos por usuário.
 
### Ambiente de Desenvolvimento
  
Esse projeto utiliza o pdm, para instalá-lo siga esse [tutorial](https://pdm.fming.dev/).

Com o  pdm corretamente configurado, é possível instalar as dependências do projeto executando:

```
git clone https://github.com/hllustosa/online-judge
cd online-judge
pdm install
```

Cada projeto pode ser executado independentemente através dos scripts:

```
./run_problems.sh
./run_scores.sh
./run_users.sh
```

Porém, neste caso é necessário ter o rabbitmq (com usuário e senha "guest" e "guest" respectivamente) e o mongodb (com autenticação ativa e um usuário: "admin" e com senha: "pass")  em execução e acessíveis através do localhost com suas portas padrão. Isto é necessário para executar, desenvolver ou testar a aplicação fora do docker.

### Executar o Projeto

A maneira aconselhável de executar o projeto é através do docker compose (isto exige que o docker e o docker-compose estejam instalados no ambiente). O docker-compose executa todos os microsserviços com suas dependências corretamente:

```
docker-compose up -d
```
Após a execução os serviços ficarão acessíveis em:

 - Users: http://localhost:8001/
 - Problems: http://localhost:8002/
 - Score: http://localhost:8003/
 
 ### Api Online Judge
 
[Esta collection do postman](https://github.com/hllustosa/online-judge/blob/master/online_judge.postman_collection.json) contém exemplos de requisições básicas, como login, criação de problemas, submissão de código, verificação de resultado de execução e placar.
