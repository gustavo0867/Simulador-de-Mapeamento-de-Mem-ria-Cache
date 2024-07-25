# Simulador de Mapeamento de Memória Cache com LFU

## Descrição

Este projeto é parte do trabalho de Organização e Arquitetura de Computadores, que consiste na criação de uma aplicação para emular o mapeamento de memória cache com mapeamento associativo por conjunto. Se a memória cache estiver cheia, o programa usa o algoritmo de substituição Least Frequently Used (LFU).

## Funcionalidades

- Leitura de um arquivo de entrada com informações sobre a memória principal e cache.
- Menu interativo que permite:
  - Carregar um arquivo com os dados de configuração.
  - Informar um endereço da memória principal (MP) para acesso.
  - Ler um arquivo com uma sequência de endereços da MP.
  - Sair do programa.
- Apresentação das informações da memória principal e cache na tela.
- Indicação das operações de substituição na cache.
- Exibição das taxas de falhas e acertos, e posições substituídas na cache.

## Entrada

O programa aceita arquivos de entrada em modo texto, contendo:

- Tamanho da memória principal (até 256KB).
- Quantidade de palavras por bloco na MP (2, 4 ou 8).
- Tamanho da cache (até 32KB).
- Número de linhas por conjunto da cache (mínimo de 2 linhas, máximo é número de linhas/2).

## Requisitos

- Python 3.6+
- Arquivos de entrada com configuração da memória principal e cache.


