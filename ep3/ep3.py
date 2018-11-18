# -*- coding: utf-8 -*-

# MAC0465 - Biologia Computacional
# NOME: Tais Pinheiro
# NUSP: 7580421
# Exercício Programa 3 - Reconstrução de uma supersequência comum ao nível t.

import sys

### MAIN
def main ():
    if len(sys.argv) != 1:
        help()      # Executar sem todos os argumentos necessários mostra ajuda
        sys.exit()

    else:
        entrada = raw_input('\nInforme um limiar inteiro t e o conjunto de strings separadas por espaços:\n\n')

        print('\nProcessando...\n')

        parametros = ajuste_parametros(entrada)
        nstrings = len(parametros[1])

        t = parametros[0]
        strings = parametros[1]
        tamanhos = parametros[2]

        matriz = []
        adj = []
        matriz = list(matriz_adjacencias(strings, nstrings, t))
        adj = list(matriz_adjacencias(strings, nstrings, t))

        ciclo = verifica_ciclos(matriz, nstrings)

        #Se o grafo possui ciclos temos uma exceção
        if ciclo == 1:
            print('\n\n Exception!\n\nO grafo possui ciclo. Programa abortado!\n')

        #Caso contrario procuramos um caminho hamiltoniano
        else:
            topologico = []
            topologico = list(topological_sorting(matriz, nstrings))
            print_supersequencia(topologico, strings, adj)


#Ordenação topologica
def topological_sorting(m, n):
    l = [] #lista que ira conter os elementos ordenados
    s = [] #conjunto de todos os nós sem aresta de entrada

    adj = m
    s = list(sem_aresta_entrada(adj,n))

    # enquanto s não esta vazia
    while(len(s) > 0):
        no = s.pop(0) #retiro um no de s
        l.append(no) #insiro em l
        # para cada no m com uma aresta e de n até m  remova a aresta e do grafo
        for i in range(n):
            if adj[no][i] > 0:
                adj[no][i] = 0
                soma = 0
                for k in range(n):
                    soma = soma + adj[k][i]
                if soma == 0:
                    s.append(i)

    return l

def print_supersequencia(l,strings, adj):

    sequencia = strings[l[0]]

    for i in range(len(l)-1):
        limite = adj[l[i]][l[i+1]]
        sequencia = sequencia + strings[l[i+1]][limite:]

    print('\nA supersequencia das variáveis dada é:\n\n')
    print(sequencia)

def sem_aresta_entrada(m,n):

    result = []

    for i in range(n):
        soma = 0
        for j in range(n):
            soma = soma + m[j][i]
        if soma == 0:
            result.append(i)

    return result

# Determina quais vértices estão ligados ao vertice r
def encontra_territorio(adj, n, r):
    #branco = -1
    #cinza = 0
    #preto = 1
    cor = []
    lista = []

    #todos os vertices soa brancos
    for i in range(n):
        cor.append(-1)

    #o vertice r é cinza
    cor[r] = 0

    #insere r na lista
    lista.append(r)

    #enquanto a lista não estiver vazia
    while len(lista) > 0:
        #tiro o primeiro elemento da lista e verifico a quem ele se liga
        u = lista.pop(0)
        for i in range(n):
            if adj[u][i] > 0:
                #se elemento ainda não foi inserido na lista
                if cor[i] == -1:
                    #elemento fica cinza e inserido na lista
                    cor[i] = 0
                    lista.append(i)
        #u fica preto
        cor[u] = 1

    return cor

#Dada uma matri m representando um grafo, verifica se exite um ciclo.
def verifica_ciclos(m,n):
    ciclo = 0
    territorio = []
    for i in range(n):
        territorio = list(encontra_territorio(m,n,i))

        for j in range(n):
            #se está no territorio e existe uma aresta de retorno
            if territorio[j] == 1 and m[j][i] > 0:
                ciclo = 1
                j = n

    return ciclo

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
