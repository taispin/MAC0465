# -*- coding: utf-8 -*-

# MAC0465 - Biologia Computacional
# NOME: Tais Pinheiro
# NUSP: 7580421
# Exercício Programa 2 - Alinhador Multiplo Otimo

import sys

### MAIN
def main ():
    if len(sys.argv) != 1:
        help()      # Executar sem todos os argumentos necessários mostra ajuda
        sys.exit()

    else:
        #entrada = raw_input('\nInforme: r q g k e k sequencias que serão alinhadas:\n\n')
        entrada = "2 1 0 3 atc cgga cact"
        parametros = ajuste_parametros(entrada)

        r = parametros[0]
        q = parametros[1]
        g = parametros[2]
        k = parametros[3]

        tamanhos = []
        sequencias = []
        deltas = []
        sequencias = list(parametros[4])

        print('r: '+str(r))
        print('q: '+str(q))
        print('g: '+str(g))
        print('k: '+str(k))

        tamanhos = define_tamanhos(k,sequencias)

        sequencias.insert(0,str(0))

        print('\nSequencias e seus tamanhos:\n')
        print(sequencias)
        print(tamanhos)

        monta_matriz(k,sequencias,tamanhos)
        v = preenche_matriz(k, tamanhos)
        deltas = gerador_de_pontos(k)
        print(deltas)

        #Agora eu tenho os parametros e sequencias.
        #Próximo passo: Como montar a matriz

# Informa como o programa deve ser executado
def help():
    print('\nEXECUÇÃO DO EP2: python ep2.py')
    print('\nSiga as orientações que você vê na tela para informar os dados de entrada.\n')

# Recebe uma string e extrai os parametros de entrada
def ajuste_parametros(entrada):
    lista = entrada.split()

    #Parametros inteiros
    r = int(lista[0])
    q = int(lista[1])
    g = int(lista[2])
    k = int(lista[3])

    #Sequencias
    sequencias = lista[4:]

    return[r,q,g,k,sequencias]


#Recebe um numero k e uma lista com k sequencias
#Devolve uma lista em que cada indice i tem o tamanho da sequencia sequencias[i]
def define_tamanhos(k, sequencias):

    tamanhos = []
    tamanhos.append(0)
    for i in range(k):
        tamanhos.append(len(sequencias[i]))

    return tamanhos

def monta_matriz(k,sequencias, tamanhos):

    #acrescentei a subsequencia vazia para cada sequencia
    for i in range(k):
        sequencias[i+1] = str(0) + sequencias[i+1][0:]

    #Numero de celulas na matriz M = (n1+1)*(n2+1)*...*(nk+1)
    #Formato da Matriz M = ((n1+1)*...*(nk-1 +1))x(nk+1)

    #O numero de colunas eh o tamanho da ultima sequencia
    colunas = tamanhos[k]+1

    #O numero de linhas eh o produtos das demais sequencias
    linhas = 1
    i = 1
    while i <= k-1:
        linhas = linhas * (tamanhos[i]+1)
        i = i + 1

    #Montamos a matriz m
    m = ['x']*linhas
    for i in range(linhas):
        m[i] = ['x']*colunas

    #numero de celulas da matriz
    celulas = linhas * colunas

    negocio = []
    m = escreve_recursivo(1, sequencias, tamanhos, negocio, linhas, colunas, k, m)
    mostra_matriz(m)


def escreve_recursivo(id, sequencias, tamanhos, gravar, linhas, colunas, k, m):

    #base da recursão
    if id == k+1:
        col = gravar[k-1]
        lin = gravar[0]

        #Matriz funciona para k qualquer.
        #no exeplo funciona com #lin = ((cel/colunas)-1)+(gravar[0]*colunas)
        linha_maxima_1 = (linhas/(tamanhos[1]+1)) * (gravar[0]+1)
        linhas_total = linhas

        i = 2
        while i < k:
            linhas_total = linhas_total/(tamanhos[i-1]+1)
            linha_maxima_2 = (linhas_total/(tamanhos[i]+1)) * (gravar[i-1]+1)
            lin = linha_maxima_1 - (linhas_total - linha_maxima_2)
            linha_maxima_1 = lin

            i = i+1

        #print(gravar)

        if k > 2:
            lin = lin - 1
        #print(lin)
        #print(col)
        if(m[lin][col] == 'x'):
            m[lin][col] = list(gravar)

    #recursão
    elif id <= k:
        tam = len(sequencias[id])

        for i in range(tam):
            gravar.append(i)
            escreve_recursivo(id+1, sequencias, tamanhos, gravar, linhas, colunas, k, m)
            lixo = gravar.pop()

    return m


def preenche_matriz(k,tamanhos):
    v = []

    #O numero de colunas eh o tamanho da ultima sequencia
    colunas = tamanhos[k]+1

    #O numero de linhas eh o produtos das demais sequencias
    linhas = 1
    i = 1
    while i <= k-1:
        linhas = linhas * (tamanhos[i]+1)
        i = i + 1

    v = ['x']*linhas
    for i in range(linhas):
        v[i] = ['x']*colunas

    v[0][0] = 0

    mostra_matriz(v)

def gerador_de_pontos(k):
    deltas = []

    unidade = []
    deltas = gerador_recursivo(1, k, deltas, unidade)
    del deltas[0]

    return deltas

def gerador_recursivo(id, k, lista_delta, delta):

    #base da recursão
    if id == k+1:

        lista_delta.append(list(delta))

    #recursão
    elif id <= k:

        for i in range(2):
            delta.append(i)
            gerador_recursivo(id+1, k, lista_delta, delta)
            lixo = delta.pop()

    return lista_delta

def mostra_matriz(m):
    for i in range(len(m)):
        print(m[i])
        #print('-----------')



if __name__ == "__main__":
    main()
