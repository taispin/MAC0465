# -*- coding: utf-8 -*-

# MAC0465 - Biologia Computacional
# NOME: Tais Pinheiro
# NUSP: 7580421
# Exercício Programa 2 - Alinhador Multiplo Otimo

import sys
import numpy as np

### MAIN
def main ():
    if len(sys.argv) != 1:
        help()      # Executar sem todos os argumentos necessários mostra ajuda
        sys.exit()

    else:
        entrada = raw_input('\nInforme: r q g k e k sequencias que serão alinhadas:\n\n')
        parametros = ajuste_parametros(entrada)

        r = parametros[0]
        q = parametros[1]
        g = parametros[2]
        k = parametros[3]

        tamanhos = []
        sequencias = []
        deltas = []
        m = []
        v = []
        c = []
        s = []
        sequencias = list(parametros[4])

        print('r: '+str(r))
        print('q: '+str(q))
        print('g: '+str(g))
        print('k: '+str(k))

        tamanhos = define_tamanhos(k,sequencias)

        sequencias.insert(0,str(0))

        m = monta_matriz(k,sequencias,tamanhos)
        v = preenche_matriz(k, tamanhos)
        c = preenche_controle(k, tamanhos)
        s = preenche_sequencia(k, tamanhos)
        deltas = gerador_de_deltas(k)

        calcula_alinhamento_otimo(m, v,c, s, tamanhos,sequencias, k, r, q, g)

# Informa como o programa deve ser executado
def help():
    print('\nEXECUÇÃO DO EP2: python ep2.py')
    print('\nSiga as orientações que você vê na tela para informar os dados de entrada.\n')

def monta_alinhamento(max, s, k):

    linhas = len(s)
    colunas = len(s[0])

    mostrar = []
    indice = [0]*k
    for i in range(k):
        indice[i] = str(i+1) + ':'

    mostrar.append(indice)

    posl = linhas - 1
    posc = colunas - 1

    while (posl + posc) !=  0:
        col = s[posl][posc][1]
        mostrar.insert(1,col)
        posl = s[posl][posc][0][0]
        posc = s[posl][posc][0][1]

    print("O alinhamento ótimo tem valor: " + str(max))
    print("O alinhamento ótimo é dado por: ")

    a = np.array(mostrar)

    b = a.transpose()

    print(b)

def calcula_alinhamento_otimo(m,v, c, s, tamanhos, sequencias, k, r, q, g):

    p = []
    #gera todas as variaçoes de deltas
    p = gerador_de_deltas(k)

    otimo = 0

    for i in range(len(m)):
        for j in range(len(m[i])):
            if (i + j) != 0:
                [c, v, s] = calcula_otimo_q(m[i][j], p, v, c, s, tamanhos, sequencias, k, r,q,g)


    monta_alinhamento(v[i][j], s, k)

def calcula_otimo_q(ponto_q, p, v, c, s, tamanhos, sequencias, k, r, q, g):

    zeros = 1
    max = 0
    for i in range(k):
        if ponto_q[i] != 0:
            zeros = 0

    #Se estivermos no ponto onde todas as coordenadas são zeros, devolvemos o 0
    if zeros == 1:
        max = 0

    else:
        verificar_delta = []
        verificar_delta = list(deltas_validos(ponto_q,p,k))

        verificar_p = []
        verificar_p = list(p_validos(ponto_q,verificar_delta,k))

        colun = []

        [linq, colq] = (posicao(ponto_q, len(v), tamanhos, k))


        [lin, col] = posicao(verificar_p[0], len(v), tamanhos, k)

        coluna_p = c[lin][col]

        peso = w(ponto_q,verificar_p[0], coluna_p, sequencias, k, r, q, g)[0]
        max = v[lin][col] + peso

        for i in range(len(verificar_p)):
            [lin, col] = posicao(verificar_p[i], len(v), tamanhos, k)
            coluna_p = list(c[lin][col])
            [peso, nova, colun] = w(ponto_q,verificar_p[i], coluna_p, sequencias, k, r, q, g)
            valor = v[lin][col] + peso
            if valor >= max:
                max = valor
                c[linq][colq] = list(nova)
                v[linq][colq] = int(max)
                s[linq][colq] = [list([lin,col]),list(colun)]

    return [list(c), list(v), list(s)]

