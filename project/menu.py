def exibir_menu():
    largura_total = 60
    largura_texto = largura_total - 4  # Subtrai bordas e espaços

    print("\n" + "═" * largura_total)
    print("║" + " " * ((largura_texto - len("Menu de Opções")) // 2) + "Menu de Opções" + " " * (
                (largura_texto - len("Menu de Opções") + 1) // 2) + "  ║")
    print("═" * largura_total)
    print("║ {:<56} ║".format("L - Ler arquivo de configuração"))
    print("║ {:<56} ║".format("I - Imprimir informações da cache e da memória principal"))
    print("║ {:<56} ║".format("E - Acessar endereço da memória"))
    print("║ {:<56} ║".format("A - Ler arquivo de endereços e acessar endereços"))
    print("║ {:<56} ║".format("T - Imprimir taxa de acerto da cache"))
    print("║ {:<56} ║".format("X - Sair do programa"))
    print("═" * largura_total)

    opcao = input("Escolha uma opção: ").upper()
    return opcao
