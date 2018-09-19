import argparse, random, re


# Essa lista irá armazenar qual o número de vezes que uma
# determinada posição da memória cache foi executada
contador_lfu = {}


# Essa lista irá armazenar a ordem que a posição da memória
# principal foi inserida na memória cache
contador_fifo = {}


def existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria):
  """Verifica se existe na cache alguma posição de memória vazia,
  se existir essa posição é retornada.

  Arguments:
    memoria_cache {list} -- memória cache
    qtd_conjuntos {int} -- número de conjuntos da cache
    posicao_memoria {int} -- posição de memória que se quer armazenar na cache

  Returns:
    [int] -- com a primeira posição de memória vazia do conjunto
  """
  num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
  lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos)

  # verifica se alguma das posições daquele conjunto está vazia
  for x in lista_posicoes:
    if memoria_cache[x] == -1:
      return x
  return -1


def imprimir_contador_fifo():
    print('+--------------------------------------+')
    print("| Contador FIFO                        |")
    print('+--------------------------------------+')
    print("|Conjunto | Próxima Posição Substituir |")
    print('+---------+----------------------------+')
    for index, x in enumerate(contador_fifo):
      print("|{:>9}|{:>28}|".format(index,x))
    print('+---------+----------------------------+')


def inicializar_contador_fifo():
  """Seta os valores do contador fifo para que a primeira subsitituição
  ocorra no primeiro elemento que faz parte do conjunto
  """
  # cria no contador fifo uma posição para cada conjunto
  for x in range(0, qtd_conjuntos):
    contador_fifo[x] = 0

  if debug:
    imprimir_contador_fifo()


def imprimir_contador_lfu():
    print('+--------------------------------------+')
    print("| Contador LFU                         |")
    print('+--------------------------------------+')
    print("|Posição Cache | Qtd Acessos           |")
    print('+---------+----------------------------+')
    for index, x in enumerate(contador_lfu):
      print("|{:>9}|{:>28}|".format(index,contador_lfu[x]))
    print('+---------+----------------------------+')


def inicializar_contador_lfu():
  """Seta os valores do contador LFU para zero, ou seja, a posição que ocupa aquela
  posição da cache ainda não foi utilizada. Para cada posição da cache teremos um contador
  que será somado tada vez que houver um hit e será zerado quando a posição for substituida
  """
  # cria on contador LFU uma posiçõao para caqda posição de memória
  for x in range(0, total_cache):
    contador_lfu[x] = 0

  if debug:
    imprimir_contador_lfu()


def get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos):
  """Retorna o número do conjunto onde essa posição de memória é sempre mapeada

  Arguments:
    posicao_memoria {int} -- posição de memória que se quer acessar
    qtd_conjuntos {int} -- número de conjuntos que a cache possui
  """
  return int(posicao_memoria)%int(qtd_conjuntos)


def print_cache_direto(cache):
  print("+--------------------------+")
  print("|      Cache Direto        |")
  print("+--------------------------+")
  print("|Tamanho Cache: {:>11}| ".format(len(cache)))
  print("+----------+---------------+")
  print("|Pos Cache |Posição Memória|")
  print("+----------+---------------+")
  for posicao, valor in cache.items():
    print("|{:>10}|{:>15}|".format(posicao, valor))
  print("+----------+---------------+")


def print_cache_associativo(cache):
  print("+--------------------------+")
  print("|Tamanho Cache: {:>11}| ".format(len(cache)))
  print("+----------+---------------+")
  print("|     Cache Associativo    |")
  print("+----------+---------------+")
  print("|Pos Cache |Posição Memória|")
  print("+----------+---------------+")
  for posicao, valor in cache.items():
    print("|{:>10}|{:>15}|".format(posicao, valor))
  print("+----------+---------------+")


def print_cache_associativo_conjunto(cache, qtd_conjuntos):
  print("+------------------------------+")
  print("|Tamanho: {:>21}|\n|Conjuntos: {:>19}|".format(len(cache), qtd_conjuntos))
  print("+------------------------------+")
  print("+  Cache Associativo Conjunto  +")
  print("+-------+-------+--------------+")
  print("|#\t| Cnj\t|   Pos Memória|")
  print("+-------+-------+--------------+")
  for posicao, valor in cache.items():
    num_conjunto = get_num_conjuno_posicao_memoria(posicao, qtd_conjuntos)
    print("|{} \t|{:4}\t|\t   {:>4}|".format(posicao, num_conjunto, valor))
  print("+-------+-------+--------------+")


