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

        #nao estou conseguindo determinar o i para k = 2.
        #no exeplo funciona com #lin = ((cel/colunas)-1)+(gravar[0]*colunas)
        linha_maxima_1 = (linhas/(tamanhos[1]+1)) * (gravar[0]+1)
        linhas_total = linhas

        i = 2
        while i < k:
            linhas_total = linhas_total/(tamanhos[i-1]+1)
            linha_maxima_2 = (linhas_total/(tamanhos[i]+1)) * (gravar[i-1]+1)
            lin = linha_maxima_1 - ((tamanhos[i]+1)-linha_maxima_2)
            linha_maxima_1 = lin

            i = i+1

        print(gravar)

        if k > 2:
            lin = lin - 1
        print(lin)
        print(col)
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

def mostra_matriz(m):
    for i in range(len(m)):
        print(m[i])
        #print('-----------')

#Recebe duas sequencias s e t e retorna b e d indices para limitação
# de alinhamento local otimo
def encontra_limitantes(s,t):

    g = -2
    match = 1
    mismatch = -1
    maximo = 0
    b = 0
    d = 0

    m = len(s) #tamanho da sequencia s
    n = len(t) #tamanho da sequencia t
    a = [] #lista onde calcularemos o score

    for j in range(n):
        a.append(0)
    i = 1
    while i < m:
        old = a[0]
        a[0] = 0 # punicao = 0
        j = 1
        while j < n:
            temp = a[j]
            if s[i] == t[j]:
                p = match
            else:
                p = mismatch
            a[j] = max([a[j] + g, a[j-1] + g, old+p, 0])
            if a[j] >= maximo:
                maximo = a[j]
                b = i
                d = j
            old = temp
            j = j + 1
        i = i + 1

    limitantes = [b,d]
    return limitantes


def best_score(s_orig,t_orig):

    g = -2
    match = 1
    mismatch = -1

    s = s_orig
    t = t_orig

    s.insert(0,0)
    t.insert(0,0)

    m = len(s) #tamanho da sequencia s
    n = len(t) #tamanho da sequencia t
    a = [] #lista onde calcularemos o score

    for j in range(n):
        a.append(j * g)
    i = 1
    while i < m:
        old = a[0]
        a[0] = i * g
        j = 1
        while j < n:
            temp = a[j]
            if s[i] == t[j]:
                p = match
            else:
                p = mismatch
            a[j] = max([a[j] + g, a[j-1] + g, old+p])
            old = temp
            j = j + 1
        i = i + 1

    return a

def best_score_reverse(s_orig,t_orig):
    g = -2
    match = 1
    mismatch = -1

    s = s_orig
    t = t_orig

    s.append(0)
    t.append(0)

    m = len(s) #tamanho da sequencia s
    n = len(t) #tamanho da sequencia t
    a = [] #lista onde calcularemos o score

    for j in range(n):
        a.append((n-1-j) * g)
    k = 1
    i = m-2
    while i >= 0:
        old = a[n-1]
        a[n-1] = k * g
        k = k + 1
        j = n-2
        while j >= 0:
            temp = a[j]
            if s[i] == t[j]:
                p = match
            else:
                p = mismatch
            a[j] = max([a[j] + g, a[j+1] + g, old+p])
            old = temp
            j = j - 1
        i = i - 1

    return a


def alinhamento(s,t,a,b,c,d):

    tam = max([len(s),len(t)])
    #garantimos que o alainhamento máximo vai ter no máximo 2x a maior sequencia
    alinhamento_s = [0] * (2*tam) #alinhamento em s
    alinhamento_t = [0] * (2*tam) #alinhamento em t

    res = align(s,t,a,b,c,d,alinhamento_s,alinhamento_t)

    return res

def align(s,t,a,b,c,d,alin_s,alin_t):

    space = '-'
    g = -2

    #se a sequencia s está vazia
    if a > b:
        if c <= d:
            for i in range(d - c + 1):
                alin_t[c+i] = s[c+i] #acertar em que indices colocar isso
                alin_s[c+i] = "-"

    #se a sequencia t está vazia
    elif c > d:
        if a <= b:
            for i in range(b - a + 1):
                alin_s[a+i] = s[a+i]
                alin_t[a+i] = "-" #acertar onde colocar esses indices

    #ambas as sequencias não são vazias
    elif a <= b and c <= d:
        i = (a + b)/2

        pref_sim = best_score(s[a:i],t[c:d+1])
        suff_sim = best_score_reverse(s[i+1:b+1],t[c:d+1])
        posmax = c-1
        typemax = 's'

        #coloco um gap com s[i] e alinho t[c...d] com o que está à direita
        vmax = pref_sim[0] + g + suff_sim[0]

        j = 1
        #procuro t[j] que quero alinhar com s[i]
        while j <= d-c+1:
            if (pref_sim[j-1] + p_i_j(i,j,s,t) + suff_sim[j]) > vmax:
                posmax = j
                typemax = 's'
                vmax = (pref_sim[j-1] + p_i_j(i,j,s,t) + suff_sim[j])

            if (pref_sim[j] + g + suff_sim[j]) > vmax:
                posmax = j
                typemax = 'g'
                vamx = pref_sim[j] + g + suff_sim[j]

            j = j + 1

        #casei s[i] com t[j]
        if typemax == 's':
            align(s,t,a,i-1,c,posmax-1,alin_s,alin_t)
            alin_s[i] = s[i]
            alin_t[i] = t[posmax]
            align(s,t,i+1,b,posmax+1,d,alin_s,alin_t)
        #casei s[i] com um gap
        else:
            align(s,t,a,i-1,c,posmax,alin_s,alin_t)
            alin_s[i] = s[i]
            alin_t[i] = '-'
            align(s,t,i+1,b,posmax+1,d,alin_s,alin_t)

        return[alin_s,alin_t]

def p_i_j(i,j,s,t):
    if s[i] == t[j]:
        p = 1
    else:
        p = -1

    return p

if __name__ == "__main__":
    main()
