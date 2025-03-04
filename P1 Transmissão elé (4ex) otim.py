# -------------------------------------------------------------
# João Gabriel Ruiz Gonçalves - MT 3012034
# -------------------------------------------------------------
# Código para cálculo de indutância e reatância em uma linha
# de transmissão simples, trifásica, sem ou com solo, sem cabo para-raio
# e com cabo singelo ou acordoado.
# -------------------------------------------------------------
# Para testar o código acesse: https://computeel.org/LOM3260/teste/
#--------------------------------------------------------------

import math  # Importa a biblioteca matemática para cálculos

# Função para criar uma matriz preenchida com zeros
def criar_matriz(N):
    matriz = []  # Inicializa a matriz como uma lista vazia
    for i in range(N):  # Laço que cria N linhas na matriz
        linha = [0] * N  # Cria uma linha com N zeros
        matriz.append(linha)  # Adiciona a linha à matriz
    return matriz 

# Função para preencher a matriz com valores fornecidos pelo usuário
def preencher_matriz(matriz, mensagem):
    N = len(matriz)  # Obtém o tamanho da matriz
    for i in range(N):  # Laço que percorre as linhas da matriz
        for j in range(i + 1, N):  # Laço que percorre as colunas acima da diagonal principal
            # Solicita ao usuário o valor da distância entre os cabos i+1 e j+1
            matriz[i][j] = float(input(f"{mensagem} entre o cabo {i+1} e o cabo {j+1} (m): "))
            matriz[j][i] = matriz[i][j]  # Reflete o valor na outra metade da matriz por simetria

# Função para exibir a matriz formatada
def exibir_matriz(matriz, titulo):
    print(f"\n{titulo}:")  # Exibe o título da matriz
    for i in range(len(matriz)):  # Laço que percorre as linhas da matriz
        linha = []  # Inicializa uma lista para armazenar os valores da linha
        for j in range(len(matriz[i])):  # Laço que percorre as colunas de cada linha
            linha.append(f"{matriz[i][j]:.3e}")  # Formata o valor da célula como notação científica
        print(linha)  # Exibe a linha formatada

# Função para calcular os valores L_i para cada cabo
def calcular_Li(matriz_L):
    N = len(matriz_L)  # Obtém o tamanho da matriz
    Lx = []  # Lista para armazenar os valores L_i
    for i in range(N):  # Laço que percorre as linhas da matriz
        f_ii = matriz_L[i][i]  # Termo da diagonal principal (indutância própria do cabo)
        soma_mutuos = 0  # Inicializa a soma dos elementos fora da diagonal
        for j in range(N):  # Laço que percorre as colunas da matriz
            if j != i:  # Se a posição não for a diagonal principal
                soma_mutuos += matriz_L[i][j]  # Adiciona o valor da indutância mútua
        L_i = f_ii - 0.5 * soma_mutuos  # Calcula o valor L_i com a fórmula 7.63 do Fuchs
        Lx.append(L_i)  # Adiciona o valor de L_i à lista
    return Lx  # Retorna a lista com os valores L_i

# Função para calcular a reatância a partir de Lx e frequência
def calcular_reatancia(Lx, frequencia):
    w = 2 * math.pi * frequencia  # Calcula a pulsação angular (ω = 2πf)
    reatancia = []  # Lista para armazenar os valores de reatância
    for i in range(len(Lx)):  # Laço que percorre os valores de Lx
        reatancia.append(w * Lx[i])  # Calcula a reatância de cada L_i
    return reatancia  # Retorna a lista com as reatâncias

# Função para calcular a matriz de indutância com ou sem influência do solo
def calcular_matriz_indutancia(N, d, D, dim, hi=None):
    """
    Calcula a matriz de indutância considerando a presença ou ausência do solo.
    - Se hi (altura de flecha) for fornecida, significa que há influência do solo.
    - Caso contrário, não há influência do solo.
    """
    L = criar_matriz(N)  # Cria uma matriz para armazenar os valores de indutância
    for i in range(N):  # Laço que percorre as linhas da matriz
        for j in range(N):  # Laço que percorre as colunas da matriz
            if i == j:  # Diagonal principal
                if hi is not None:  # Se a altura de flecha (hi) for fornecida
                    L[i][j] = 2 * 10**-7 * math.log(2 * hi / dim)  # Fórmula 7.42 do Fuchs para indutância com solo 
                else:  # Caso contrário
                    L[i][j] = 2 * 10**-7 * math.log(1 / dim)  # Fórmula 7.30 do Fuchs para indutância sem solo
            else:  # Fora da diagonal
                if hi is not None:  # Se a altura de flecha (hi) for fornecida
                    L[i][j] = 2 * 10**-7 * math.log(D[i][j] / d[i][j])  # Fórmula 7.43 do Fuchs para indutância com solo
                else:  # Caso contrário
                    L[i][j] = 2 * 10**-7 * math.log(1 / d[i][j])  # Fórmula 7.30 do Fuchs para indutância sem solo
    return L  # Retorna a matriz de indutância calculada