#devolve o valor w para dois pontos p e q e o controle dos caracteres
# das sequencias
def w(ponto_q,ponto_p,coluna_p, sequencias, k, r, q, g):

    coluna = [0]*k
    nova = [0]*k


    for i in range(k):
        if (ponto_q[i] - ponto_p[i]) == 0:
            coluna[i] = '-'
            nova[i] = coluna_p[i]
        else:
            nova[i] = coluna_p[i] + 1
            coluna[i] = sequencias[i+1][coluna_p[i]+1]

    return [pontua_coluna(k,coluna,r,q,g), nova, coluna]


def deltas_validos(ponto, verificar, k):

    validos = []
    inclui = 1
    for i in range(len(verificar)):
        for j in range(k):
            if ponto[j] == 0 and verificar[i][j] != 0:
                inclui = 0
        if inclui == 1:
            validos.append(list(verificar[i]))

        inclui = 1

    return validos

def p_validos(ponto, verificar, k):

    validos = []
    incluir = [0]*k
    for i in range(len(verificar)):
        for j in range(k):
            incluir[j] = ponto[j] - verificar[i][j]
        validos.append(list(incluir))

    return validos


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


def posicao(ponto, linhas, tamanhos, k):

    col = ponto[k-1]
    lin = ponto[0]

    linha_maxima_1 = (linhas/(tamanhos[1]+1)) * (ponto[0]+1)
    linhas_total = linhas

    i = 2
    while i < k:
        linhas_total = linhas_total/(tamanhos[i-1]+1)
        linha_maxima_2 = (linhas_total/(tamanhos[i]+1)) * (ponto[i-1]+1)
        lin = linha_maxima_1 - (linhas_total - linha_maxima_2)
        linha_maxima_1 = lin

        i = i+1


    if k > 2:
        lin = lin - 1

    return [lin, col]


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

    return m


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

    v = [0]*linhas
    for i in range(linhas):
        v[i] = [0]*colunas

    v[0][0] = 0

    return v

def preenche_controle(k,tamanhos):
    c = []

    #O numero de colunas eh o tamanho da ultima sequencia
    colunas = tamanhos[k]+1

    #O numero de linhas eh o produtos das demais sequencias
    linhas = 1
    i = 1
    while i <= k-1:
        linhas = linhas * (tamanhos[i]+1)
        i = i + 1

    c = [0]*linhas
    for i in range(linhas):
        c[i] = [0]*colunas

    c[0][0] = [0]*k

    return c

def preenche_sequencia(k,tamanhos):
    s = []

    #O numero de colunas eh o tamanho da ultima sequencia
    colunas = tamanhos[k]+1

    #O numero de linhas eh o produtos das demais sequencias
    linhas = 1
    i = 1
    while i <= k-1:
        linhas = linhas * (tamanhos[i]+1)
        i = i + 1

    s = [0]*linhas
    for i in range(linhas):
        s[i] = [0]*colunas

    s[0][0] = [[0,0],[0,0]]

    return s

def gerador_de_deltas(k):
    deltas = []

    unidade = []
    deltas = list(gerador_recursivo(1, k, deltas, unidade))
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


# Calcula o score de uma coluna com k caracteres
def pontua_coluna(k, coluna, r, q, g):

    score = 0
    for i in range(k):
        score = score + pontua(k,i,coluna,r,q,g)

    return score

def pontua(k,ini,coluna, r, q, g):

    score = 0

    for i in range(k - ini -1):
        if coluna[ini] == coluna[ini+i+1]:
            if coluna[ini] == '-':
                score = score + 0
            else:
                score = score + r
        else:
            if coluna[ini] == '-':
                score = score + g
            elif coluna[ini+i+1] == '-':
                score = score + g
            else:
                score = score + q
    return score

def mostra_matriz(m):
    for i in range(len(m)):
        print(m[i])
        #print('-----------')



if __name__ == "__main__":
    main()
