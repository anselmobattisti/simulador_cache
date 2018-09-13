# Simulador de Cache

Olá, ficamos muito felizes que você tenha interesse em aprender um pouco mais sobre as políticas de substituição de páginas da memória cache!

Esse script permite que você visualize de forma didática como ocorre a escolha e a substituição de uma posição de memória no cache.

Instalação
--

O único pré-requisito do script é que sua maquina rode python 3.7+

Para saber qual versão do python que você tem instalado acesse o seu terminal e digite:

```
$ python --version
```

Como resultado desejado deve aparecer algo do tipo

```
Python 3.7.0
```

O que foi implementado
--

Esse projeto foi desenvolvido com o objetivo de apresentar as principais políticas de substituição de páginas em memória cache. Serão implementados 4 algoritmos de substituição, sendo eles:

* FIFO
* LRU
* LFU
* RANDOM

No simulador, a memória poderá ser organizada em três diferentes esquemas de esquemas de associação endereçamento de memória / endereço de cache, sendo eles:

* DI - Direto
* AS - Associativo
* AC - Associativo por contjunto

Os parâmetros recebidos pelo programa são:

* total_cache: número máximo de páginas que a memória cache suporta (número inteiro)
* tipo_mapeamento: DI / AS / AC
* arquivo_acesso: arquivo com as entradas das posições de memória que dem acessadas, cada linha corresponde a uma posição de memória diferente.

Exemplo de uso:

1 - Mapeamento Direto
--

O mapeamento direto da memória cache é aquele que associa cada posição da memória principal com uma posição específica da memória cache, nessa aplicação foi implementado utilizando o mod. Temos quatro arquivos com cenários diferentes com relação ao uso do mapeamento direto.

No primeiro exemplo ocorre nenhum cache hit, ou seja, para cada posição de memória desejada será necessário ir buscar na memória principal

```
$ python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_0_hit.txt
```

O resultado final da executação será:

```
Total de acessos: 10
Total HIT 0
Total MISS 10
Taxa de Cache HIT 0.0%
```

No segundo exemplo duas posições são consecutivamente acessadas, então ocorre cache miss apenas na primeira vez que a posição é acessada e em seguinda todos os demais acesso são hit.

```
$ python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_50_hit.txt
```

```
Total de acessos: 10
Total HIT 8
Total MISS 2
Taxa de Cache HIT 80.0%
```

No teceriro exemplo temos uma mesma posição sendo acessada consecutivamente, assim, ocorre apenas um miss e o restante é hit

```
$ python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_100_hit.txt
```

```
Total de acessos: 10
Total HIT 9
Total MISS 1
Taxa de Cache HIT 90.0%
```

No quarto exemplo apresentamos um exemplo onde a ineficiência do mapeamento direto é apresentada. Apesar de existir um número grande de memória o número de miss é elevado uma vez que está sendo feita um alto uso de memória de uma localidade de memória com sombreamento entre si de utilização de memória.

```
$ python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_misto_hit.txt
```


```
Total de acessos: 13
Total HIT 2
Total MISS 11
Taxa de Cache HIT 15.38%
```

NOTA DOS AUTORES
--

No método direto não existem políticas de substituição de cache uma vez que a posição da memória principal sempre estará mapeada com a mesma posição de memória da memória cache, já nos modos associativo e associativo por conjunto essa relação direta entre as duas memórias não existe, e portanto, é necessário que sejam implementados mecanismos para escolher em caso de falta de espaço na memória cache, qual posição será descartada para que a nova posição seja ocupada.

2 - Mapeamento Associativo
--

No mapeamento associativo não existe uma posição pré-estabelecida, ou seja, determinística entre a posição da memória principal e a posição da memória cache, dessa forma é necessário percorrer toda a memória cache a fim de verificar se a posição da memória princial está ou não na cache.

Caso a posição de memória esteja na cache estão ela é retornada como um HIT, caso ela não exista então é necessário que seja escolhida uma posição de memória para ser removida da cache, no caso do MISS.

O problema desse tipo de mapeamento é que o o custo para identificar se uma posição da memória principal está na cache é a de verificar todas as posições da cache, isso é ruim!

Os algoritmos de substição de cache são os mesmos tanto para o associativo como para o associativo por conjunto!

```
$ python main.py --total_cache 3 --tipo_mapeamento=AS --arquivo_acesso=arquivos_teste/acesso_associativo_100_hit.txt --debug 1
```