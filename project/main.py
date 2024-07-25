from calculos import (calcular_valores, inicializar_cache, acessar_cache,
                      imprimir_informacoes, imprimir_taxa_de_acerto,preencher_memoria_principal,
                      ler_arquivo_entrada, verificar_dados, ler_arquivo_enderecos)
from menu import exibir_menu

def main():
    informacoes = {}
    cache = []
    memoria_principal = []
    counters = {'hits': 0, 'misses': 0}

    while True:
        opcao = exibir_menu()

        if opcao == 'L':
            while True:
                nome_arquivo = input("Digite o nome do arquivo de configuração (sem a extensão .txt): ")
                nome_arquivo += '.txt'
                try:
                    informacoes = ler_arquivo_entrada(nome_arquivo)
                    verificar_dados(informacoes)
                    w, num_linhas_cache, s, tag_bits = calcular_valores(
                        informacoes['palavras_por_bloco'],
                        informacoes['tamanho_cache_kb'],
                        informacoes['linhas_por_conjunto'],
                        informacoes['tamanho_mp_kb']
                    )
                    cache = inicializar_cache(num_linhas_cache)
                    memoria_principal = preencher_memoria_principal(informacoes['tamanho_mp_kb'])
                    print("Arquivo lido com sucesso!")
                    break
                except FileNotFoundError:
                    print(f"Arquivo '{nome_arquivo}' não encontrado. Tente novamente.")
                except Exception as e:
                    print(f"Erro ao ler o arquivo: {e}. Tente novamente.")

        elif opcao == 'I':
            imprimir_informacoes(informacoes, cache, memoria_principal)

        elif opcao == 'E':
            endereco = int(input("Digite o endereço de memória para acessar: "))
            acessar_cache(cache, endereco, informacoes['palavras_por_bloco'], w, s, tag_bits, memoria_principal, counters)

        elif opcao == 'A':
            while True:
                nome_arquivo = input("Digite o nome do arquivo de endereços (sem a extensão .txt): ")
                nome_arquivo += '.txt'
                try:
                    enderecos = ler_arquivo_enderecos(nome_arquivo)
                    for endereco in enderecos:
                        acessar_cache(cache, endereco, informacoes['palavras_por_bloco'], w, s, tag_bits,
                                      memoria_principal, counters)
                    print("Arquivo de endereços processado com sucesso!")
                    break
                except FileNotFoundError:
                    print(f"Arquivo '{nome_arquivo}' não encontrado. Tente novamente.")
                except Exception as e:
                    print(f"Erro ao ler o arquivo: {e}. Tente novamente.")

        elif opcao == 'T':
            imprimir_taxa_de_acerto(counters)

        elif opcao == 'X':
            imprimir_taxa_de_acerto(counters)

            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