# ---- Escolha da Opção ----
print("Escolha uma das opções:")
print("1 - Rodar o código para cálcular a indutância e reatância para cabo singelo sem solo")
print("2 - Rodar o código para cálcular a indutância e reatância para cabo singelo com solo")
print("3 - Rodar o código para cálcular a indutância e reatância para cabo acordoado sem solo")
print("4 - Rodar o código para cálcular a indutância e reatância para cabo acoroado com solo")

# Entrada da opção do usuário
opcao = int(input("Digite o número da opção desejada: "))

# Cabo Singelo Sem Solo
if opcao == 1:
    # ---- Entrada de Dados ----
    N = int(input("Número de Cabos Condutores: "))  # Número de cabos
    d = criar_matriz(N)  # Cria a matriz de distâncias
    preencher_matriz(d, "Distância")  # Preenche a matriz com os valores das distâncias
    dim = float(input("Diâmetro do cabo condutor (m): "))  # Diâmetro do cabo condutor

    # ---- Cálculo da Matriz de Indutância ----
    L = calcular_matriz_indutancia(N, d, d, dim)  # Calcula a matriz de indutância 
    exibir_matriz(L, "Matriz de Indutância (H/m)")  # Exibe a matriz de indutância

    # ---- Cálculo dos Valores de Indutância L_i ----
    Lx = calcular_Li(L)  # Calcula os valores L_i de indutância
    print("\nValores L_i calculados:")
    for i in range(len(Lx)):  # Itera de 0 até o tamanho de Lx - 1
        L_i = Lx[i]  # Obtém o valor L_i na posição i
        print(f"L_{i+1} = {L_i:.3e} H/m")  # Exibe o valor L_i com notação científica

    # ---- Cálculo da Reatância ----
    f = float(input("\nInforme a frequência do sistema (em Hz): "))  # Frequência do sistema
    X = calcular_reatancia(Lx, f)  # Calcula a reatância
    print("\nValores de Reatância calculados:")
    for i, X_i in enumerate(X):  # Itera sobre a lista X de reatâncias
        print(f"X_{i+1} = {X_i:.3e} Ω/m")  # Exibe os valores de reatância calculados

    # Cálculo da reatância indutiva de sequência positiva
    X_seq_positiva = sum(X) / len(X)  # Média das reatâncias
    print(f"\nReatância Indutiva de Sequência Positiva: X1 = {X_seq_positiva:.3e} Ω/m")

# Cabo Singelo Com Solo
elif opcao == 2:
    # ---- Entrada de Dados ----
    N = int(input("Número de Cabos Condutores: "))  # Número de cabos
    ji = float(input("Insira o valor de flecha: ")) * 0.7  # Altura de flecha
    H = float(input("Medida da altura dos cabos: "))  # Altura dos cabos
    hi = H - ji  # Calcula a altura de flecha

    # Matrizes de distâncias reais e imaginárias
    d = criar_matriz(N)
    preencher_matriz(d, "Valor da distância real")
    D = criar_matriz(N)
    preencher_matriz(D, "Valor da distância imaginária")

    dim = float(input("Diâmetro do cabo condutor (m): "))  # Diâmetro do cabo condutor

    # ---- Cálculo da Matriz de Indutância ----
    L = calcular_matriz_indutancia(N, d, D, dim, hi)  # Calcula a matriz de indutância com solo
    exibir_matriz(L, "Matriz de Indutância (H/m)")  # Exibe a matriz de indutância

    # ---- Cálculo dos Valores de Indutância L_i ----
    Lx = calcular_Li(L)  # Calcula os valores L_i de indutância
    print("\nValores L_i calculados:")
    for i in range(len(Lx)):  # Itera de 0 até o tamanho de Lx - 1
        L_i = Lx[i]  # Obtém o valor L_i na posição i
        print(f"L_{i+1} = {L_i:.3e} H/m")  # Exibe o valor L_i com notação científica

    # ---- Cálculo da Reatância ----
    f = float(input("\nInforme a frequência do sistema (em Hz): "))  # Frequência do sistema
    X = calcular_reatancia(Lx, f)  # Calcula a reatância
    print("\nValores de Reatância calculados:")
    for i, X_i in enumerate(X):  # Itera sobre a lista X de reatâncias
        print(f"X_{i+1} = {X_i:.3e} Ω/m")  # Exibe os valores de reatância calculados

    # Cálculo da reatância indutiva de sequência positiva
    X_seq_positiva = sum(X) / len(X)  # Média das reatâncias
    print(f"\nReatância Indutiva de Sequência Positiva: X1 = {X_seq_positiva:.3e} Ω/m")

