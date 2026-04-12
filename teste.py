
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


    lista_quincas = le_arquivo_quincas()
    # tamanho_quincas = math.floor((len(lista_quincas)) / 0.7) # a = n/M , 0.7 = 11808 / M => 16868 (arrendado para baixo)


    print(len(lista_quincas))

    lista_tale = le_arquivo_tale()
    # tamanho_tale = math.floor((len(lista_tale)) / 0.7) # a = 0.7 floorMod(x, y)

    # print(len(lista)) # 19695 palavras em tale.txt e 11808 em quincasborba-utf8-limpo.txt