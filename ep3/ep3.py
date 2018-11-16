# -*- coding: utf-8 -*-

# MAC0465 - Biologia Computacional
# NOME: Tais Pinheiro
# NUSP: 7580421
# Exercício Programa 3 - Reconstrução de uma supersequência comum ao nível t.

import sys
import numpy as np

### MAIN
def main ():
    if len(sys.argv) != 1:
        help()      # Executar sem todos os argumentos necessários mostra ajuda
        sys.exit()

    else:
        #entrada = raw_input('\nInforme um limiar inteiro t e o conjunto de strings separadas por espaços:\n\n')

        entrada = "3 AGTATTGGCAATC AATCGATG ATGCAAACCT CCTTTTGG TTGGCAATCACT"
        print('entrada: ' + entrada)
        parametros = ajuste_parametros(entrada)
        nstrings = len(parametros[1])

        t = parametros[0]
        strings = parametros[1]
        tamanhos = parametros[2]
        print(tamanhos)

        eq = compara_strings(strings[0],strings[4], t)
        print('igualdade: [' + str(eq) + ']')

        matriz = []
        matriz = list(matriz_adjacencias(strings, nstrings, t))
        mostra_matriz(matriz)

        #mostra_parametros(parametros)
        print('\nProcessando...\n')



#Recebe as strings de entrada e montra uma matriz de adjacencias reperesentando o grafo
def matriz_adjacencias(strings, n, t):

    #Montamos a matriz de adjacencias adj
    adj = []

    adj = [0]*n
    for i in range(n):
        adj[i] = [-1]*n

    for i in range(n):
        for j in range(n):
            if i == j:
                #distancia de um nó para ele mesmo
                adj[i][j] = 0
            else:
                adj[i][j] = compara_strings(strings[i],strings[j],t)

    return adj



def mostra_matriz(m):
    for i in range(len(m)):
        print(m[i])
        #print('-----------')


# Recebe duas strings e compara o quanto são similares
def compara_strings(a,b,t):

    if len(a)<= t:
        igual = 0
    elif len(b) <= t:
        igual = 0
    else:
        igual = 0
        i = t - 1
        go = 1
        while go == 1:
            i = i + 1
            cont = len(a) - i
            if len(a) > i and len(b) > i:
                #compara suf de tamanho i de a com pref tam t de b
                if a[cont:] == b[0:i]:
                    igual = i

            else:
                go = 0

    return igual




########## TRATANDO OS PARAMETROS DE ENTRADA ########

# Informa como o programa deve ser executado
def help():
    print('\nEXECUÇÃO DO EP3: python ep3.py\n')
    print('\nSiga as orientações que você vê na tela para informar os dados de entrada.\n')


# Recebe uma string e extrai os parametros de entrada
def ajuste_parametros(entrada):
    lista = entrada.split()

    #limiar t
    t = int(lista[0])

    #Sequencias
    sequencias = list(lista[1:])
    tamanhos = []

    for i in range(len(sequencias)):
        tamanhos.append(len(sequencias[i]))

    return[t,sequencias, tamanhos]

def mostra_parametros(parametros):

    nstrings = len(parametros[1])

    print('t: ' + str(parametros[0]))
    print('strings: ')
    print(parametros[1])
    print('tamanhos das strigs: ')
    print(parametros[2])
    print('nstrings: ' + str(nstrings))


if __name__ == "__main__":
    main()
