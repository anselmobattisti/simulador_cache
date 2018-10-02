# Simulador de Cache

Olá, ficamos muito felizes que você tenha interesse em aprender um pouco mais sobre as políticas de substituição de páginas da memória cache!

A memória cache possui menos espaço de memória que a memória principal, logo, é necessário que seja implementado um mecanismo que permita que os endereços da memória principal, sejam associados a endereços da memória cache, além disso, é necessário uma política de substituição dos dados na memória cache caso seja necessário a atualização de dados pelo processador.

Esse script, permite que seja visualizado de forma didática, como ocorre a escolha e a substituição de uma posição de memória no cache, em três modelos diferentes de mapeamento de memória, sendo eles: mapeamento direto, associativo e associativo por conjunto.


Instalação do Script
--

O único pré-requisito do script é que sua máquina tenha instalado o python 3.7 ou superior.

Para saber qual versão do python que você tem instalado, acesse o seu terminal e digite:


```
$ python --version
```

Como resultado desejado deve aparecer algo do como:

```
Python 3.7.0
```

O arquivo principal é o main.py. Após a instalação do script para acessar o help da aplicação, basta digitar no console o comando a seguir:

```
$ python main.py -h
```

```
usage: Simulador de Cache [-h] --total_cache TOTAL_CACHE --tipo_mapeamento
                          TIPO_MAPEAMENTO
                          [--politica_substituicao POLITICA_SUBSTITUICAO]
                          [--qtd_conjuntos QTD_CONJUNTOS] --arquivo_acesso
                          ARQUIVO_ACESSO [--debug DEBUG] [--step STEP]
Simulador de Cache: error: the following arguments are required: --total_cache, --tipo_mapeamento, --arquivo_acesso
PS C:\anselmo\versionado\simulador_cache> python .\main.py -h
usage: Simulador de Cache [-h] --total_cache TOTAL_CACHE --tipo_mapeamento
                          TIPO_MAPEAMENTO
                          [--politica_substituicao POLITICA_SUBSTITUICAO]
                          [--qtd_conjuntos QTD_CONJUNTOS] --arquivo_acesso
                          ARQUIVO_ACESSO [--debug DEBUG] [--step STEP]

optional arguments:
  -h, --help            show this help message and exit
  --total_cache TOTAL_CACHE
                        Número total de posições da memória cache.
  --tipo_mapeamento TIPO_MAPEAMENTO
                        Tipo do mapeamento desejado. Os valores aceitos para
                        esse parâmetro são: DI / AS / AC.
  --politica_substituicao POLITICA_SUBSTITUICAO
                        Qual será a política de substituição da cache que será
                        utilizada. Os valores aceitos para esse parâmetro são:
                        RANDOM / FIFO / LRU / LFU.
  --qtd_conjuntos QTD_CONJUNTOS
                        Quando for escolhido o tipo de mapeamento AC deve-se
                        informar quantos conjuntos devem ser criados dentro da
                        memória cache.
  --arquivo_acesso ARQUIVO_ACESSO
                        Nome do arquivo que possui as posições da memória
                        principal que serão acessadas. Para cada linha do
                        arquivo deve-se informar um número inteiro.
  --debug DEBUG         Por padrão vem setado como 0, caso queira exibir as
                        mensagens de debugs basta passar --debug 1.
  --step STEP           Solicita a interação do usuário após cada linha
                        processada do arquivo --step 1.
```

Os exemplos de acesso a memória estão na parta arquivos_teste. Cada linha representa um acesso a uma posição da memória principal e o seu valor é um número inteiro que representa o número da posição que está sendo acessada.

# O que foi implementado
--

No simulador, a memória cache poderá ser organizada em três diferentes esquemas, sendo eles:

* DI - Direto;
* AS - Associativo; e
* AC - Associativo por contjunto.

Além disso, você pode escolher qual será a política de substituição de páginas da memória cache será utilizada. Estão implementados 4 algoritmos de substituição, sendo eles:

* FIFO;
* LRU;
* LFU; e
* RANDOM.

## 1 - Mapeamento Direto

O mapeamento direto da memória cache é aquele que associa cada posição da memória principal com uma posição específica da memória cache. Nessa aplicação essa associação foi implementado utilizando o mod, porém, caso o endereçamento de memória seja binário em geral é utilizado um conjunto dos primeiros do endereçamento da posição de memória como referência da posição da memória cache, o tamanho da memória cache definirá a quantidade de bits que serão selecionados.

Nessa aplicação de exemplo foram criados quatro arquivos com cenários diferentes com relação ao uso do mapeamento direto, tentamos aqui refletir as principais situação de cache hit e cache miss.