def inicializar_cache(total_cache):
  """Cria uma memória cache zerada utilizando dicionários e com
  valor padrão igual a -1

  Arguments:
    total_cache {int} -- tamanho total de palavras da cache

  Returns:
    [list] -- [dicionário]
  """
  # zera tota a memória cache
  memoria_cache = {}

  # popula a memória cache com o valor -1, isso indica que a posição não foi usada
  for x in range(0, total_cache):
    memoria_cache[x] = -1

  return memoria_cache


def verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria,):
  """Verifica se uma determinada posição de memória está na cache
    no modo associativo

  Arguments:
    memoria_cache {list} -- memória cache
    qtd_conjuntos {int} -- número de conjuntos do cache
    posicao_memoria {int} -- posição que se deseja acessar
  """
  num_conjunto = int(posicao_memoria)%int(qtd_conjuntos)

  while num_conjunto < len(memoria_cache):
    if memoria_cache[num_conjunto] == posicao_memoria:
      return num_conjunto

    num_conjunto += qtd_conjuntos

  # não achou a posição de memória na cache
  return -1


def get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos):
  """Retorna uma lista com todas as posições da memória cache que fazem parte de um determinado conjunto

  Arguments:
    memoria_cache {list} -- memória cache
    num_conjunto {int} -- número do conjunto que se quer saber quais são os endereçamentos associados com aquele conjunto
    qtd_conjuntos {int} -- quantidade total de conjuntos possíveis na memória

  Returns:
    [list] -- lista de posições de memória associada com um conjunto em particular
  """
  lista_posicoes = []
  posicao_inicial = num_conjunto
  while posicao_inicial < len(memoria_cache):
    lista_posicoes.append(posicao_inicial)
    posicao_inicial += qtd_conjuntos
  return lista_posicoes


def politica_substituicao_RANDOM(memoria_cache, qtd_conjuntos, posicao_memoria):
  """Nessa politica de substituição no momento que ocorrer um cache miss
  será sorteado um elemento do conjunto para ser removido

  Arguments:
    memoria_cache {list} -- memóiria cache
    qtd_conjuntos {int} -- quantidade de conjuntos
    posicao_memoria {int} -- posição de memória que será acessada
  """
  num_conjunto = int(posicao_memoria)%int(qtd_conjuntos)

  lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache,num_conjunto, qtd_conjuntos)

  # seleciona de forma aleatória uma das posições de memória
  # que fazem parte do conjunto em particular e armazena dentro
  # daquela posição o valor da memória principal
  posicao_memoria_cache_para_trocar = random.choice(lista_posicoes)

  if debug:
    print('Posição de memória cache que será trocada é: {}'.format(posicao_memoria_cache_para_trocar))

  memoria_cache[posicao_memoria_cache_para_trocar] = posicao_memoria


def politica_substituicao_FIFO(memoria_cache, qtd_conjuntos, posicao_memoria):
  """Nessa politica de substituição o primeiro elemento que entra é o primeiro elemento que sai

  Arguments:
    memoria_cache {list} -- memóiria cache
    qtd_conjuntos {int} -- quantidade de conjuntos
    posicao_memoria {int} -- posição de memória que será acessada
  """
  num_conjunto = int(posicao_memoria)%int(qtd_conjuntos)
  posicao_substituir = contador_fifo[num_conjunto]
  lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache,num_conjunto, qtd_conjuntos)

  if debug:
    imprimir_contador_fifo()
    print('Posição Memória: {}'.format(posicao_memoria))
    print('Conjunto: {}'.format(num_conjunto))
    print('Lista posições: {}'.format(lista_posicoes))
    print('Posição para subistituição: {}'.format(posicao_substituir))

  memoria_cache[lista_posicoes[posicao_substituir]] = posicao_memoria

  contador_fifo[num_conjunto] += 1

  if contador_fifo[num_conjunto] >= (len(memoria_cache)/qtd_conjuntos):
    contador_fifo[num_conjunto] = 0

  if debug:
    print('Posição de memória cache que será trocada é: {}'.format(lista_posicoes[posicao_substituir]))


