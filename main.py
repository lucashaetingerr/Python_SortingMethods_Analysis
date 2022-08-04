import numpy as np 
import random #valores aleatórios
import timeit #responsável pela contagem de tempo de cada método
import matplotlib.pyplot as plt #para gerar os gráficos

lista_metodos=["BUBBLE", "INSERTION", "SELECTION", "QUICK", "MERGE", "SHELL"] #para ter o tempo de execução alinhado ao seu
lista_execTime=[]                                                             #respectivo método

class AlgoritmoInfo:
    def __init__(self, nome: str):
        self.nome = nome
        self.comparacoes = 0
        self.trocas = 0
        self.timer = None
        self.tempoDecorrido = 0

    def contarComparacao(self):
        self.comparacoes += 1

    def contarTroca(self):
        self.trocas += 1

    def inicio(self):
        self.timer = timeit.default_timer()
        self.tempoDecorrido = 0

    def continuar(self):
        self.timer = timeit.default_timer()

    def fim(self):
        if self.timer is None:
            return

        self.tempoDecorrido += timeit.default_timer() - self.timer

    def print_info(self):
        print(self.nome + ':')
        print(' - Comparações:', str(self.comparacoes).replace('.', ','))
        print(' - Trocas:', str(self.trocas).replace('.', ','))
        print(' - Tempo: {:.10f} segs'.format(self.tempoDecorrido).replace('.', ','))
        print('----------------------------------')

def bubble_sort(vetor):
    algo_info = AlgoritmoInfo('Bubble sort')
    # Inicio da captura do tempo decorrido
    algo_info.inicio()

    troca = True

    # Enquanto houver troca
    while troca:
        troca = False
        # Percorer o vetor até o penúltimo elemento
        for i in range(len(vetor) - 1):
            algo_info.contarComparacao()
            # Verificar se o elemento da esquerda é maior do que o da direita
            if vetor[i] > vetor[i + 1]:
                # Fazer a troca
                swap(vetor, i, i + 1)
                algo_info.contarTroca()
                troca = True

    # Fim da captura do tempo decorrido
    algo_info.fim()
    tempoExec_bubble=algo_info.tempoDecorrido #salva o tempo de execução do método de ordenação bubble
    lista_execTime.append(tempoExec_bubble)   #salva na lista global esse tempo de execução
    return algo_info


def particao(vetor, inicio, final, algo_info: AlgoritmoInfo):
    pivo = vetor[final]  # O pivô de comparação é o último elemento.
    i = inicio - 1

    for j in range(inicio, final):
        algo_info.contarComparacao()
        if vetor[j] <= pivo:
            i += 1
            swap(vetor, i, j)
            algo_info.contarTroca()

    swap(vetor, i + 1, final)
    algo_info.contarTroca()

    return i + 1


def quick_sort(vetor, inicio=None, final=None, algo_info: AlgoritmoInfo = None):
    # Verificar se é a primeira chamada recursiva
    first = algo_info is None
    if first:
        algo_info = AlgoritmoInfo('Quick sort')
        algo_info.inicio()  # Inicio da captura do tempo decorrido

    inicio = 0 if inicio is None else inicio
    final = len(vetor) - 1 if final is None else final

    if inicio < final:
        posicao = particao(vetor, inicio, final, algo_info)
        # Ordena a parte esquerda do vetor.
        quick_sort(vetor, inicio, posicao - 1, algo_info)
        # Ordena a parte direita do vetor.
        quick_sort(vetor, posicao + 1, final, algo_info)

    # Parar a contagem do tempo somente quando chegar ao fim da primeira chamada do método
    if first:
        algo_info.fim()
        tempoExec_quick=algo_info.tempoDecorrido #salva o tempo de execução do método de ordenação quick
        lista_execTime.append(tempoExec_quick)   #salva na lista global esse tempo de execução

    return algo_info