No primeiro exemplo não ocorrem CACHE HIT, ou seja, para cada posição de memória desejada será necessário ir buscar na memória principal.

O arquivo acesso_direto_0_hit.txt é composto por:
```
1
2
3
11
12
13
14
6
7
15
```

Executando o comando:

```
$ python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_0_hit.txt
```

O resultado final da executação será:

```
+--------------------------+
|      Cache Direto        |
+--------------------------+
|Tamanho Cache:          10|
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|             -1|
|         1|             11|
|         2|             12|
|         3|             13|
|         4|             14|
|         5|             15|
|         6|              6|
|         7|              7|
|         8|             -1|
|         9|             -1|
+----------+---------------+

------------------------
Resumo Mapeamento Direto
------------------------
Total de acessos: 10
Total HIT: 0
Total MISS: 10
Taxa de Cache HIT: 0.00%
```

É imporatnte ressaltar que nesse exemplo algumas posições da memória cache não foram utilizadas pois nenhuma das posições de memória solicitadas estavam associadas com as posições de memória vazias, com -1.  Isso mostra que a associação direta ganha em tempo de computação mas, em contra partida, pode perder em flexibilidade uma vez que mesmo havendo posições de memória cache disponível foi necessário fazer a substituição de uma página de memória na memória cache.

Caso o mesmo arquivo seja executado utilizando, por exemplo, um esquema de cache associativo o resultado final seria:

```
+--------------------------+
|Tamanho Cache:          10|
+----------+---------------+
|     Cache Associativo    |
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|              1|
|         1|              2|
|         2|              3|
|         3|             11|
|         4|             12|
|         5|             13|
|         6|             14|
|         7|              6|
|         8|              7|
|         9|             15|
+----------+---------------+
```

Perceba agora que como o tamanho da cache é exatamente igual a quantidade de posições diferentes de memória que está se tentando acessar, não existe troca de posição de memória na cache, isso é bom pois assim estamos utilizando a cache de maneira integral.

No segundo exemplo, duas posições são consecutivamente acessadas, então ocorre cache miss apenas na primeira vez que a posição é acessada e em seguinda todos os demais acesso são CACHE HIT.

O arquivo arquivos_teste/acesso_direto_50_hit.txt é composto por

```
0
1
2
3
4
5
0
1
2
3
4
5
```
Executando o comando:

```
$ python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_50_hit.txt
```

O resultado final da executação será:

```
+--------------------------+
|      Cache Direto        |
+--------------------------+
|Tamanho Cache:          10|
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|             -1|
|         1|              1|
|         2|              2|
|         3|             -1|
|         4|             -1|
|         5|             -1|
|         6|             -1|
|         7|             -1|
|         8|             -1|
|         9|             -1|
+----------+---------------+


------------------------
Resumo Mapeamento Direto
------------------------
Total de acessos: 10
Total HIT: 8
Total MISS: 2
Taxa de Cache HIT: 80.00%
```

Observer que nesse caso temos uma alta taxa de CACHE HIT e novamente um uso limitado da cache.

No teceriro exemplo temos uma mesma posição sendo acessada consecutivamente, assim, ocorre apenas um miss e o restante é hit

No terceiro exemplo apresentamos um cenário onde a ineficiência do mapeamento direto é apresentada. Apesar de existir um número grande de memória o número de CACHE MISS é elevado uma vez que está sendo feita um alto uso de memória de uma mesma localidade de memória com sombreamento entre si de utilização de memória, gerando assim um fenômeno onde existe cache disponível mas o modo como o mapeamento é feito, no caso, associativo, impede o uso da totalidade da cache.

O arquivo arquivos_teste/acesso_direto_misto_hit.txt é composto por

```
0
1
2
2
22
32
42
20
1
10
11
12
13
```
Executando o comando:

```
$ python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_misto_hit.txt
```

O resultado final da executação será:

```
+--------------------------+
|      Cache Direto        |
+--------------------------+
|Tamanho Cache:          10|
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|             10|
|         1|             11|
|         2|             12|
|         3|             13|
|         4|             -1|
|         5|             -1|
|         6|             -1|
|         7|             -1|
|         8|             -1|
|         9|             -1|
+----------+---------------+


------------------------
Resumo Mapeamento Direto
------------------------
Total de acessos: 13
Total HIT: 2
Total MISS: 11
Taxa de Cache HIT: 15.38%
```

Nota dos autores sobre o método de mapeamento direto
--

