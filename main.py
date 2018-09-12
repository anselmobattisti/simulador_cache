import argparse
import re


def print_cache_direto(cache):
  print("+------- Cache ------+")
  print("|# \t|\t Data|")
  print("+--------------------+")
  for posicao, valor in cache.items():
    print("|{} \t|\t   {}|".format(posicao, valor))
  print("+--------------------+")


def executar_mapeamento_direto(total_cache, posicoes_memoria_para_acessar):
  """Executa a operação de mapeamento direto.

  Arguments:
    total_cache {int} -- tamanho total de palavras da cache
    posicoes_memoria_para_acessar {list} - quais são as posições de memória que devem ser acessadas
  """
  # zera tota a memória cache
  memoria_cache = {}

  # popula a memória cache com o valor -1, isso indica que a posição não foi usada
  for x in range(0, total_cache):
    memoria_cache[x] = -1

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
  print('Taxa de Cache HIT {}%'.format(taxa_cache_hit))

parser = argparse.ArgumentParser(prog='Simulador de Cache')
parser.add_argument('--total_cache',type=int, help='Número total de páginas da memória cache')
parser.add_argument('--tipo_mapeamento', help='Tipo do mapeamento desejado')
parser.add_argument('--arquivo_acesso', help='Nome do arquivo')
parser.add_argument('--debug', default=0, help='Debug')

args = parser.parse_args()

# recuperar toos os parâmetros passados
total_cache = args.total_cache
tipo_mapeamento = args.tipo_mapeamento
arquivo_acesso = args.arquivo_acesso
debug = args.debug

# lê o arquivo e armazena cada uma das posições de memória que será lida em uma lista
f = open(arquivo_acesso, "r")
posicoes_memoria_para_acessar = []
for posicao_memoria in f:
  posicoes_memoria_para_acessar.append(int(re.sub(r"\r?\n?$", "", posicao_memoria, 1)))
f.close()


print('='*30)
print('SIMULADOR DE CACHE')
print('='*30)

# se o tipo do mapeamento for direto DI
if tipo_mapeamento == 'DI':
  executar_mapeamento_direto(total_cache, posicoes_memoria_para_acessar)

if debug:
  print('-'*30)
  print('Posições de Memória Para acessar: {}'.format(len(posicoes_memoria_para_acessar)))
  print(posicoes_memoria_para_acessar)
  print('Parâmetros da Simulação')
  print("Total cache: {}".format(total_cache))
  print("Tipo Mapeamento: {}".format(tipo_mapeamento))
  print("Arquivo Acesso: {}".format(arquivo_acesso))
  print("Debug: {}".format(debug))
  print('-'*30)


