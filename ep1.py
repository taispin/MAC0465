# -*- coding: utf-8 -*-

# MAC0465 - Biologia Computacional
# NOME: Tais Pinheiro
# NUSP: 7580421
# Exercício Programa 1 - Alinhador Local Otimo

import sys

### MAIN
def main ():
    if len(sys.argv) != 1:
        help()      # Executar sem todos os argumentos necessários mostra ajuda
        sys.exit()
    elif len(sys.argv) == 1:

        #Recebe as sequencias s e t como strings
        s = raw_input('\nInforme a sequencia s: ')
        t = raw_input('\nInforme a sequencia t: ')
        s = s.upper()
        s = ajuste(s)
        t = t.upper()
        t = ajuste(t)

        #Encontra os limitantes b e d
        limitantes = encontra_limitantes(s,t)
        b = limitantes[0]
        d = limitantes[1]

        #Encontra os limitantes a e c
        #Inverte as sequencias primeiro
        s.reverse()
        t.reverse()
        #remove o ultimo elemento inserido no ajuste anterior
        lixo = s.pop()
        lixo = t.pop()
        #reajusta as listas invertidas
        s = ajuste(s)
        t = ajuste(t)

        limitantes = encontra_limitantes(s,t)
        a = limitantes[0]
        c = limitantes[1]

        #Achamos a,b,c e d iupiiiii

        #Agora reajustamos as sequencias s e t para finalizar o trabalho
        s.reverse()
        t.reverse()
        lixo = s.pop()
        lixo = t.pop()

        #corta os trecho de a a b e c a d
        s = corta_sequencia(s,a,b)
        t = corta_sequencia(t,c,d)

        #ajusta novamente
        #s = ajuste(s)
        #t = ajuste(t)

        print(s)
        print(t)

        print("a: ", a, "b: ", b, "c: ", c, "d: ", d)

        #print(best_score(s,t))
        #print(best_score_reverse(s,t))
        #score = best_score(s,t)

# Informa como o programa deve ser executado
def help():
    print('\n[EXECUÇÃO DO EP1] python ep1.py')
    print('\nSiga as orientações que você vê na tela para informar as Sequencias s e t.')

# Ajusta as sequencias recebidas para o formato do algoritmo
def ajuste(x):
    tam = len(x)
    y =[]
    y.append(0)
    for i in range(tam):
        y.append(x[i])
    return y

# Resjusta as sequencias recebidas para o calculo final
def corta_sequencia(x,ini,fim):
    tam = len(x)
    for i in range(ini-1):
        lixo = x.pop(0)
    for i in range(tam-fim):
        lixo = x.pop()
    return x

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
    global alinhamento-s = [0] * (2*tam) #alinhamento em s
    global alinhamento-t = [0] * (2*tam) #alinhamento em t

def align(s,t,a,b,c,d,start,end,alin-s,alinh-t):

    space = '-'
    g = -2

    #se a sequencia s está vazia
    if len(s) == 0:
        if len(t) != 0:
            for i in range(len(t)):
                alinh-t[i] = "-"

    #se a sequencia t está vazia
    elif len(t) == 0:
        if len(s) != 0:
            for i in range(len(s)):
                alinh-s[i] = "-"

    #ambas as sequencias não são vazias
    elif len(s) != 0 and len(t) != 0:
        i = (a + b)/2
        pref-sim = best_score(s[a:i], t[c:d+1])
        suff-sim = best_score_reverse(s[i+1:b+1], t[c:d+1])

        posmax = c-1
        typemax = space
        vmax = pref-sim[0] + g + suff-sim[0]

        j = 1
        while j <= d-c+1:
            if (pref-sim[j-1] + p_i_j(i,j) + suff-sim[j+1]) > vmax:
                posmax = j
                typemax = 's'
                vmax = (pref-sim[j-1] + p_i_j(i,j) + suff-sim[j+1])

            if (pref-sim[j] + g + suff-sim[j+1]) > vmax:
                posmax = j
                typemax = 'g'
                vamx = pref-sim[j] + g + suff-sim[j+1]

            j = j + 1

        if typemax = 'g':
            align(s,t,a,i-1,c,posmax,start,i,alin-s,alinh-t):
            alin-s[middle] = s[i]
            alin-t[middle] = '-'
            align(s,t,i+1,b,posmax+1,d,middle +1,end,alin-s,alinh-t):

        else:
            align(s,t,a,i-1,c,posmax-1,start,middle,alin-s,alinh-t):
            alin-s[middle] = s[i]
            alin-t[middle] = t[posmax]
            align(s,t,i+1,b,posmax+1,d,middle +1,end,alin-s,alinh-t):

        return[alin-s,alin-t]

def p_i_j(i,j,s,t):
    if s[i] == t[j]:
        p = 1
    else:
        p = -1

    return p

if __name__ == "__main__":
    main()
