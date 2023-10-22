import random

# Definir os jogadores
def get_player_info():
    num_players = int(input("Quantos jogadores (até 5) deseja adicionar? "))
    players = []
    for i in range(num_players):
        name = input(f"Nome do jogador {i + 1}: ")
        players.append({"name": name, "cards": []})
    return players

# Cartelas geradas
def generate_card():
    return [random.sample(range(1, 51), 5) for _ in range(5)]

def generate_cards(players):
    for player in players:
        player["cards"] = [generate_card() for _ in range(1, 6)]

# Exibir as cartelas
def display_cards(players):
    for i, player in enumerate(players, start=1):
        print(f"Cartelas do jogador {i} ({player['name']}):")
        for card in player['cards']:
            for row in card:
                print(" ".join(map(str, row)))
            print()

# Sorteio dos números
def draw_number(used_numbers):
    number = random.randint(1, 50)
    while number in used_numbers:
        number = random.randint(1, 50)
    used_numbers.add(number)
    return number

# Verificação do ganhador
def check_winner(player, drawn_numbers):
    for card in player['cards']:
        for i in range(5):
            if all(number in drawn_numbers for number in card[i]):
                return True
            if all(card[j][i] in drawn_numbers for j in range(5)):
                return True
        if all(card[i][i] in drawn_numbers for i in range(5)) or all(card[i][4 - i] in drawn_numbers for i in range(5)):
            return True
    return False

# O controle do ranking 
def update_ranking(player_name, rankings):
    for i, (name, wins) in enumerate(rankings):
        if name == player_name:
            rankings[i] = (name, wins + 1)
            return
    rankings.append((player_name, 1))
    rankings.sort(key=lambda x: x[1], reverse=True)

def display_ranking(rankings):
    print("Ranking de Jogadores:")
    for i, (name, wins) in enumerate(rankings, start=1):
        print(f"{i}. {name} - {wins} vitórias")

def main():
    used_numbers = set()
    rankings = []
    while True:
        players = get_player_info()
        generate_cards(players)
        display_cards(players)
        drawn_numbers = set()
        winner = None
        while not winner:
            input("Pressione Enter para sortear um número...")
            number = draw_number(used_numbers)
            drawn_numbers.add(number)
            print(f"Número sorteado: {number}")
            for i, player in enumerate(players):
                if check_winner(player, drawn_numbers):
                    winner = player
                    update_ranking(player["name"], rankings)
                    break
        print(f"O jogador {winner['name']} venceu!")
        display_ranking(rankings)
        play_again = input("Deseja jogar novamente? (s/n): ")
        if play_again.lower() != 's':
            break

if __name__ == "__main__":
    main()