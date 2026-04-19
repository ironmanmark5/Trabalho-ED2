import math, os, csv, re
import matplotlib.pyplot as plt
from random_word import RandomWords

def le_arquivo_quincas():
    lista_palavras = []
    padrao = re.compile(r'[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]+')
    with open("quincasborba-utf8-limpo.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavras = padrao.findall(linha)
            for palavra in palavras:
                palavra = palavra.lower()
                if palavra not in lista_palavras:
                    lista_palavras.append(palavra)
                    
    return lista_palavras

def le_arquivo_tale():
    lista_palavras = []
    padrao = re.compile(r'[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]+')
    with open("tale.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavras = padrao.findall(linha)
            for palavra in palavras:
                palavra = palavra.lower()
                if palavra not in lista_palavras:
                    lista_palavras.append(palavra)
                    
    return lista_palavras

def gerar_lista_palavras_falhas():
    lista_palavras_falhas = []
    r = RandomWords()

    lista_palavras_quincas = le_arquivo_quincas()
    lista_palavras_tale = le_arquivo_tale()
    palavras_existentes = lista_palavras_quincas + lista_palavras_tale

    while len(lista_palavras_falhas) < 1000:
        palavra_falha = r.get_random_word()

        if palavra_falha is None:
            continue

        if (palavra_falha not in palavras_existentes and palavra_falha not in lista_palavras_falhas):
            lista_palavras_falhas.append(palavra_falha)
    
    return lista_palavras_falhas


def hashSomaAscii(palavra: str, tamanho_tabela: int):
    soma_ascii = 0

    for letra in palavra:
        soma_ascii += ord(letra)
    
    return (soma_ascii) % tamanho_tabela

def hashSomaPonderada(palavra: str, tamanho_tabela: int):
    soma_ascii = 0

    for i, letra in enumerate(palavra):
        soma_ascii += (i + 1) * ord(letra)

    return (soma_ascii) % tamanho_tabela

def hashMeio(palavra: str, tamanho_tabela: int):
    indice_meio = len(palavra) // 2 # arredonda para numero inteiro
    letra = palavra[indice_meio]

    cod_acsii = ord(letra)

    return cod_acsii % tamanho_tabela

def hashQualquer(palavra: str, tamanho_tabela: int):
    letra_inicial = palavra[0]
    letra_final = palavra[len(palavra) - 1]
    
    primeiro_n_primo = 23
    segundo_n_primo = 103

    cod_ascii = (ord(letra_inicial) * primeiro_n_primo) + (ord(letra_final) * segundo_n_primo)

    return cod_ascii % tamanho_tabela

def definirParametros():
    lista_arquivo = []
    arquivo_texto_desejado = int(input("Arquivos de Texto: \n1 - Quincas Borba\n2 - Tale\nDigite o arquivo de texto que você deseja: "))

    if(arquivo_texto_desejado == 1):
        lista_arquivo = le_arquivo_quincas()

    elif(arquivo_texto_desejado == 2):
        lista_arquivo = le_arquivo_tale()
    
    tamanho_tabela = int(input("Digite o tamanho da tabela desejada: "))
    
    return lista_arquivo, tamanho_tabela, arquivo_texto_desejado

funcoes = [hashSomaAscii, hashSomaPonderada, hashMeio, hashQualquer]

def montarTabelasHash(lista_palavras, tamanho):
    tabelas_hash = {}

    # Inicializa uma tabela hash para cada função
    for funcao in funcoes:
        # Cria uma tabela com 'tamanho' buckets (listas vazias)
        tabela = [[] for _ in range(tamanho)]
        tabelas_hash[funcao.__name__] = tabela # cada indice

    # Insere as palavras nas respectivas tabelas
    for funcao in funcoes:
        tabela = tabelas_hash[funcao.__name__]
        for palavra in lista_palavras:
            bucket = funcao(palavra, tamanho)
            tabela[bucket].append(palavra)

    return tabelas_hash

def buscarPalavraHash(palavra, tabela_hash):
    print(f"\n{"-" * 8} Buscando na Tabela Hash. {"-" * 8}\n")
    palavra = palavra.lower()
    cont = 0

    bucket = hashSomaAscii(palavra, len(tabela_hash))
    print(f"Procurando palavra no bucket: {bucket}")

    #if palavra in tabela_hash[bucket]:
    #    print(f"A palavra {palavra} encontrata!")
    #else: print(f"A palavra {palavra} não foi encontrada")

    for pal in tabela_hash[bucket]:
        cont += 1
        if(pal == palavra): 
            print(f"A palavra {palavra} foi encontrada!\nNúmero de comparações: {cont}\n")
            return
    print(f"A palavra {palavra} não foi encontrada.\nNúmero de comparações: {cont}\n")

def buscaPalavraLinear(palavra, lista_palavras):
    print(f"\n{"-" * 8} Buscando Linearmente. {"-" * 8}\n")
    cont = 0
    
    for pal in lista_palavras:
        cont+=1
        if(pal == palavra):
            print(f"A palavra {palavra} foi encontrada!\nNúmero de comparações: {cont}\n")
            return
    print(f"A palavra {palavra} não foi encontrada.\nNúmero de comparações: {cont}\n")

def calculoVarDesvio(tabela_hash, tamanho_tabela):
    """""
    for i in tabela_hash[i]:
        mediaVar += tabela_hash[i] + tabela_hash[i+1]
    mediaVar = (mediaVar)/(tamanho_tabela)

    for i in tabelas_hash[i]:
        somatorio += pow(tabela_hash[i] - mediaVar, 2)

    variancia = (somatorio)/(tamanho_tabela)    
    desvioPadrao = math.sqrt(variancia)    
    """""

    # 1. Contar quantos elementos existem em cada bucket (colisões)
    # Assumindo que tabela_hash é uma lista de listas
    contagens = [len(bucket) for bucket in tabela_hash]
    
    # 2. Calcular a Média (μ)
    media = sum(contagens) / tamanho_tabela
    
    # 3. Calcular o Somatório da Variância: Σ(x - μ)²
    somatorio = sum(pow(x - media, 2) for x in contagens)
    
    # 4. Variância e Desvio Padrão
    variancia = somatorio / tamanho_tabela
    desvioPadrao = math.sqrt(variancia)
    
    return variancia, desvioPadrao

def maxBucket(tabela_hash):
    #buckets = [len(bucket) for bucket in tabela_hash]
    #maior_bucket = max(buckets)
    
    #return maior_bucket 
    maior_bucket = max(tabela_hash, key=len)
    return maior_bucket, len(maior_bucket)


def simularBuscas(tabela_hash, lista_palavras_sucesso, lista_palavras_falha, funcao_hash, M):
    # --- SUCESSO ---
    total_comp_success = 0
    for palavra in lista_palavras_sucesso:
        bucket = funcao_hash(palavra, M)
        for p in tabela_hash[bucket]:
            total_comp_success += 1
            if p == palavra:
                break # Encontrou
                
    # --- FALHA ---
    total_comp_fail = 0
    for palavra in lista_palavras_falha:
        bucket = funcao_hash(palavra, M)
        for p in tabela_hash[bucket]:
            total_comp_fail += 1
            if p == palavra: # Na teoria nunca vai entrar aqui, pois são palavras ausentes
                break
                
    avg_comp_success = total_comp_success / len(lista_palavras_sucesso) if lista_palavras_sucesso else 0
    avg_comp_fail = total_comp_fail / len(lista_palavras_falha) if lista_palavras_falha else 0
    
    return total_comp_success, avg_comp_success, total_comp_fail, avg_comp_fail

def gerarRelatorioCompleto():
    print("\nIniciando bateria de testes automatizada...")
    
    # Define os tamanhos de tabela que você quer testar
    tamanhos_tabela = [97, 100, 997]
    
    # Carrega os textos usando as funções que você já criou
    textos = [
        ("Quincas", le_arquivo_quincas()),
        ("Tale", le_arquivo_tale())
    ]
    
    # Cabeçalho do arquivo CSV
    cabecalho = [
        "texto", "M", "hash_name", "n", "alpha", 
        "max_bucket", "avg_bucket", "total_comp_success", 
        "avg_comp_success", "total_comp_fail", "avg_comp_fail"
    ]
    
    nome_arquivo = "relatorio_final_hash.csv"

    lista_palavras_falhas = gerar_lista_palavras_falhas()
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(cabecalho) # Escreve o cabeçalho uma única vez
        
        # Loop 1: Passa por cada texto (Quincas e Tale)
        for nome_texto, lista_palavras in textos:
            n = len(lista_palavras)
            
            # Loop 2: Passa por cada tamanho de tabela (M)
            for M in tamanhos_tabela:
                alpha = n / M
                
                # Gera as tabelas para todas as funções de uma vez nesse M
                tabelas = montarTabelasHash(lista_palavras, M)
                
                # Loop 3: Extrai os dados de cada função hash
                for funcao in funcoes:
                    nome_hash = funcao.__name__
                    tabela = tabelas[nome_hash]
                    
                    # Usa a sua função maxBucket corrigida
                    _, tam_maior = maxBucket(tabela)
                    
                    # Calcula o sucesso/falha
                    tc_success, ac_success, tc_fail, ac_fail = simularBuscas(tabela, lista_palavras, lista_palavras_falhas, funcao, M)
                    
                    # Monta a linha com os dados formatados
                    linha = [
                        nome_texto, M, nome_hash, n, round(alpha, 4),
                        tam_maior, round(alpha, 4), # avg_bucket teórico é o próprio alpha
                        int(tc_success), round(ac_success, 4),
                        int(tc_fail), round(ac_fail, 4)
                    ]
                    
                    # Grava a linha no CSV
                    escritor.writerow(linha)
                    print(f"Processado: {nome_texto} | M={M} | Função: {nome_hash}")
                    
    print(f"\n[+] Relatório gerado com sucesso! Arquivo salvo como: {nome_arquivo}")

def montarGrafico(resultados_cenario, nome_texto, tamanho_m):
    """
    resultados_cenario: dicionário {'Soma': tabela1, 'Ponderada': tabela2, ...}
    nome_texto: 'Quincas' ou 'Tale'
    tamanho_m: 97, 100 ou 997
    """

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(f'Análise de Funções Hash - {nome_texto} (M={tamanho_m})', fontsize=18)
    
    # transforma a matriz 2x2 em uma lista simples para iterar
    eixos = axes.flatten()
    
    for i, (nome_hash, tabela) in enumerate(resultados_cenario.items()):
        # calcula a ocupação de cada bucket
        contagens = [len(bucket) for bucket in tabela]
        indices = list(range(len(tabela)))
        
        eixos[i].bar(indices, contagens, color='darkblue', alpha=0.7)
        eixos[i].set_title(f"Função: {nome_hash}", fontsize=14)
        eixos[i].set_xlabel("Índice do Bucket")
        eixos[i].set_ylabel("Qtd de Palavras")
        
        # adiciona uma linha com a média (fator de carga alpha)
        alpha = sum(contagens) / len(tabela)
        eixos[i].axhline(alpha, color='red', linestyle='--', label=f'Média (α={alpha:.2f})')
        eixos[i].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # ajusta espaço para o título principal

    plt.tight_layout()

    if not os.path.exists('resultados'): os.makedirs('resultados')        
    nome_arquivo = f"comp_{nome_texto.lower()}_{tamanho_m}.png"
    plt.savefig(os.path.join('resultados', nome_arquivo), dpi=300)
    
    plt.show()

if __name__ == "__main__":

    while True:
        opcao = int(input("Qual operação você deseja executar?\n1 - Buscar palavra\n2 - Imprimir gráfico\n3 - Imprimir métricas da função\n4 - Gerar planílha\n5 - Encerrar programa\nDigite a opção desejada: "))

        if(opcao == 1):
            tabelas_hash = {}
            lista_palavras, tamanho_tabela, _ = definirParametros()
            tabelas_hash = montarTabelasHash(lista_palavras, tamanho_tabela)

            palavra = str(input("Digite a palavra que deseja buscar: "))
            
            buscarPalavraHash(palavra, tabelas_hash["hashSomaAscii"])
            print("\n(A fins de comparação.)\n")
            buscaPalavraLinear(palavra, lista_palavras)

        elif(opcao == 2):
            tabelas_hash = {}
            lista_palavras, tamanho_tabela, cod_texto = definirParametros()

            if(cod_texto == 1): nome_texto = "Quincas"
            elif(cod_texto == 2): nome_texto = "Tale"
            
            tabelas_hash = montarTabelasHash(lista_palavras, tamanho_tabela)

            montarGrafico(tabelas_hash, nome_texto, tamanho_tabela)
        
        elif(opcao == 3):
            tabelas_hash = {}
            lista_palavras, tamanho_tabela, _ = definirParametros()
            fator_carga = len(lista_palavras) / tamanho_tabela
            tabelas_hash = montarTabelasHash(lista_palavras, tamanho_tabela)

            for funcao in funcoes:
                tabela_hash = tabelas_hash[funcao.__name__]

                maior_bucket, tamanho_maior_bucket = maxBucket(tabela_hash)
                indice_maior_bucket = funcao(maior_bucket[0], tamanho_tabela)
                variancia, desvio_padrao = calculoVarDesvio(tabela_hash, tamanho_tabela)

                print(f"Métricas da Função {funcao.__name__}:")
                print(f"\nFator de Carga: {fator_carga}")
                print(f"\nMaior Bucket: {indice_maior_bucket}  -   Tamanho do Maior Bucket: {tamanho_maior_bucket}")
                print(f"\nVariância: {variancia}")
                print(f"\nDesvio Padrão: {desvio_padrao}")
            
        elif(opcao == 4):
            gerarRelatorioCompleto()

        elif(opcao == 5):
            break  
        else: opcao = int(input("Valor inválido. Digite novamente a opção desejada: "))
    