def politica_substituicao_LFU(memoria_cache, qtd_conjuntos, posicao_memoria):
  """Nessa politica de substituição o elemento que é menos acessado é removido da
  memória cache quando ocorrer um MISS, a cada HIT aquela posição do HIT ganha um ponto
  de acesso

  Arguments:
    memoria_cache {list} -- memóiria cache
    qtd_conjuntos {int} -- quantidade de conjuntos
    posicao_memoria {int} -- posição de memória que será acessada
  """
  num_conjunto = int(posicao_memoria)%int(qtd_conjuntos)
  lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache,num_conjunto, qtd_conjuntos)

  # descobrir dentro do conjunto qual tem menos acesso
  posicao_substituir = 0
  if len(lista_posicoes) > 1:

    if debug:
      imprimir_contador_lfu()

    # descobrir qual das posições é menos usada
    lista_qtd_acessos = []
    for qtd_acessos in range(0, len(lista_posicoes)):
      lista_qtd_acessos.append(contador_lfu[qtd_acessos])

    posicoes_com_menos_acesso = min(lista_qtd_acessos)
    candidatos_lfu = []
    for qtd_acessos in range(0, len(lista_posicoes)):
      if contador_lfu[qtd_acessos] == posicoes_com_menos_acesso:
        candidatos_lfu.append(qtd_acessos)

    # para garantir ordem aleatória de escolha caso duas ou mais posições
    # tenham o mesmo número de acessos
    posicao_substituir = random.choice(candidatos_lfu)

  # zera o número de acessos a posição que foi substituida
  contador_lfu[posicao_substituir] = 0

  # altera a posição de memória que está na cache
  memoria_cache[lista_posicoes[posicao_substituir]] = posicao_memoria

  if debug:
    print('Posição Cache Substituir: {}'.format(posicao_substituir))
    print('Contador LFU: {}'.format(contador_lfu))
    print('Posição Memória: {}'.format(posicao_memoria))
    print('Conjunto: {}'.format(num_conjunto))
    print('Lista posições: {}'.format(lista_posicoes))
    print('Posição para subistituição: {}'.format(posicao_substituir))
    print('Posição de memória cache que será trocada é: {}'.format(lista_posicoes[posicao_substituir]))


def politica_substituicao_LRU_miss(memoria_cache, qtd_conjuntos, posicao_memoria):
  """Nessa politica de substituição quando ocorre um HIT a posição vai para o topo da fila,
  se ocorrer um MISS remove o elemento 0 e a posição da cache onde a memória foi alocada é
  colocada no topo da fila

  Arguments:
    memoria_cache {list} -- memóiria cache
    qtd_conjuntos {int} -- quantidade de conjuntos
    posicao_memoria {int} -- posição de memória que será acessada
  """
  num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
  lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache,num_conjunto, qtd_conjuntos)

  # copiar os valores de cada posição da cache do conjunto em questão uma posição para traz
  for posicao_cache in lista_posicoes:
    proxima_posicao = posicao_cache+qtd_conjuntos
    if proxima_posicao < len(memoria_cache):
      memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]

  memoria_cache[lista_posicoes[-1]] = posicao_memoria

  if debug:
    print('Posição Memória: {}'.format(posicao_memoria))
    print('Conjunto: {}'.format(num_conjunto))
    print('Lista posições: {}'.format(lista_posicoes))


def politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria, posicao_cache_hit):
  """Nessa politica de substituição quando ocorre um HIT a posição vai para o topo da fila,
  se ocorrer um MISS remove o elemento 0 e a posição da cache onde a memória foi alocada é
  colocada no topo da fila

  Arguments:
    memoria_cache {list} -- memóiria cache
    qtd_conjuntos {int} -- quantidade de conjuntos
    posicao_memoria {int} -- posição de memória que será acessada
    posicao_cache_hit {int} -- posição de memória cache onde o dados da memória principal está
  """
  num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
  lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache,num_conjunto, qtd_conjuntos)

  # copiar os valores de cada posição da cache do conjunto em questão uma posição para traz
  for posicao_cache in lista_posicoes:
    if posicao_cache_hit <= posicao_cache:
      proxima_posicao = posicao_cache+qtd_conjuntos
      if proxima_posicao < len(memoria_cache):
        memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]

  memoria_cache[lista_posicoes[-1]] = posicao_memoria

  if debug:
    print('Posição Memória: {}'.format(posicao_memoria))
    print('Conjunto: {}'.format(num_conjunto))
    print('Lista posições: {}'.format(lista_posicoes))



def executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, politica_substituicao='RANDOM'):
  """Executa a operação de mapeamento associativo, ou seja, não existe uma posição específica
  para o mapemento de uma posição de memória.

  Arguments:
    total_cache {int} -- tamanho total de palavras da cache
    qtd_conjuntos {int} -- quantidade de conjuntos na cache
    posicoes_memoria_para_acessar {list} -- quais são as posições de memória que devem ser acessadas
    politica_substituicao {str} -- Qual é a política para substituição caso a posição de memória desejada não esteja na cache E não exista espaço vazio
  """

  memoria_cache = inicializar_cache(total_cache)

  if qtd_conjuntos == 1:
    print_cache_associativo(memoria_cache)
  else:
    print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)

  num_hit = 0
  num_miss = 0

  # se a política for fifo então inicializa a lista de controle
  if politica_substituicao == 'FIFO':
    inicializar_contador_fifo()

  # se a política for fifo então inicializa a lista de controle
  if politica_substituicao == 'LFU':
    inicializar_contador_lfu()


  for index, posicao_memoria in enumerate(posicoes_memoria_para_acessar):
    print('\n\n\nInteração número: {}'.format(index+1))
    # verificar se existe ou não o dado na cache
    inserir_memoria_na_posicao_cache = verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria)
    if inserir_memoria_na_posicao_cache >= 0:
      num_hit += 1
      hitoumiss = 'Hit'

      # se for LFU então toda vez que der um HIT será incrementado o contador daquela posição
      if politica_substituicao == 'LFU':
        imprimir_contador_lfu()
        contador_lfu[inserir_memoria_na_posicao_cache] += 1

      # se for LRU então toda vez que der um HIT será incrementado o contador daquela posição
      if politica_substituicao == 'LRU':
        politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria, inserir_memoria_na_posicao_cache)


    else:
      num_miss += 1
      hitoumiss = 'Miss'
      ########
      # agora precisa executar as políticas de substituição
      ########
      # verifica se existe uma posição vazia na cache, se sim aloca nela a posição de memória
      posicao_vazia = existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria)

      if debug:
        print('Cache Miss')
        print('Posição da cache ainda não utilizada: {}'.format(posicao_vazia))
        print('\nLeitura linha {}, posição de memória {}.'.format(index,posicao_memoria))

      if posicao_vazia >= 0:
        memoria_cache[posicao_vazia] = posicao_memoria
      elif politica_substituicao == 'RANDOM':
        politica_substituicao_RANDOM(memoria_cache,qtd_conjuntos,posicao_memoria)
      elif politica_substituicao == 'FIFO':
        politica_substituicao_FIFO(memoria_cache,qtd_conjuntos,posicao_memoria)
      elif politica_substituicao == 'LFU':
        politica_substituicao_LFU(memoria_cache,qtd_conjuntos,posicao_memoria)
      elif politica_substituicao == 'LRU':
        politica_substituicao_LRU_miss(memoria_cache,qtd_conjuntos,posicao_memoria)


    if qtd_conjuntos == 1:
      print_cache_associativo(memoria_cache)
    else:
      print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)


  # se for LFU e com debug imprimir os dados computador no contador LFU
  if politica_substituicao == 'LFU' and debug:
    imprimir_contador_lfu()

  print('\n\n-----------------')
  print('Resumo Mapeamento')
  print('-----------------')
  print('Política de Substituição: {}'.format(politica_substituicao))
  print('-----------------')
  print('Total de acessos: {}'.format(len(posicoes_memoria_para_acessar)))
  print('Total HIT {}'.format(num_hit))
  print('Total MISS {}'.format(num_miss))
  taxa_cache_hit = (num_hit / len(posicoes_memoria_para_acessar))*100
  print('Taxa de Cache HIT {number:.{digits}f}%'.format(number=taxa_cache_hit, digits=2))


def executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao):
  """O mapeamento associativo é um tipo de mapeamento associativo por conjunto
  ou o número de conjunto é igual a 1

  Arguments:
    total_cache {int} -- tamanho total de palavras da cache
    posicoes_memoria_para_acessar {list} - quais são as posições de memória que devem ser acessadas
    politica_substituicao {str} -- qual será a política de subistituição
  """
  # o número 1 indica que haverá apenas um único conjunto no modo associativo por conjunto
  # que é igual ao modo associativo padrão! :) SHAZAM
  executar_mapeamento_associativo_conjunto(total_cache, 1, posicoes_memoria_para_acessar, politica_substituicao)


def executar_mapeamento_direto(total_cache, posicoes_memoria_para_acessar):
  """Executa a operação de mapeamento direto.

  Arguments:
    total_cache {int} -- tamanho total de palavras da cache
    posicoes_memoria_para_acessar {list} - quais são as posições de memória que devem ser acessadas
  """
  # zera tota a memória cache
  memoria_cache = inicializar_cache(total_cache)

  print('Situação Inicial da Memória Cache')
  print_cache_direto(memoria_cache)

  hitoumiss = ''
  num_hit = 0;
  num_miss = 0
  for index, posicao_memoria in enumerate(posicoes_memoria_para_acessar):
    # no mapeamento direto, cada posição da memória principal tem uma posição
    # específica na memória cache, essa posição será calculada em função
    # do mod da posição acessada em relação ao tamanho total da cache
    posicao_cache = posicao_memoria % total_cache

    # se a posição de memória principal armazenada na linha da cache for a posição
    # desejada então dá hit, caso contrário da miss
    if memoria_cache[posicao_cache] == posicao_memoria:
      num_hit += 1
      hitoumiss = 'Hit'
    else:
      num_miss += 1
      hitoumiss = 'Miss'

    memoria_cache[posicao_cache] = posicao_memoria

    print('\nLeitura linha {},  posição de memória desejada {}.'.format(index,posicao_memoria))
    print('Status: {}'.format(hitoumiss))
    print_cache_direto(memoria_cache)

    if debug:
      print('Poisição de Memória: {} \nPosição Mapeada na Cache: {}'.format(posicao_memoria, posicao_cache))

  print('\n\n------------------------')
  print('Resumo Mapeamento Direto')
  print('------------------------')
  print('Total de acessos: {}'.format(len(posicoes_memoria_para_acessar)))
  print('Total HIT: {}'.format(num_hit))
  print('Total MISS: {}'.format(num_miss))
  taxa_cache_hit = (num_hit / len(posicoes_memoria_para_acessar))*100
  print('Taxa de Cache HIT: {number:.{digits}f}%'.format(number=taxa_cache_hit, digits=2))

parser = argparse.ArgumentParser(prog='Simulador de Cache')
parser.add_argument('--total_cache', required=True, type=int, help='Número total de posições da memória cache.')
parser.add_argument('--tipo_mapeamento', required=True, help='Tipo do mapeamento desejado. Os valores aceitos para esse parâmetro são: DI / AS / AC.')
parser.add_argument('--politica_substituicao', default='ALL', help='Qual será a política de substituição da cache que será utilizada. Os valores aceitos para esse parâmetro são: RANDOM / FIFO / LRU / LFU.')
parser.add_argument('--qtd_conjuntos', type=int, default=1, help='Quando for escolhido o tipo de mapeamento AC deve-se informar quantos conjuntos devem ser criados dentro da memória cache.')
parser.add_argument('--arquivo_acesso', required=True, default='', help='Nome do arquivo que possui as posições da memória principal que serão acessadas. Para cada linha do arquivo deve-se informar um número inteiro.')
parser.add_argument('--debug', default=0, help='Por padrão vem setado como 0, caso queira exibir as mensagens de debugs basta passar --debug 1.')