No método de mapeamento direto não existem políticas de substituição de cache uma vez que a posição da memória principal sempre estará mapeada com a mesma posição da memória cache. Em contra partida, nos modos associativo e associativo por conjunto essa relação direta entre as duas memórias existe mas com granularidade menor, e com isso surge a necessidade que sejam implementados mecanismos para escolher em caso de falta de espaço na memória cache para armazenar uma posição da memória principal qual posição será descartada para que a nova posição seja ocupada.

## 2 - Mapeamento Associativo


No mapeamento associativo não existe uma relação pré-estabelecida entre a posição da memória principal e a posição da memória cache, ou seja, não existe determinismo entre a posição da memória principal e a posição da memória cache. Dessa forma para saber se uma posição da memória principal está na memória cache é necessário percorrer toda a memória cache a fim de verificar se a posição da memória princial está ou não na cache.

Caso a posição de memória principal esteja na memória cache então ela é retornada como um CACHE HIT, caso ela não esteja armazenada  então é necessário que seja escolhida uma posição de memória cache para ser removida para que a nova posição da memória principal possa ser armazenada na memória cache.

A vantágem desse modelo de mapeamento em relação ao modelo direto é que não corremos o risco de ter cache ociosa, em contra partida, o custo para identificar se uma posição da memória principal está na memória cache é maior pois temos que verificar todas as posições da memória cache.

Abaixo serão apresentados alguns exemplos de uso do simulador onde é utilizado o esquema de mapeamento associativo juntamente com esquemas diversos de substituição de memória.

### FIFO

Nesse esquema de substituição o primeiro elemento que entra é o primeiro elemento que sai.

O arquivo arquivos_teste/acesso_associativo_100_hit.txt é composto por

```
0
1
2
3
4
4
5
6
```

Executando o comando

```
$ python main.py --total_cache 4 --tipo_mapeamento=AS --arquivo_acesso=arquivos_teste/acesso_associativo_100_hit.txt --debug 1 --politica_substituicao FIFO
```

```
+--------------------------+
|Tamanho Cache:           4|
+----------+---------------+
|     Cache Associativo    |
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|              4|
|         1|              5|
|         2|              6|
|         3|              3|
+----------+---------------+


-----------------
Resumo Mapeamento
-----------------
Política de Substituição: FIFO
-----------------
Total de acessos: 8
Total HIT 1
Total MISS 7
Taxa de Cache HIT 12.50%


-------------------------------------------------------------------
Parâmetros da Simulação
--------------------------------------------------------------------
Arquivo com as posições de memória: arquivos_teste/acesso_associativo_100_hit.txt
Número de posições de memória: 8
As posições são: [0, 1, 2, 3, 4, 4, 5, 6]
Tamanho total da cache: 4
Tipo Mapeamento: AS
Política de Substituição: FIFO
Debug: 1
--------------------------------------------------------------------
```

### RANDOM

Nesse esquema de substituição existe a escolha aleatória sobre qual elemento da cache deve ser substituida.

```
python main.py --total_cache 4 --tipo_mapeamento=AS --arquivo_acesso=arquivos_teste/acesso_associativo_100_hit.txt --debug 1 --politica_substituicao RANDOM
```

É interessante observar que duas execuções consecutivas podem ter resultados distintos tanto no estado final da cache como também na sua taxa de CACHE HIT.


O arquivo arquivos_teste/acesso_associativo_101_hit.txt é composto por

```
0
1
2
3
4
4
5
6
```

Executando o comando duas vezes:

```
$ python main.py --total_cache 4 --tipo_mapeamento=AS --arquivo_acesso=arquivos_teste/acesso_associativo_101_hit.txt --debug 1 --politica_substituicao RANDOM
```

Note que a sua saída não necessariamente será igual a saída apresentada abaixo uma vez que a escolha do elemento da cache que será removido é aleatória.

#### Execução A
```
+--------------------------+
|Tamanho Cache:           4|
+----------+---------------+
|     Cache Associativo    |
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|              5|
|         1|              1|
|         2|              6|
|         3|              3|
+----------+---------------+


-----------------
Resumo Mapeamento
-----------------
Política de Substituição: RANDOM
-----------------
Total de acessos: 14
Total HIT 6
Total MISS 8
Taxa de Cache HIT 42.86%
```

#### Execução B

```
+--------------------------+
|Tamanho Cache:           4|
+----------+---------------+
|     Cache Associativo    |
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|              0|
|         1|              1|
|         2|              5|
|         3|              6|
+----------+---------------+


-----------------
Resumo Mapeamento
-----------------
Política de Substituição: RANDOM
-----------------
Total de acessos: 14
Total HIT 7
Total MISS 7
Taxa de Cache HIT 50.00%
```

### LRU