def insertion_sort(vetor):
    algo_info = AlgoritmoInfo('Insertion sort')
    # Inicio da captura do tempo decorrido
    algo_info.inicio()

    # Percorer o vetor começando da posicao 1
    for i in range(1, len(vetor)):
        # Pegar o valor do elemento
        v = vetor[i]
        k = -1
        # Percorer o vetor da direita para a esquerda a partir da posição atual
        for j in range(i - 1, -1, -1):
            algo_info.contarComparacao()
            # Parar se o valor na posicao for maior do que o valor do elemento
            if v >= vetor[j]:
                break
            else:  # Caso o valor seja menor
                # Mover o elemento atual para a direita
                algo_info.contarTroca()
                vetor[i] = vetor[j]
                i -= 1
                k = j
        # Colocar o valor na posição k
        if k != -1:
            vetor[k] = v

    # Fim da captura do tempo decorrido
    algo_info.fim()
    tempoExec_insertion=algo_info.tempoDecorrido #salva o tempo de execução do método de ordenação insertion
    lista_execTime.append(tempoExec_insertion)   #salva na lista global esse tempo de execução

    return algo_info


def selection_sort(vetor):
    algo_info = AlgoritmoInfo('Selection sort')
    # Inicio da captura do tempo decorrido
    algo_info.inicio()

    # Percorer o vetor
    for i in range(len(vetor) - 1):
        # Determinar o primeiro valor como o menor
        menor = vetor[i]
        posicao_menor = i
        # Buscar por um valor menor no vetor
        for j in range(i, len(vetor)):
            algo_info.contarComparacao()
            if vetor[j] < menor:
                menor = vetor[j]
                posicao_menor = j
        # Realizar a troca do valor menor com o valor atual
        if posicao_menor != i:
            algo_info.contarTroca()
            swap(vetor, i, posicao_menor)

    # Fim da captura do tempo decorrido
    algo_info.fim()
    tempoExec_selection=algo_info.tempoDecorrido #salva o tempo de execução do método de ordenação selection
    lista_execTime.append(tempoExec_selection)   #salva na lista global esse tempo de execução

    return algo_info


def merge(vetor, vetor_ord, inicio, meio, fim, algo_info: AlgoritmoInfo):
    i = inicio
    j = meio

    # Coloca os valores no vetor_ord do maior para o menor
    for k in range(inicio, fim + 1):
        # Caso a parte da esquerda tiver vazia, copiar os elementos da parte da direita
        if i >= meio:
            if vetor_ord[k] != vetor[j]:
                algo_info.contarTroca()
                vetor_ord[k] = vetor[j]
            j += 1
        # Caso a parte da direita tiver vazia, copiar os elementos da parte da esquerda
        elif j > fim:
            if vetor_ord[k] != vetor[i]:
                algo_info.contarTroca()
                vetor_ord[k] = vetor[i]
            i += 1
        else:
            # Determinar o menor valor para ser copiado para o vetor
            algo_info.contarComparacao()
            if vetor[i] < vetor[j]:
                if vetor_ord[k] != vetor[i]:
                    algo_info.contarTroca()
                    vetor_ord[k] = vetor[i]
                i += 1
            else:
                if vetor_ord[k] != vetor[j]:
                    algo_info.contarTroca()
                    vetor_ord[k] = vetor[j]
                j += 1

    # Copiar os valores do vetor_ord para vetor
    for k in range(inicio, fim + 1):
        vetor[k] = vetor_ord[k]


def merge_sort(vetor, vetor_ord=None, inicio=None, fim=None, algo_info: AlgoritmoInfo = None):
    # Verificar se é a primeira chamada recursiva
    first = algo_info is None
    if first:
        algo_info = AlgoritmoInfo('Merge sort')
        # Inicio da captura do tempo decorrido
        algo_info.inicio()

    # Criar uma cópia do vetor de não tiver sido pasado como argumento
    if vetor_ord is None:
        vetor_ord = vetor.copy()

    # Determinar o inicio e fim
    inicio = 0 if inicio is None else inicio
    fim = len(vetor) - 1 if fim is None else fim

    if inicio < fim:
        meio = int((inicio + fim) / 2)
        # Divide a parte da esquerda
        merge_sort(vetor, vetor_ord, inicio, meio, algo_info)
        # Divide a parte da direita
        merge_sort(vetor, vetor_ord, meio + 1, fim, algo_info)
        # Junta as duas partes comparando quais são os menores
        merge(vetor, vetor_ord, inicio, meio + 1, fim, algo_info)

    # Parar a contagem do tempo somente quando chegar ao fim da primeira chamada do método
    if first:
        algo_info.fim()
        tempoExec_merge=algo_info.tempoDecorrido #salva o tempo de execução do método de ordenação merge
        lista_execTime.append(tempoExec_merge)   #salva na lista global esse tempo de execução

    return algo_info