# Cabo Acordoado Sem Solo
if opcao == 3:
    # ---- Entrada de Dados ----
    N = int(input("Número de Cabos Condutores: "))  # Número de cabos
    d = criar_matriz(N)  # Cria a matriz de distâncias
    preencher_matriz(d, "Distância")  # Preenche a matriz com os valores das distâncias
    dim = float(input("Diâmetro do cabo condutor (m): ")) * 0.7788  # Diâmetro do cabo acordoado

    # ---- Cálculo da Matriz de Indutância ----
    L = calcular_matriz_indutancia(N, d, d, dim)  # Calcula a matriz de indutância 
    exibir_matriz(L, "Matriz de Indutância (H/m)")  # Exibe a matriz de indutância

    # ---- Cálculo dos Valores de Indutância L_i ----
    Lx = calcular_Li(L)  # Calcula os valores L_i de indutância
    print("\nValores L_i calculados:")
    for i in range(len(Lx)):  # Itera de 0 até o tamanho de Lx - 1
        L_i = Lx[i]  # Obtém o valor L_i na posição i
        print(f"L_{i+1} = {L_i:.3e} H/m")  # Exibe o valor L_i com notação científica

    # ---- Cálculo da Reatância ----
    f = float(input("\nInforme a frequência do sistema (em Hz): "))  # Frequência do sistema
    X = calcular_reatancia(Lx, f)  # Calcula a reatância
    print("\nValores de Reatância calculados:")
    for i, X_i in enumerate(X):  # Itera sobre a lista X de reatâncias
        print(f"X_{i+1} = {X_i:.3e} Ω/m")  # Exibe os valores de reatância calculados

    # Cálculo da reatância indutiva de sequência positiva
    X_seq_positiva = sum(X) / len(X)  # Média das reatâncias
    print(f"\nReatância Indutiva de Sequência Positiva: X1 = {X_seq_positiva:.3e} Ω/m")

# Cabo Acordoado Com Solo
elif opcao == 4:
    # ---- Entrada de Dados ----
    N = int(input("Número de Cabos Condutores: "))  # Número de cabos
    ji = float(input("Insira o valor de flecha: ")) * 0.7  # Altura de flecha
    H = float(input("Medida da altura dos cabos: "))  # Altura dos cabos
    hi = H - ji  # Calcula a altura de flecha

    # Matrizes de distâncias reais e imaginárias
    d = criar_matriz(N)
    preencher_matriz(d, "Valor da distância real")
    D = criar_matriz(N)
    preencher_matriz(D, "Valor da distância imaginária")

    dim = float(input("Diâmetro do cabo condutor (m): ")) * 0.7788  # Diâmetro do cabo condutor

    # ---- Cálculo da Matriz de Indutância ----
    L = calcular_matriz_indutancia(N, d, D, dim, hi)  # Calcula a matriz de indutância com solo
    exibir_matriz(L, "Matriz de Indutância (H/m)")  # Exibe a matriz de indutância

    # ---- Cálculo dos Valores de Indutância L_i ----
    Lx = calcular_Li(L)  # Calcula os valores L_i de indutância
    print("\nValores L_i calculados:")
    for i in range(len(Lx)):  # Itera de 0 até o tamanho de Lx - 1
        L_i = Lx[i]  # Obtém o valor L_i na posição i
        print(f"L_{i+1} = {L_i:.3e} H/m")  # Exibe o valor L_i com notação científica

    # ---- Cálculo da Reatância ----
    f = float(input("\nInforme a frequência do sistema (em Hz): "))  # Frequência do sistema
    X = calcular_reatancia(Lx, f)  # Calcula a reatância
    print("\nValores de Reatância calculados:")
    for i, X_i in enumerate(X):  # Itera sobre a lista X de reatâncias
        print(f"X_{i+1} = {X_i:.3e} Ω/m")  # Exibe os valores de reatância calculados

    # Cálculo da reatância indutiva de sequência positiva
    X_seq_positiva = sum(X) / len(X)  # Média das reatâncias
    print(f"\nReatância Indutiva de Sequência Positiva: X1 = {X_seq_positiva:.3e} Ω/m")

else:
    print("Opção inválida. Tente novamente.")