Nesse esquema de substituição quando ocorre um CACHE MISS e é necessário trazer uma nova posição da memóiria principal para a memória cache então será removido a posição de memória que está na cache que foi usada há mais tempo.

O algorítmo trabalha da seguinte forma: Se houver um CACHE HIT então essa posição da CACHE vai para o topo da pilha, caso ocorra um CACHE MISS o primeiro elemento da fila é removido e no seu lugar é colocado a posição da memória principal e esse local passa a ser o novo topo da pilha.

```
python main.py --total_cache 4 --tipo_mapeamento=AS --arquivo_acesso=arquivos_teste/acesso_associativo_101_hit.txt --debug 1 --politica_substituicao LRU
```

Temos como saída:

```
+--------------------------+
|Tamanho Cache:           4|
+----------+---------------+
|     Cache Associativo    |
+----------+---------------+
|Pos Cache |Posição Memória|
+----------+---------------+
|         0|              3|
|         1|              4|
|         2|              5|
|         3|              6|
+----------+---------------+


-----------------
Resumo Mapeamento
-----------------
Política de Substituição: LRU
-----------------
Total de acessos: 14
Total HIT 7
Total MISS 7
Taxa de Cache HIT 50.00%


---------------------------------------------------------------------
Parâmetros da Simulação
---------------------------------------------------------------------
Arquivo com as posições de memória: arquivos_teste/acesso_associativo_101_hit.txt
Número de posições de memória: 14
As posições são: [0, 1, 2, 3, 4, 4, 5, 6, 5, 6, 5, 6, 5, 6]
Tamanho total da cache: 4
Tipo Mapeamento: AS
Política de Substituição: LRU
Debug: 1
---------------------------------------------------------------------
```

Observer que ao final da execução os elementos que não estão mais na cache são: 0, 1, 2, 3 pois após serem inseridos na cache os mesmos não mais foram acessados fazendo assim com que eles fossem removidos para que os demais elementos fossem utilizados.

### LFU

Esse é esquema de substituição exige que exista um contador para cada posição da memória cache, esse contador é incrementado toda vez que a posição é acessdo e é zerado toda vez que uma nova posição da memória principal é vinculada com aquela posição da memória cache.

A ideia aqui é aproveitar a localidade temporal, ou seja, aquela localidade que diz respeito a reusar posições que foram recentemente utilizadas.

Executando o comando:

```
$ python main.py --total_cache 4 --tipo_mapeamento=AS --arquivo_acesso=arquivos_teste/acesso_associativo_101_hit.txt --debug 1 --politica_substituicao LFU
```

Temos como saída:

```
-----------------
Resumo Mapeamento
-----------------
Política de Substituição: LFU
-----------------
Total de acessos: 14
Total HIT 7
Total MISS 7
Taxa de Cache HIT 50.00%


---------------------------------------------------------------------
Parâmetros da Simulação
---------------------------------------------------------------------
Arquivo com as posições de memória: arquivos_teste/acesso_associativo_101_hit.txt
Número de posições de memória: 14
As posições são: [0, 1, 2, 3, 4, 4, 5, 6, 5, 6, 5, 6, 5, 6]
Tamanho total da cache: 4
Tipo Mapeamento: AS
Política de Substituição: LFU
Debug: 1
---------------------------------------------------------------------
```


## 3 - Mapeamento Associativo por Conjuntos

Nesse modo, a memória cache é dividida em conjutos, ou seja, uma posição da memória principal é mapeada sempre para um mesmo conjunto e isso permite uma consulta mais rápida na cache se uma dada posição de memória está ou não nela.

No exemplo abaixo é aplicado o mapeamento por conjunto utilizando como número de conjuntos o valor 2 e como política de substituição da memória está sendo utilizado o tipo RANDOM

Existem diversas formas de se organizar um conjunto dentro da cache, no nosso simulador utilizamos o módulo da quantidade de conjuntos en relação ao tamanho da cache para determinar qual posição da cache faz parte de cada conjunto. Em uma cache de tamanho 4 com 2 conjuntos, as posições do conjunto ZERO são {0, 2}, ao passo que o conjunto UM está associado aos elementos {1, 3}, como pode ser observado abaixo.

```
+------------------------------+
|Tamanho:                     4|
|Conjuntos:                   2|
+------------------------------+
+  Cache Associativo Conjunto  +
+-------+-------+--------------+
|#      | Cnj   |   Pos Memória|
+-------+-------+--------------+
|0      |   0   |            -1|
|1      |   1   |            -1|
|2      |   0   |            -1|
|3      |   1   |            -1|
+-------+-------+--------------+
```

