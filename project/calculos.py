#bibliotecas usadas
#biblioteca de funções matemáticas
import math
#biblioteca numero random
import random

# Funções que converte a MP de KB para Byte
def calcular_tamanho_endereco_mp(tamanho_mp_kb):
    tamanho_mp_bytes = tamanho_mp_kb * 1024
    tamanho_endereco_mp = math.ceil(math.log2(tamanho_mp_bytes))
    return tamanho_endereco_mp

#função que calcula os valores da cache e MP
def calcular_valores(palavras_por_bloco, tamanho_cache_kb, linhas_por_conjunto, tamanho_mp_kb):
    tamanho_palavra_bytes = 4  # Tamanho da palavra em bytes
    tamanho_cache_bytes = tamanho_cache_kb * 1024
    w = math.ceil(math.log2(palavras_por_bloco))
    num_linhas_cache = tamanho_cache_bytes // (palavras_por_bloco * tamanho_palavra_bytes)
    s = math.ceil(math.log2(num_linhas_cache / linhas_por_conjunto))
    tag = calcular_tamanho_endereco_mp(tamanho_mp_kb) - (w + s)
    return w, int(num_linhas_cache), s, tag

# Funções que preenche a memória principal com valores aleátorios
def preencher_memoria_principal(tamanho_mp_kb):
    tamanho_mp_bytes = tamanho_mp_kb * 1024
    #gera valor aleatorios para a MP
    memoria_principal = [random.randint(0, 255) for _ in range(tamanho_mp_bytes)]
    return memoria_principal

def ler_arquivo_entrada(nome_arquivo):
    informacoes = {}
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) != 4:
                raise ValueError("O arquivo de entrada deve conter exatamente 4 linhas.")

            informacoes['tamanho_mp_kb'] = int(linhas[0].strip())
            informacoes['palavras_por_bloco'] = int(linhas[1].strip())
            informacoes['tamanho_cache_kb'] = int(linhas[2].strip())
            informacoes['linhas_por_conjunto'] = int(linhas[3].strip())

    except Exception as e:
        print(f"Erro ao ler o arquivo de entrada: {e}")
        raise

    return informacoes

#função que realiza a verificação dos valores arquivo
def verificar_dados(informacoes):
    if not (informacoes['tamanho_mp_kb'] > 0 and ((informacoes['tamanho_mp_kb'] & (informacoes['tamanho_mp_kb'] - 1)) == 0)):
        raise ValueError("Tamanho da memória principal deve ser uma potência de 2 e maior que 0.")
    if not (informacoes['tamanho_cache_kb'] > 0 and ((informacoes['tamanho_cache_kb'] & (informacoes['tamanho_cache_kb'] - 1)) == 0)):
        raise ValueError("Tamanho da cache deve ser uma potência de 2 e maior que 0.")
    if not (informacoes['palavras_por_bloco'] > 0 and ((informacoes['palavras_por_bloco'] & (informacoes['palavras_por_bloco'] - 1)) == 0)):
        raise ValueError("Número de palavras por bloco deve ser uma potência de 2 e maior que 0.")
    if not (informacoes['linhas_por_conjunto'] > 0 and ((informacoes['linhas_por_conjunto'] & (informacoes['linhas_por_conjunto'] - 1)) == 0)):
        raise ValueError("Número de linhas por conjunto deve ser uma potência de 2 e maior que 0.")

# Funções que inicializa a cache
def inicializar_cache(num_linhas_cache):
    cache = [{'tag': None, 'dados': None, 'freq': 0} for _ in range(num_linhas_cache)]
    return cache

#função que acessa os valores da cache
def acessar_cache(cache, endereco, palavras_por_bloco, w, s, tag_bits, memoria_principal, counters):
    bloco = endereco >> w
    conjunto_index = (bloco >> tag_bits) & ((1 << s) - 1)
    tag = bloco >> s

    conjunto_inicio = conjunto_index * len(cache) // (1 << s)
    conjunto_fim = conjunto_inicio + len(cache) // (1 << s)

    #contador de acertos/erros
    for linha in range(conjunto_inicio, conjunto_fim):
        if cache[linha]['tag'] == tag:
            cache[linha]['freq'] += 1
            counters['hits'] += 1
            print(f"Cache hit na linha {linha}")
            return cache[linha]['dados']

    lfu_linha = min(range(conjunto_inicio, conjunto_fim), key=lambda linha: cache[linha]['freq'])

    cache[lfu_linha]['tag'] = tag
    cache[lfu_linha]['dados'] = memoria_principal[bloco * palavras_por_bloco:(bloco + 1) * palavras_por_bloco]
    cache[lfu_linha]['freq'] = 1
    counters['misses'] += 1
    #print para mostrar qual linha foi substituida
    print(f"Cache miss - substituindo linha {lfu_linha} com bloco {bloco}")
    return cache[lfu_linha]['dados']

