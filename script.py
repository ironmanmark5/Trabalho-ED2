import math, random, os
import matplotlib.pyplot as plt

def le_arquivo_quincas():
    lista_palavras = []
    with open("quincasborba-utf8-limpo.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavras = linha.split() # funcao split é para separar palavra por palavra
            for palavra in palavras:
                palavra = palavra.lower()
                if palavra not in lista_palavras:
                    lista_palavras.append(palavra)
                    
    return lista_palavras

def le_arquivo_tale():
    lista_palavras = []
    with open("tale.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavras = linha.split() # funcao split é para separar palavra por palavra
            for palavra in palavras:
                palavra = palavra.lower()
                if palavra not in lista_palavras:
                    lista_palavras.append(palavra)
                    
    return lista_palavras

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
            bucket = funcao(palavra, tamanho) % tamanho
            tabela[bucket].append(palavra)

    return tabelas_hash

def buscarPalavra(palavra, tamanho, tabela_hash):
    palavra = palavra.lower()

    bucket = hashSomaAscii(palavra, tamanho)
    print(f"Procurando palavra no bucket: {bucket}")

    if palavra in tabela_hash[bucket]:
        print(f"A palavra {palavra} encontrata!")
    else: print(f"A palavra {palavra} não foi encontrada")

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

    ''' codigo = int(input("Escolha o tamanho da tabela:\n1 - 97\n2 - 100\n3 - 997\n"))
    tamanho = 1

    while True:
        if(codigo == 1): 
            tamanho = 97 
            break

        elif(codigo == 2): 
            tamanho = 100 
            break

        elif(codigo == 3): 
            tamanho = 997
            break

        else: 
            código = int(input("Código inválido. Digite o código novamente: "))

    lista_quincas = le_arquivo_quincas()
    # tamanho_quincas = math.floor((len(lista_quincas)) / 0.7) # a = n/M , 0.7 = 11808 / M => 16868 (arrendado para baixo)
    tabela_hash_quincas = {}
    for i in range(tamanho):
        tabela_hash_quincas[i] = []
    
    lista_tale = le_arquivo_tale()
    # tamanho_tale = math.floor((len(lista_tale)) / 0.7) # a = 0.7 floorMod(x, y)
    tabela_hash_tale = {}
    for i in range(tamanho):
        tabela_hash_tale[i] = []

    # print(len(lista)) # 19695 palavras em tale.txt e 11808 em quincasborba-utf8-limpo.txt
    # virou 10828 palavras pro quincas depois de adicionar a parte de normalização para minúsculas 

    # ------------------- Hash Soma dos códigos ascii -------------------
    print("\n" + (10 * "-") + " Hash Soma dos códigos ascii " + (10 * "-") + "\n")
    
    for palavra in lista_quincas:
        bucket = hashSomaAscii(palavra, tamanho)
        tabela_hash_quincas[bucket].append(palavra)
   
    print("\nHistograma da tabela hash do quincas: \n")

    for categoria in tabela_hash_quincas:
        tamanho_categoria = len(tabela_hash_quincas[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')
    
    for palavra in lista_tale:
        bucket = hashSomaAscii(palavra, tamanho)
        tabela_hash_tale[bucket].append(palavra)
    
    print("\nHistograma da tabela hash do tale: \n")
    
    for categoria in tabela_hash_tale:
        tamanho_categoria = len(tabela_hash_tale[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')

    for bucket in tabela_hash_quincas.values():
        bucket.clear() # esvaziando tabela
    
    for bucket in tabela_hash_tale.values():
        bucket.clear() # esvaziando tabela

    # ------------------- Hash Soma Ponderada -------------------
    print("\n" + (10 * "-") + " Hash Soma Ponderada " + (10 * "-") + "\n")

    for palavra in lista_quincas:
        bucket = hashSomaPonderada(palavra, tamanho)
        tabela_hash_quincas[bucket].append(palavra)
   
    print("\nHistograma da tabela hash do quincas: \n")

    for categoria in tabela_hash_quincas:
        tamanho_categoria = len(tabela_hash_quincas[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')
    
    for palavra in lista_tale:
        bucket = hashSomaPonderada(palavra, tamanho)
        tabela_hash_tale[bucket].append(palavra)
    
    print("\nHistograma da tabela hash do tale: \n")
    
    for categoria in tabela_hash_tale:
        tamanho_categoria = len(tabela_hash_tale[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')

    for bucket in tabela_hash_quincas.values():
        bucket.clear() # esvaziando tabela
    
    for bucket in tabela_hash_tale.values():
        bucket.clear() # esvaziando tabela
    
    # ------------------- Hash Letra do Meio -------------------
    print("\n" + (10 * "-") + " Hash Letra do Meio " + (10 * "-") + "\n")

    for palavra in lista_quincas:
        bucket = hashMeio(palavra, tamanho)
        tabela_hash_quincas[bucket].append(palavra)
   
    print("\nHistograma da tabela hash do quincas: \n")

    for categoria in tabela_hash_quincas:
        tamanho_categoria = len(tabela_hash_quincas[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')
    
    for palavra in lista_tale:
        bucket = hashMeio(palavra, tamanho)
        tabela_hash_tale[bucket].append(palavra)
    
    print("\nHistograma da tabela hash do tale: \n")
    
    for categoria in tabela_hash_tale:
        tamanho_categoria = len(tabela_hash_tale[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')

    for bucket in tabela_hash_quincas.values():
        bucket.clear() # esvaziando tabela
    
    for bucket in tabela_hash_tale.values():
        bucket.clear() # esvaziando tabela


    # ------------------- Hash Qualquer -------------------
    print("\n" + (10 * "-") + " Hash Qualquer " + (10 * "-") + "\n")

    for palavra in lista_quincas:
        bucket = hashQualquer(palavra, tamanho)
        tabela_hash_quincas[bucket].append(palavra)
   
    print("\nHistograma da tabela hash do quincas: \n")

    for categoria in tabela_hash_quincas:
        tamanho_categoria = len(tabela_hash_quincas[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')
    
    for palavra in lista_tale:
        bucket = hashQualquer(palavra, tamanho)
        tabela_hash_tale[bucket].append(palavra)
    
    print("\nHistograma da tabela hash do tale: \n")
    
    for categoria in tabela_hash_tale:
        tamanho_categoria = len(tabela_hash_tale[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')

    for bucket in tabela_hash_quincas.values():
        bucket.clear() # esvaziando tabela
    
    for bucket in tabela_hash_tale.values():
        bucket.clear() # esvaziando tabela
        
'''
    while True:
        opcao = int(input("Qual operação você deseja executar?\n1 - Buscar palavra\n2 - Imprimir gráfico\n3 - Encerrar programa\nDigite a opção desejada: "))

        if(opcao == 1):
            tabelas_hash = {}
            lista_palavras, tamanho_tabela, _ = definirParametros()
            tabelas_hash = montarTabelasHash(lista_palavras, tamanho_tabela)

            palavra = str(input("Digite a palavra que deseja buscar: "))
            
            buscarPalavra(palavra, tamanho_tabela, tabelas_hash["hashSomaAscii"])

        elif(opcao == 2):
            tabelas_hash = {}
            lista_palavras, tamanho_tabela, cod_texto = definirParametros()

            if(cod_texto == 1): nome_texto = "Quincas"
            elif(cod_texto == 2): nome_texto = "Tale"
            
            tabelas_hash = montarTabelasHash(lista_palavras, tamanho_tabela)

            montarGrafico(tabelas_hash, nome_texto, tamanho_tabela)
            
        elif(opcao == 3):
            break

        else: opcao = int(input("Valor inválido. Digite novamente a opção desejada: "))