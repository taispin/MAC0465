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

        s.insert(0,0)
        t.insert(0,0)

        print("\nOs valores de a, b, c e d são:\n")
        print('a: ', a)
        print('b: ', b)
        print('c: ', c)
        print('d: ', d)

        print("\nAlinhamento:\n")
        res = alinhamento(s,t,a,b,c,d)
        print(res[0])
        print(res[1])

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
