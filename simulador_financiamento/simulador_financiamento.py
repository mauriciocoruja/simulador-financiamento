"""
Métodos para gerar os dados do financiamento
"""
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

    **Examples**

    >>> calcular_juros(100, 7.5)
    0.625

    >>> calcular_juros('',7.5)
    Traceback (most recent call last):
        ...
    TypeError: can't multiply sequence by non-int of type 'float'

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

    **Examples**:

    >>> calcular_parcela(200, 250)
    450

    >>> calcular_parcela(200, 250, 2000)
    2450
    """
    return valor_amortizacao + valor_juros + demais_valores


def calcular_amortizacao(quantidade_parcelas: int, valor_emprestimo: float) -> float:
    """ Calcula o valor de amortização dada a quantidade de parcelas e valor do financiamento

    :param quantidade_parcelas: Quantidade de parcelas do financiamento
    :param valor_emprestimo: Valor financiado.
    :return: Valor a ser amortizado mensalmente

    **Examples**

    >>> calcular_amortizacao(360, 3600)
    10.0
    """
    valor_amortizacao = valor_emprestimo / quantidade_parcelas
    return valor_amortizacao


def gerar_dados(valor_financiamento: float,
                taxa_juros: float,
                quantidade_parcelas: int,
                amortizacao: float = 0) -> list[tuple]:
    """Gera/calcula os dadas do financiamento

    :param valor_financiamento: Valor total do financiamento
    :param taxa_juros: Taxa de juros (valor decimal)
    :param quantidade_parcelas: Total de parcelas do financiamento
    :param amortizacao: Volor médio de amortizações mensais
    :return: Lista de tuplas com as informações geradas

    **Examples**

    >>> gerar_dados(1000,10,2)
    [(508.3333333333333, 500.0, 0, 8.333333333333334, 500.0), (504.1666666666667, 500.0, 0.0, 4.166666666666667, 0.0)]
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

            break

        adicionar_dados(
            valor_parcela,
            amortizacao_financiamento,
            amortizacao_adicional,
            juros,
            valor_financiamento,
            dados)
    # TODO: Adicionar total em um dataframe separado e concatatenar tendo um index 'total'

    return dados


def calcular_totais(dados: list[tuple]) -> tuple:
    """Calcula o total pago individualmente nas parcelas, juros e amortizações.

    :param dados: lista com os dados do financiamento calculados.
    :return: tupla com os dados totais calculados

    **Examples**

    >>> calcular_totais([(508.3333333333333, 500.0, 0, 8.333333333333334, 500.0),
    ...        (504.1666666666667, 500.0, 0.0, 4.166666666666667, 0.0)])
    (1012.5, 1000.0, 0.0, 12.5)
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
                    dados_financiamento: list[tuple]) -> None:
    """ Adiciona em uma lista todos os dados necessarios para montar a tabela com a simulação do financiamento

    :param valor_parcela: valor da parcela do financiamento.
    :param amortizacao_financiamento: valor da amortização do financiamento.
    :param amortizacao_adicional: valor adicional de amortização do financimento.
    :param juros: valor valor dos juros do financiamento.
    :param valor_financiamento: valor total financiado.
    :param dados_financiamento: lista com os dados calculados do financiamento.
    :return: none

    **Examples**

    >>> dados = [(508.3333333333333, 500.0, 0, 8.333333333333334, 500.0), (504.1666666666667, 500.0, 0.0, 4.166666666666667, 0.0)]
    >>> adicionar_dados(510.10, 500.0, 0, 9.50, 500.0, dados)
    >>> len(dados)
    3
    """
    dados_financiamento.append(
        (valor_parcela,
         amortizacao_financiamento,
         amortizacao_adicional,
         juros,
         valor_financiamento))


def gerar_tabela_meses(dados_calculados: list[tuple],
                       data_inicio: str = datetime.strftime(datetime.now(), "%m/%y")) -> str:
    """Gerar uma representação em forma de tabela a partir de uma lista de dados, onde o index informa os meses de pagamento do financiamento.

    :param dados_calculados: lista com os dados das parcelas do financiamento.
    :param data_inicio: mês e ano do início do financiamento.
    :return: Conteudo do dataframe como string

    **Examples**

    >>> print(gerar_tabela_meses(list(f for f in gerar_dados(10000, 7.4, 2))))
            Parcela Amortização Amortização adicional  Juros Saldo Devedor
    07/22  5.061,67    5.000,00                  0,00  61,67      5.000,00
    08/22  5.030,83    5.000,00                  0,00  30,83          0,00
    """
    dados_formatados = []
    for i in dados_calculados:
        dados_formatados.append([formatar_valor(j) for j in i])

    index = list(f for f in configurar_meses(dados_formatados, data_inicio))
    df = pd.DataFrame(dados_formatados,
                      columns=['Parcela', 'Amortização', 'Amortização adicional', 'Juros', 'Saldo Devedor'],
                      index=index)
    return df


def gerar_tabela_parcela(dados_calculados: list[tuple]) -> str:
    """Gerar uma representação em forma de tabela a partir de uma lista de dados, onde o index informa o número de parcelas do financiamento.

    :param dados_calculados: lista com os dados das parcelas do financiamento.
    :return: Conteudo do dataframe como string

    **Examples**

    >>> print(gerar_tabela_parcela(list(f for f in gerar_dados(10000, 7.4, 2))))
        Parcela Amortização Amortização adicional  Juros Saldo Devedor
    1  5.061,67    5.000,00                  0,00  61,67      5.000,00
    2  5.030,83    5.000,00                  0,00  30,83          0,00
    """

    dados_formatados = []

    for i in dados_calculados:
        dados_formatados.append([formatar_valor(j) for j in i])

    df = pd.DataFrame(dados_formatados,
                      columns=[
                          'Parcela', 'Amortização',
                          'Amortização adicional',
                          'Juros', 'Saldo Devedor'
                      ],
                      index=pd.RangeIndex(start=1, stop=len(dados_formatados) + 1))

    return df


def configurar_meses(dados: list[tuple],
                     data_inicio: str = datetime.strftime(datetime.now(), "%m/%y")
                     ) -> list[str]:
    """Criar lista com range de datas formatadas

    :param dados: dados do financiamento calculado.
    :param data_inicio: data de início do pagamento do financiamento.
    :return: lista de datas no formato m/a (07/22)

    **Examples**

    >>> configurar_meses(list(e for e in range(2)), '07/22')
    ['07/22', '08/22']
    """
    start_strptime = datetime.strptime(data_inicio, "%m/%y")
    return [e.strftime("%m/%y") for e in
            list(rrule.rrule(rrule.MONTHLY, count=len(dados), dtstart=start_strptime))]


def formatar_valor(valor: float) -> str:
    """Formatar os valores para o formato brasileiro (000.000,00)

    :param valor: valor a ser formatado
    :return: string com o valor monetario formatado

    **Examples**

    >>> formatar_valor(1000.1245)
    '1.000,12'
    """
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    return locale.format_string("%.2f", valor, grouping=True)


def criar_arquivo(conteudo: str) -> None:
    with open("simulacao_financiamento.html", "w") as f:
        f.writelines(conteudo)
