import argparse, random, re

class Dado():

  def __init__(self, posicao_memoria, num_acessos, num_ciclos_vida, ordem_leitura):
    """Dado é o nome da estrutura que é armazenada dentro do cache associativo

    Arguments:
      posicao_memoria {int} -- posição da memória principal ao qual o dado está associado
      num_acessos {int} -- quantidade de vezes que o dado foi acessado
      num_ciclos_vida {int} -- há quantos ciclos de acesso ao cache esse dado está na cache
      ordem_leitura {int} -- em relação aos demais dados da memória
    """

def print_cache_direto(cache):
  print("+------- Cache ------+")
  print("|# \t|\t Data|")
  print("+--------------------+")
  for posicao, valor in cache.items():
    print("|{} \t|\t   {}|".format(posicao, valor))
  print("+--------------------+")


def print_cache_associativo_conjunto(cache, qtd_conjuntos):
  print("+------- Cache ------+")
  print("|#\t|Cnj\t|\t Data|")
  print("+--------------------+")
  for posicao, valor in cache.items():
    num_conjunto = int(posicao)%int(qtd_conjuntos)
    print("|{} \t|{}\t|\t   {}|".format(posicao, num_conjunto, valor))
  print("+--------------------+")


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
  num_conjunto = int(posicao_memoria)%int(qtd_conjuntos)

  lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache,num_conjunto, qtd_conjuntos)

  # seleciona de forma aleatória uma das posições de memória
  # que fazem parte do conjunto em particular e armazena dentro
  # daquela posição o valor da memória principal
  posicao_memoria_cache_para_trocar = random.choice(lista_posicoes)

  if debug:
    print('Posição de memória cache que será trocada é: {}'.format(posicao_memoria_cache_para_trocar))

  memoria_cache[posicao_memoria_cache_para_trocar] = posicao_memoria



def politica_substituicao_FIFO():
  pass


def politica_substituicao_LRU():
  pass


def politica_substituicao_LFU():
  pass


def existe_posicao_vazia(memoria_cache):
  """Verifica se existe na cache alguma posição de memória vazia,
  se existir essa posição é retornada.

  Arguments:
    memoria_cache {list} -- memória cache

  Returns:
    [int] -- com a primeira posição de memória vazia
  """
  for x in range(0, total_cache):
    if memoria_cache[x] == -1:
      return x
  return -1

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

  print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)

  hitoumiss = ''
  num_hit = 0;
  num_miss = 0

  for index, posicao_memoria in enumerate(posicoes_memoria_para_acessar):

    # verificar se existe ou não o dado na cache
    inserir_memoria_na_posicao_cache = verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria)
    if inserir_memoria_na_posicao_cache >= 0:
      num_hit += 1
      hitoumiss = 'Hit'
    else:
      num_miss += 1
      hitoumiss = 'Miss'
      ########
      # agora precisa executar as políticas de substituição
      ########
      # verifica se existe uma posição vazia na cache, se sim aloca nela a posição de memória
      posicao_vazia = existe_posicao_vazia(memoria_cache)

      if debug:
        print('Posição Vazia: {}'.format(posicao_vazia))

      if posicao_vazia >= 0:
        memoria_cache[posicao_vazia] = posicao_memoria
      elif politica_substituicao == 'RANDOM':
        politica_substituicao_RANDOM(memoria_cache,qtd_conjuntos,posicao_memoria)

    print('\nLeitura número {} da memória {}'.format(index,posicao_memoria))
    print('Status: {}'.format(hitoumiss))
    print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)

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


def executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar):
  """O mapeamento associativo é um tipo de mapeamento associativo por conjunto
  ou o número de conjunto é igual a 1

  Arguments:
    total_cache {int} -- tamanho total de palavras da cache
    posicoes_memoria_para_acessar {list} - quais são as posições de memória que devem ser acessadas
  """
  # o número 1 indica que haverá apenas um único conjunto no modo associativo por conjunto
  # que é igual ao modo associativo padrão! :) SHAZAM
  executar_mapeamento_associativo_conjunto(total_cache, 1, posicoes_memoria_para_acessar)


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

    print('\nLeitura número {} da memória {}'.format(index,posicao_memoria))
    print('Status: {}'.format(hitoumiss))
    print_cache_direto(memoria_cache)

    if debug:
      print('Poisição de Memória: {} \nPosição Mapeada na Cache: {}'.format(posicao_memoria, posicao_cache))

  print('Resumo Mapeamento Direto')
  print('------------------------')
  print('Total de acessos: {}'.format(len(posicoes_memoria_para_acessar)))
  print('Total HIT {}'.format(num_hit))
  print('Total MISS {}'.format(num_miss))
  taxa_cache_hit = (num_hit / len(posicoes_memoria_para_acessar))*100
  print('Taxa de Cache HIT {number:.{digits}f}%'.format(number=taxa_cache_hit, digits=2))

parser = argparse.ArgumentParser(prog='Simulador de Cache')
parser.add_argument('--total_cache',type=int, help='Número total de páginas da memória cache')
parser.add_argument('--tipo_mapeamento', help='Tipo do mapeamento desejado')
parser.add_argument('--qtd_conjuntos', type=int, help='Quantos conjuntos devem ser criados no método associativo por conjuntos')
parser.add_argument('--arquivo_acesso', help='Nome do arquivo')
parser.add_argument('--debug', default=0, help='Debug')

args = parser.parse_args()

# recuperar toos os parâmetros passados
total_cache = args.total_cache
tipo_mapeamento = args.tipo_mapeamento
arquivo_acesso = args.arquivo_acesso
qtd_conjuntos = args.qtd_conjuntos
debug = args.debug

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


print('+====================+')
print('| SIMULADOR DE CACHE |')
print('+====================+')

# se o tipo do mapeamento for direto DI
if tipo_mapeamento == 'DI':
  executar_mapeamento_direto(total_cache, posicoes_memoria_para_acessar)
elif tipo_mapeamento == 'AS':
  executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar)
elif tipo_mapeamento == 'AC':
  # o número de conjuntos deve ser um divisor do total da memória
  if total_cache%qtd_conjuntos != 0:
    print('\n\n------------------------------')
    print('ERRO: O número de conjuntos {} deve ser obrigatoriamente um divisor do total de memória cache disponível {}.'.format(qtd_conjuntos, total_cache))
    print('------------------------------')
    exit()
  executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar)
else:
  print('\n\n------------------------------')
  print('ERRO: O tipo de mapeamento \'{}\'não foi encontrado.'.format(tipo_mapeamento))
  print('------------------------------')
  exit()

if debug:
  print('-'*30)
  print('Posições de Memória Para acessar: {}'.format(len(posicoes_memoria_para_acessar)))
  print(posicoes_memoria_para_acessar)
  print('Parâmetros da Simulação')
  print("Total cache: {}".format(total_cache))
  print("Quantidade de Conjuntos: {}".format(qtd_conjuntos))
  print("Tipo Mapeamento: {}".format(tipo_mapeamento))
  print("Arquivo Acesso: {}".format(arquivo_acesso))
  print("Debug: {}".format(debug))
  print('-'*30)


