from simulador_financiamento import simulador_financiamento as sf


def main():
    step: int = 0
    while True:
        try:
            if step == 0:
                valor_financiamento = float(
                    input("Insira o valor Financiado: "))
                step = 1
            if step == 1:
                taxa_juros = float(
                    input("Insira a taxa de juros: "))
                step = 2
            if step == 2:
                prazo = int(
                    input("Insira o prazo para pagamento: "))
                step = 3
            if step == 3:
                amortizacao_adicional = float(input("Caso queira amortizar adicionalmente, insira a media mensal: "))
                dados = sf.gerar_dados(
                    valor_financiamento, taxa_juros,
                    prazo, amortizacao_adicional)
                return sf.gerar_tabela_parcela(dados)
        except ValueError:
            print("Por favor, informe um número inteiro ou decimal")
        else:
            break
    exit(0)


if __name__ == '__main__':
    import doctest

    doctest.testmod(sf)
    print(main())
