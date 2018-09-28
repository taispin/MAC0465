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
        s = ajuste(s)
        t = ajuste(t)

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


def best_score(s,t):

    g = -2
    match = 1
    mismatch = -1

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

    return a[n-1]

def best_score_reverse(s,t):
    g = -2
    match = 1
    mismatch = -1

    lixo = s.pop(0)
    lixo = t.pop(0)
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

    return a[0]

if __name__ == "__main__":
    main()