Desta forma, podemos observar que o comportamento do modo associativo por conjunto quando o conjunto é igual a 1 é exatamente igual ao modo associativo, pois no modo associativo existe apenas um único conjunto para toda a cache.

Quando temos dois conjuntos, por exemplo, toda posição de memória principal cujo identificador é par será associado a algum elemento do conjunto ZERO, ao passo que toda posição de memória ímpar será associado a algum elemento do conjunto UM.

Todos os modos de substituição de memória, RANDOM, FIFO, LRU e LFU apresentados anteriormente nos modo associativo funcionarão exatamente da mesma forma, a diferença é que ao invés de utilizar todos os elementos, usamores apenas os elementos que pertencem ao conjunto associado com a posição de memória que está sendo acessada!

Legal né, acesse o código fonte para entender um pouco mais sobre como essas políticas são implemetadas. É importante observar que não estamos preocupados com eficiência, ou uso da melhor estrutura de dados para cada tipo de algorítmo de substituição de memória, o intúito é apresentar como cada um se comporta, seus pontos positivos e negativos.

```
$ python main.py --total_cache 10 --tipo_mapeamento=AC --arquivo_acesso=arquivos_teste/acesso_associativo_100_hit.txt --qtd_conjuntos 2 --debug 1 --politica_substituicao RANDOM
```

No segundo exemplo estamos utilizando a politica de substituição conhecida como FIFO, ou seja, a primeira posição de memória que entra no conjunto e a primeira que será substituída quando houver um cache miss.


```
$ python main.py --total_cache 10 --tipo_mapeamento=AC --arquivo_acesso=arquivos_teste/acesso_associativo_100_hit.txt --qtd_conjuntos 2 --debug 1 --politica_substituicao FIFO
```

Nesse exemplo temos alguns cache hit obrigando assim que o contador da posição a ser substituida não seja incrementado.

```
$ python main.py --total_cache 10 --tipo_mapeamento=AC --arquivo_acesso=arquivos_teste/acesso_associativo_conjunto_51_hit.txt --qtd_conjuntos 2 --debug 1 --politica_substituicao FIFO
```

O próximo exemplo simula o processo o tipo de mapeamento associativo por conjunto com um total de 6 posições de cache e dois conjuntos.

```
$ python main.py --total_cache 6 --tipo_mapeamento=AC --arquivo_acesso=arquivos_teste/acesso_associativo_conjunto_51_hit.txt --debug 1 --politica_substituicao FIFO --qtd_conjuntos 2
```

Nesse exemplo temos leituras de memórias em dois conjuntos distintos, mostrando que primeiro é substituído a posição que está há mais tempo na memória cache, respeitando a ordem do conjunto.

```
python main.py --total_cache 6 --tipo_mapeamento=AC --arquivo_acesso=arquivos_teste/acesso_associativo_conjunto_52_hit.txt --debug 1 --politica_substituicao FIFO --qtd_conjuntos 2
```


No exemplo de substituição utilizando o LRU é necessário que haja um controle individual sobre cada posição da cache para saber quantas vezes ela já foi acessada dentro do seu conjunto.

```
$ python main.py --total_cache 10 --tipo_mapeamento=AC --arquivo_acesso=arquivos_teste/lru_0.txt --debug 1 --politica_substituicao LRU --qtd_conjuntos 1
```

As saída dessa executação foi:

```
Contador LRU:
Posição Cache    Qtd Acessos
0                3
1                4
2                3
3                3
4                0
5                0
6                0
7                0
8                0
9                0
------------------------------


-----------------
Resumo Mapeamento
-----------------
Política de Substituição: LRU
-----------------
Total de acessos: 17
Total HIT 13
Total MISS 4
Taxa de Cache HIT 76.47%
------------------------------
```

Mostrando então que houve a computação do número de acesso para cada uma das posições acessadas em relação ao conjunto que ela ocupa dentro da cache.


No próximo exemplo temos um total de 4 posições da memória cahce e dois conjuntos, nese caso, duas posições tem o mesmo número de acesso então é feito um sorteio para ver qual será a posição descartada.

```
$ python main.py --total_cache 4 --tipo_mapeamento=AC --arquivo_acesso=arquivos_teste/lru_3.txt --debug 1 --politica_substituicao LRU --qtd_conjuntos 2
```

A forma como os algorítmos de paginação são executados no mapeamento associativo por conjunto é exatamente igual ao modo associativo. A única diferença é que ao invés de fazer a substitução de página dentro de toda a cache, como no associativo, no associativo por conjunto, a substituição de página é feita apenas dentro do conjunto onde a posição de memória deveria ter sido mapeada.
