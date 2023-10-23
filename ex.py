
#RM550415 Igor Ribeiro Anccilotto
#RM551304 Gustavo Arguello Bertacci

import random

# Definição dos jogadores
def obter_informacoes_jogadores():
    while True:
        num_jogadores = int(input("Quantos jogadores (até 5) deseja adicionar? "))
        if num_jogadores >= 1 and num_jogadores <= 5:
            break
        else:
            print("Número de jogadores deve ser entre 1 e 5.")
    
    jogadores = []
    for i in range(num_jogadores):
        nome = input(f"Nome do jogador {i + 1}: ")
        jogadores.append({"nome": nome, "cartelas": []})
    return jogadores

# Geração das cartelas
def gerar_cartela():
    return [random.sample(range(1, 51), 5) for _ in range(5)]

def gerar_cartelas(jogadores):
    for jogador in jogadores:
        jogador["cartelas"] = [gerar_cartela() for _ in range(1, 6)]

# Exibição das cartelas
def exibir_cartelas(jogadores):
    for i, jogador in enumerate(jogadores, start=1):
        print(f"Cartelas do jogador {i} ({jogador['nome']}):")
        for cartela in jogador['cartelas']:
            for linha in cartela:
                print(" ".join(map(str, linha)))
            print()

# Sorteio dos números
def sortear_numero(numeros_utilizados):
    numero = random.randint(1, 50)
    while numero in numeros_utilizados:
        numero = random.randint(1, 50)
    numeros_utilizados.add(numero)
    return numero

# Verificação do vencedor
def verificar_vencedor(jogador, numeros_sorteados):
    for cartela in jogador['cartelas']:
        for i in range(5):
            if all(numero in numeros_sorteados for numero in cartela[i]):
                return True
            if all(cartela[j][i] in numeros_sorteados for j in range(5)):
                return True
        if all(cartela[i][i] in numeros_sorteados for i in range(5)) or all(cartela[i][4 - i] in numeros_sorteados for i in range(5)):
            return True
    return False

# Controle do ranking
def atualizar_ranking(nome_jogador, rankings):
    for i, (nome, vitorias) in enumerate(rankings):
        if nome == nome_jogador:
            rankings[i] = (nome, vitorias + 1)
            return
    rankings.append((nome_jogador, 1))
    rankings.sort(key=lambda x: x[1], reverse=True)

def exibir_ranking(rankings):
    print("Ranking de Jogadores:")
    for i, (nome, vitorias) in enumerate(rankings, start=1):
        print(f"{i}. {nome} - {vitorias} vitorias")

def salvar_ranking_em_arquivo(rankings):
    with open("ranking.txt", "w") as arquivo:
        for nome, vitorias in rankings:
            arquivo.write(f"{nome} - {vitorias} vitorias\n")

def main():
    numeros_utilizados = set()
    rankings = []

    while True:
        jogadores = obter_informacoes_jogadores()
        gerar_cartelas(jogadores)
        exibir_cartelas(jogadores)
        numeros_sorteados = set()
        vencedor = None
        while not vencedor:
            input("Pressione Enter para sortear um número...")
            numero = sortear_numero(numeros_utilizados)
            numeros_sorteados.add(numero)
            print(f"Número sorteado: {numero}")
            for i, jogador in enumerate(jogadores):
                if verificar_vencedor(jogador, numeros_sorteados):
                    vencedor = jogador
                    atualizar_ranking(jogador["nome"], rankings)
                    break
        print(f"O jogador {vencedor['nome']} venceu!")
        exibir_ranking(rankings)

        # Salvar ranking em um arquivo
        salvar_ranking_em_arquivo(rankings)

        jogar_novamente = input("Deseja jogar novamente? (s/n): ")
        if jogar_novamente.lower() != 's':
            break

if __name__ == "__main__":
    main()