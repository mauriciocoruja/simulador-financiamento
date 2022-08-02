

# Simulador de Financiamento e Amortização

---
## Conteúdos
 
- [Overview](#Overview)
- [Rodando a aplicação](#Rodando-a-aplicação)
- [Documentação](#Documentação)


## Overview

---

Este projeto pretende ajudar as pessoas a simular seus financiamentos e conseguir se planejar para o futuro tendo 
estimativa do número de parcelas e quando finalizarão seu financiamento dado um valor mensal de amortização 
adicional.

A ideia nasceu de um video do [Primo Pobre](https://www.youtube.com/c/PrimoPobre) onde ele compartilha um método 
para finalizar um financiamento de 30 anos em 3. Através de amortizações adicionais mensais, que por consequência 
diminui o tempo de financiamento, reduzindo os juros.

Tenha um preview — [Jupiter Notebook - Demo](https://github.com/mauriciocoruja/simulador-financiamento/blob/3289d7769ed86c0345a6ff887b0c319d93998e81/jupyter_demo.ipynb)


## Rodando a aplicação

---

Alternativa 1:
- Requisitos:
  - Python 3 — [veja aqui](https://realpython.com/installing-python/) como instalar em todos os sistemas operacionais
- Clone o repositório (botão verde acima)
- Navegue até a pasta do repositório clonado
- Crie um ambiente virtual para executar o programa — 
[veja aqui](https://realpython.com/python-virtual-environments-a-primer/#create-it) como fazer.
- Por último instale as dependências descritas no arquivo ```requirements.txt```. Podendo também ser feito através 
    do comando


      $ pip install -r requirements.txt

[//]: # (Alternativa 2)

[//]: # ()
[//]: # (- Experimente o código através de um ambiente on-line )

[//]: # ([![Binder]&#40;https://mybinder.org/badge_logo.svg&#41;]&#40;https://mybinder.org/v2/gh/mauriciocoruja/simulador-financiamento/HEAD?labpath=jupyter_demo.ipynb&#41;)

## Documentação

---
- Na pasta raiz do projeto execute o comando no terminal:
 
 
      $ pydoc simulador_financiamento/simulador_financiamento 
  para visualizar a documentação no terminal; ou execute o comando ```pydoc -b``` para iniciar um servidor web local e 
  visualizar a documentação em uma página web.

