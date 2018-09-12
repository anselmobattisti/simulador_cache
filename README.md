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
---------------

python main.py --total_cache 10 --tipo_mapeamento=DI --arquivo_acesso=acesso.txt --debug 1