def shell_sort(vetor):
    algo_info = AlgoritmoInfo('Shell sort')
    # Inicio da captura do tempo decorrido
    algo_info.inicio()

    # Armazenar o tamanho do vetor
    tamanho = len(vetor)
    # Largura do gap de comparações
    h = tamanho // 2

    # Enquanto o gap for maior que 0
    while h > 0:
        i = 0
        # Percorer os grupos
        while i < h:
            j = i + h  # j é o indice do elemento da direita
            k = i      # k é o indice do elemento da esquerda

            # Enquanto tiver elementos dentro do grupo
            while j < tamanho:
                # Criar copias de k e j
                _k = k
                _j = j

                # Realizar as comparacoes dentro do grupo, utilizando o algoritmo do insertion sort
                while _k >= 0:
                    algo_info.contarComparacao()  # Contabilizar a comparação
                    if vetor[_k] > vetor[_j]:
                        algo_info.contarTroca()  # Contabilizar a troca
                        swap(vetor, _k, _j)
                        _j = _k
                        _k -= h
                    else:  # Para caso o elemento da direita for maior ou igual ao da esquerda
                        break

                # Ir para o proximo elemento
                k = j
                j += h

            # Ir para o próximo grupo
            i += 1

        # Diminuir o gap pela metade
        h //= 2

    # Fim da captura do tempo decorrido
    algo_info.fim()
    tempoExec_shell=algo_info.tempoDecorrido #salva o tempo de execução do método de ordenação merge
    lista_execTime.append(tempoExec_shell)   #salva na lista global esse tempo de execução

    return algo_info


# Método para trocar dois indices em um vetor
def swap(vetor, i, j):
    vetor[i], vetor[j] = vetor[j], vetor[i]


# Método para gerar um vetor de numeros aleatorios
def vetor_aleatorio(tamanho):
    vetor = np.empty(tamanho, dtype=int)
    for i in range(tamanho):
        vetor[i] = random.randint(0, 10000)
    return vetor

#Função principal do código. Mostra os métodos com seus respectivos tempos de execução, trocas e comparações executadas.
#Também monta e exibe o gráfico com os dados gerados.
def main():
    # 1000, 10000, 50000, 100000

    #pede ao usuário a quantidade de elementos aleatorios que deseja gerar para serem ordenados
    tamanho_vetor=int(input("Insira um valor de elementos a ser ordenado: "))
    #ex: tamanho_vetor = 5000  (elementos)

    vetor_teste = vetor_aleatorio(tamanho_vetor)

    print('Número de elementos a serem ordenados: {}'.format(tamanho_vetor))
    print('Iniciando...\n')

    info = bubble_sort(vetor_teste.copy())
    info.print_info()

    info = insertion_sort(vetor_teste.copy())
    info.print_info()

    info = selection_sort(vetor_teste.copy())
    info.print_info()

    info = quick_sort(vetor_teste.copy())
    info.print_info()

    info = merge_sort(vetor_teste.copy())
    info.print_info()

    info = shell_sort(vetor_teste.copy())
    info.print_info()

    #para conferir com os dados do gráfico
    print("\nLista dos tempo de execução: ")
    print(lista_metodos)
    print(lista_execTime)


    #método de montagem do gráfico
    plt.plot(lista_metodos, lista_execTime)
    #exibe o gráfico
    plt.show()

#execução do código pela função main
main()
