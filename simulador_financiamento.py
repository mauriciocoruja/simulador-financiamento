import locale
from datetime import datetime

import pandas as pd
from dateutil import rrule


def calcular_juros(valor_do_financiamento: float,
                   taxa_de_juros: float) -> float:
    """Calcula o valor de juros do financiamento

    :param valor_do_financiamento: Valor financiado.
    :param taxa_de_juros: Valor da taxa de juros do financiamento.
    :return: Valor de juros referente ao valor do financiamento
    """
    return valor_do_financiamento * ((taxa_de_juros / 100) / 12)


def calcular_parcela(valor_amortizacao: float,
                     valor_juros: float,
                     demais_valores: float = 0) -> float:
    """Calcula o valor da parcela do financiamento

    :param valor_amortizacao: Valor de amortização do financiamento
    :param valor_juros: Valor de juros do financiamento — preferencialmente taxa de juros ao ano (ex.: 10% a.a)
    :param demais_valores: Valor de demais tarifas ou taxas (exemplo: Seguro, Taxa bancaria de financiamento)
    :return: Valor da parcela, baseado no valor restante do financiamento
    """
    return valor_amortizacao + valor_juros + demais_valores


def calcular_amortizacao(quantidade_parcelas: int, valor_emprestimo: float) -> float:
    """ Calcula o valor de amortização dada a quantidade de parcelas e valor do financiamento

    :param quantidade_parcelas: Quantidade de parcelas do financiamento
    :param valor_emprestimo: Valor financiado.
    :return: Valor a ser amortizado mensalmente
    """
    valor_amortizacao = valor_emprestimo / quantidade_parcelas
    return valor_amortizacao


def gerar_dados(valor_financiamento: float,
                taxa_juros: float,
                quantidade_parcelas: int,
                amortizacao: float = 0) -> list:
    """
    :param valor_financiamento: Valor total do financiamento
    :param taxa_juros: Taxa de juros (valor decimal)
    :param quantidade_parcelas: Total de parcelas do financiamento
    :param amortizacao: Volor médio de amortizações mensais
    :return: Lista de tuplas com as informações geradas
    """
    amortizacao_financiamento = calcular_amortizacao(quantidade_parcelas, valor_financiamento)
    dados = []
    amortizacao_adicional = amortizacao

    for i in range(quantidade_parcelas):

        juros = calcular_juros(valor_financiamento, taxa_juros)
        amortizacao_total = amortizacao_financiamento + amortizacao_adicional
        valor_parcela = calcular_parcela(amortizacao_financiamento, juros)
        valor_financiamento -= amortizacao_total

        if valor_financiamento - amortizacao_financiamento < 0:
            amortizacao_adicional += valor_financiamento
            valor_financiamento -= valor_financiamento
            adicionar_dados(
                valor_parcela,
                amortizacao_financiamento,
                amortizacao_adicional,
                juros,
                valor_financiamento,
                dados
            )

            adicionar_dados(calcular_totais(dados)[0],
                            calcular_totais(dados)[1],
                            calcular_totais(dados)[2],
                            calcular_totais(dados)[3],
                            0,
                            dados)
            break

        adicionar_dados(
            valor_parcela,
            amortizacao_financiamento,
            amortizacao_adicional,
            juros,
            valor_financiamento,
            dados)

    adicionar_dados(calcular_totais(dados)[0],
                    calcular_totais(dados)[1],
                    calcular_totais(dados)[2],
                    calcular_totais(dados)[3],
                    0,
                    dados)

    return dados


def calcular_totais(dados: list) -> tuple:
    """Calcula o total pago individualmente nas parcelas, juros e amortizações.

    :param dados: lista com os dados do financiamento calculados.
    :return: tupla com os dados totais calculados
    """

    valor_parcela, amortizacao_financiamento, amortizacao_adicional, juros = 0, 0, 0, 0

    for each in dados:
        valor_parcela += each[0]
        amortizacao_financiamento += each[1]
        amortizacao_adicional += each[2]
        juros += each[3]

    return valor_parcela, amortizacao_financiamento, amortizacao_adicional, juros


def adicionar_dados(valor_parcela: float,
                    amortizacao_financiamento: float,
                    amortizacao_adicional: float,
                    juros: float,
                    valor_financiamento: float,
                    dados_financiamento: list) -> None:
    """ Adiciona em uma lista todos os dados necessarios para montar a tabela com a simulação do financiamento

    :param valor_parcela:
    :param amortizacao_financiamento:
    :param amortizacao_adicional:
    :param juros:
    :param valor_financiamento:
    :param dados_financiamento:
    :return: none
    """
    dados_financiamento.append(
        (valor_parcela,
         amortizacao_financiamento,
         amortizacao_adicional,
         juros,
         valor_financiamento))


def gerar_tabela_meses(dados_calculados: list,
                       start: str = datetime.strftime(datetime.now(), "%m/%y")) -> str:
    """Gerar dados a partir de uma lista de dados

    :param dados_calculados:
    :param start:
    :return: Conteudo do dataframe como string
    """
    dados_formatados = []
    for i in dados_calculados:
        dados_formatados.append([formatar_valor(j) for j in i])

    index = list(f for f in configurar_meses(dados_formatados, start))
    df = pd.DataFrame(dados_formatados,
                      columns=['Parcela', 'Amortização', 'Amortização adicional', 'Juros', 'Saldo Devedor'],
                      index=index)
    return df.to_string(index=True)


def gerar_tabela_parcela(dados_calculados: list) -> str:
    """Gerar uma representação em forma de tabela a partir de uma lista de dados do financiamento

    :param dados_calculados:
    :return: Conteudo do dataframe como string
    """

    dados_formatados = []

    for i in dados_calculados:
        dados_formatados.append([formatar_valor(j) for j in i])

    df = pd.DataFrame(dados_formatados,
                      columns=['Parcela', 'Amortização', 'Amortização adicional', 'Juros', 'Saldo Devedor']).shift()[1:]

    return df.to_string(index=True)


def configurar_meses(dados: list,
                     start: str = datetime.strftime(datetime.now(), "%m/%y")) -> list[str]:
    """Criar lista com range de datas formatadas

    :param dados: dados do financiamento calculado.
    :param start: data de inicio do pagamento do financiamento, e estimar o fim do financiamento
    :return: lista de datas no formato m/a (07/22)
    """
    start_strptime = datetime.strptime(start, "%m/%y")
    return [e.strftime("%m/%y") for e in
            list(rrule.rrule(rrule.MONTHLY, count=len(dados), dtstart=start_strptime))]


def formatar_valor(valor) -> str:
    """Formatar os valores para o formato brasileiro (000.000,00)

    :param valor: valor a ser formatado
    :return: string com o valor monetario formatado

    """
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    return locale.format_string("%.2f", valor, grouping=True)


def criar_arquivo(conteudo: str):
    with open("simulacao_financiamento.html", "w") as f:
        f.writelines(conteudo)


def main():
    valor_financiamento = float(input("Insira o valor Financiado: "))
    taxa_juros = float(input("Insira a taxa de juros: "))
    prazo = int(input("Insira o prazo para pagamento: "))
    amortizacao_adicional = float(input("Caso queira amortizar adicionalmente, insira a media mensal: "))
    dados = gerar_dados(valor_financiamento, taxa_juros, prazo, amortizacao_adicional)

    print(gerar_tabela_parcela(dados))


if __name__ == '__main__':
    main()
