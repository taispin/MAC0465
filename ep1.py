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

        print("a: ", a, "b: ", b, "c: ", c, "d: ", d)


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

if __name__ == "__main__":
    main()