args = parser.parse_args()

# recuperar toos os parâmetros passados
total_cache = args.total_cache
tipo_mapeamento = args.tipo_mapeamento
arquivo_acesso = args.arquivo_acesso
qtd_conjuntos = args.qtd_conjuntos
politica_substituicao  = args.politica_substituicao.upper()
debug = args.debug

if arquivo_acesso == '':
  print('\n\n------------------------------')
  print('ERRO: É necesário informar o nome do arquivo que será processado, o parâmetro esperado é --arquivo_acesso seguido do nome do arquivo.')
  print('------------------------------')
  exit()

# lê o arquivo e armazena cada uma das posições de memória que será lida em uma lista
try:
  f = open(arquivo_acesso, "r")
  posicoes_memoria_para_acessar = []
  for posicao_memoria in f:
    posicoes_memoria_para_acessar.append(int(re.sub(r"\r?\n?$", "", posicao_memoria, 1)))
  f.close()
except IOError as identifier:
  print('\n\n------------------------------')
  print('ERRO: Arquivo \'{}\'não encontrado.'.format(arquivo_acesso))
  print('------------------------------')
  exit()

if len(posicoes_memoria_para_acessar) == 0:
    print('\n\n------------------------------')
    print('ERRO: o arquivo {} não possui nenhuma linha com números inteiros.'.format(arquivo_acesso))
    print('------------------------------')
    exit()

print('+====================+')
print('| SIMULADOR DE CACHE |')
print('+====================+')
print('+ Setando parâmetros iniciais da cache+')


if tipo_mapeamento != 'DI':
  if politica_substituicao != 'RANDOM' and politica_substituicao != 'FIFO' and politica_substituicao != 'LRU' and politica_substituicao != 'LFU' and politica_substituicao != 'ALL':
    print('\n\n------------------------------')
    print('ERRO: A política de substituição {} não existe.'.format(politica_substituicao))
    print('------------------------------')
    exit()

# se o tipo do mapeamento for direto DI
if tipo_mapeamento == 'DI':
  executar_mapeamento_direto(total_cache, posicoes_memoria_para_acessar)
elif tipo_mapeamento == 'AS':
  if (politica_substituicao == 'ALL'):
    executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'RANDOM')
    executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'FIFO')
    executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'LRU')
    executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'LFU')
  else:
    executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao)

elif tipo_mapeamento == 'AC':
  # o número de conjuntos deve ser um divisor do total da memória
  if total_cache%qtd_conjuntos != 0:
    print('\n\n------------------------------')
    print('ERRO: O número de conjuntos {} deve ser obrigatoriamente um divisor do total de memória cache disponível {}.'.format(qtd_conjuntos, total_cache))
    print('------------------------------')
    exit()

  if (politica_substituicao == 'ALL'):
    executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'RANDOM')
    executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'FIFO')
    executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'LRU')
    executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'LFU')
  else:
    executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, politica_substituicao)
else:
  print('\n\n------------------------------')
  print('ERRO: O tipo de mapeamento \'{}\'não foi encontrado. \nOs valores possíveis para o parâmetro --tipo_mapeamento são: DI / AS / AC'.format(tipo_mapeamento))
  print('------------------------------')
  exit()

if debug:
  print('\n')
  print('-'*80)
  print('Parâmetros da Simulação')
  print('-'*80)
  print("Arquivo com as posições de memória: {}".format(arquivo_acesso))
  print('Número de posições de memória: {}'.format(len(posicoes_memoria_para_acessar)))
  print('As posições são: {}'.format(posicoes_memoria_para_acessar))
  print('Tamanho total da cache: {}'.format(total_cache))
  print("Tipo Mapeamento: {}".format(tipo_mapeamento))
  if tipo_mapeamento != 'AS':
    print("Quantidade de Conjuntos: {}".format(qtd_conjuntos))
  print("Política de Substituição: {}".format(politica_substituicao))
  print("Debug: {}".format(debug))
  print('-'*80)


