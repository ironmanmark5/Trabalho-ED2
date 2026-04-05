import math, random

def le_arquivo_quincas():
    lista_palavras = []
    with open("quincasborba-utf8-limpo.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavras = linha.split() # funcao split é para separar palavra por palavra
            for palavra in palavras:
                if palavra not in lista_palavras:
                    lista_palavras.append(palavra)
                    
    return lista_palavras

def le_arquivo_tale():
    lista_palavras = []
    with open("tale.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavras = linha.split() # funcao split é para separar palavra por palavra
            for palavra in palavras:
                if palavra not in lista_palavras:
                    lista_palavras.append(palavra)
                    
    return lista_palavras

def hashSomaAscii(palavra: str, tamanho_tabela: int):
    soma_ascii = 0

    for letra in palavra.lower():
        soma_ascii += ord(letra)
    
    return (soma_ascii) % tamanho_tabela

def hashSomaPonderada(palavra: str, tamanho_tabela: int):
    soma_ascii = 0

    for i, letra in enumerate(palavra.lower()):
        soma_ascii += (i + 1) * ord(letra)

    return (soma_ascii) % tamanho_tabela

def hashMeio(palavra: str, tamanho_tabela: int):
    indice_meio = len(palavra) // 2 # arredonda para numero inteiro
    letra = palavra[indice_meio]

    cod_acsii = ord(letra)

    return cod_acsii % tamanho_tabela

def hashRandom(tamanho_tabela: int):
    codigo = random.randint(1, 1_000_000)

    return codigo % tamanho_tabela
    
if __name__ == "__main__":
    codigo = int(input("Escolha o tamanho da tabela:\n1 - 97\n2 - 100\n3 - 997\n"))
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


    # ------------------- Hash Random -------------------
    print("\n" + (10 * "-") + " Hash Random " + (10 * "-") + "\n")

    for palavra in lista_quincas:
        bucket = hashRandom(tamanho)
        tabela_hash_quincas[bucket].append(palavra)
   
    print("\nHistograma da tabela hash do quincas: \n")

    for categoria in tabela_hash_quincas:
        tamanho_categoria = len(tabela_hash_quincas[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')
    
    for palavra in lista_tale:
        bucket = hashRandom(tamanho)
        tabela_hash_tale[bucket].append(palavra)
    
    print("\nHistograma da tabela hash do tale: \n")
    
    for categoria in tabela_hash_tale:
        tamanho_categoria = len(tabela_hash_tale[categoria])
        print(f'Categoria: {categoria} - {int(tamanho_categoria / 10) * '*'}')

    for bucket in tabela_hash_quincas.values():
        bucket.clear() # esvaziando tabela
    
    for bucket in tabela_hash_tale.values():
        bucket.clear() # esvaziando tabela