# Funções que apresentam as informações do emulador
def imprimir_informacoes(informacoes, cache, memoria_principal):
    tamanho_cache_kb = informacoes['tamanho_cache_kb']
    linhas_por_conjunto = informacoes['linhas_por_conjunto']
    palavras_por_bloco = informacoes['palavras_por_bloco']
    tamanho_mp_kb = informacoes['tamanho_mp_kb']
    #tamanho da palavra
    tamanho_palavra_bytes = 4
    #tamanho da cache
    tamanho_cache_bytes = tamanho_cache_kb * 1024
    #numero de linhas da cache
    num_linhas_cache = int(tamanho_cache_bytes / (palavras_por_bloco * tamanho_palavra_bytes))
    #numero de conjutos da cache
    num_conjuntos = num_linhas_cache // linhas_por_conjunto
    #calculo do  W
    w = math.ceil(math.log2(palavras_por_bloco))
    #numero de linhas da MP
    num_linhas_mp = (tamanho_mp_kb*1024) // tamanho_palavra_bytes
    #numero de blocos da MP
    num_blocos_mp = num_linhas_mp // palavras_por_bloco
    #caclculo de S
    s = math.ceil(math.log2(num_blocos_mp))
    #calculo de D
    d = math.ceil(math.log2(num_conjuntos))
    #calculo da TAG
    tag_bits = s - d

    #print das informações da cache
    print("\nInformações da cache:")
    print(f"Tamanho da Cache(kb)= {tamanho_cache_kb}")
    print(f"Linhas por Conjunto= {linhas_por_conjunto}")
    print(f"Quantidade de Conjuntos= {num_conjuntos}")
    print(f"Quantidade de linhas da cache= {num_linhas_cache}")
    print(f"d= {d}")
    print(f"tag= {tag_bits}")

    #print das informações da MP
    print("\nInformações da Memória Principal:")
    print(f"Tamanho da memória(kb)= {tamanho_mp_kb}")
    print(f"Palavras por bloco= {palavras_por_bloco}")
    print(f"Quantidade de linhas= {num_linhas_mp}")
    print(f"Quantidade de blocos= {2**s}")
    print(f"Bits para word= {w}")
    print(f"Bits para s= {s}")
    tamanho_endereco = w + s
    print(f"Tamanho do endereço= {tamanho_endereco}")

    print("\nConjuntos da Cache:")
    for conjunto in range(num_conjuntos):
        print(f"Conjunto {conjunto}: {cache[conjunto * linhas_por_conjunto:(conjunto + 1) * linhas_por_conjunto]}")

    print("\nMemória Principal:")
    tamanho_mp_bytes = tamanho_mp_kb * 1024
    num_blocos = tamanho_mp_bytes // (palavras_por_bloco * tamanho_palavra_bytes)
    endereco_mp_bits = calcular_tamanho_endereco_mp(tamanho_mp_kb)

    for bloco in range(num_blocos):
        inicio = bloco * palavras_por_bloco
        fim = (bloco + 1) * palavras_por_bloco
        print(f"Bloco {bloco}: {memoria_principal[inicio:fim]}")

#função que imprime a taxa de acertos
def imprimir_taxa_de_acerto(counters):
    total_acessos = counters['hits'] + counters['misses']
    taxa_acerto = (counters['hits'] / total_acessos) * 100 if total_acessos > 0 else 0
    print(f"Taxa de acerto: {taxa_acerto:.2f}% ({counters['hits']} hits, {counters['misses']} misses)")

#função para ler um arquivo de endereço
def ler_arquivo_enderecos(nome_arquivo):
    enderecos = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            endereco = int(linha.strip())
            enderecos.append(endereco)
    return enderecos