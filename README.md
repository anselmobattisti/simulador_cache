# Simulador de Cache

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
--

python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=acesso.txt --debug 1

Mapeamento Direto
--

O mapeamento direto da memória cache é aquele que associa cada posição da memória principal com uma posição específica da memória cache, nessa aplicação foi implementado utilizando o mod. Temos 3 arquivos com cenários diferentes com relação ao uso do mapeamento direto.

No primeiro exemplo ocorre nenhum cache hit, ou seja, para cada posição de memória desejada será necessário ir buscar na memória principal

python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_0_hit.txt

O resultado final da executação será:

```
Total de acessos: 10
Total HIT 0
Total MISS 10
Taxa de Cache HIT 0.0%
```

No segundo exemplo duas posições são consecutivamente acessadas, então ocorre cache miss apenas na primeira vez que a posição é acessada e em seguinda todos os demais acesso são hit.

python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_50_hit.txt

```
Total de acessos: 10
Total HIT 8
Total MISS 2
Taxa de Cache HIT 80.0%
```

No teceriro exemplo temos uma mesma posição sendo acessada consecutivamente, assim, ocorre apenas um miss e o restante é hit

python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=arquivos_teste/acesso_direto_100_hit.txt

```
Total de acessos: 10
Total HIT 9
Total MISS 1
Taxa de Cache HIT 90.0%
```

