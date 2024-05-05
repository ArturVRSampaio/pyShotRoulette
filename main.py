from random import randrange as rand, shuffle

def print_health(health):
    print("Player 1")
    print("*" * health[0])
    print("Player 2")
    print("*" * health[1])
    print("-" * 20)

def load_shotgun():
    shotgun_rounds = rand(2, 8)
    live_rounds = rand(1, shotgun_rounds)
    blank_rounds = shotgun_rounds - live_rounds
    print(f"{shotgun_rounds} rounds. {live_rounds} live and {blank_rounds} blank")
    
    for i in range(live_rounds):
        shotgun_barrel.append(1)

    for i in range(blank_rounds):
        shotgun_barrel.append(0)
    
    shuffle(shotgun_barrel)
    return shotgun_barrel, live_rounds, blank_rounds, shotgun_rounds

def print_rounds(game_round):
    print("I   II  III ")
    print("    " * (game_round - 1) + "X" + "    " * (3 - game_round))
    print("-" * 20)

if __name__ == '__main__':
    game_round = 1
    health = [2, 2]
    current_player = 0
    shotgun_barrel = []
    while game_round < 4:        
        print_rounds(game_round)
        print_health(health)
        
        while health[0] > 0 and health[1] > 0:
            shotgun_barrel, live_rounds, blank_rounds, shotgun_rounds = load_shotgun()
            while len(shotgun_barrel) > 0 and health[0] > 0 and health[1] > 0:
                print(f"Player {current_player + 1} who do you shoot?")
                who = int(input("Player 1 or 2?\n"))
                if who > 2 or who < 1:
                    print("Invalid player")
                    continue
                who -= 1
                shot = shotgun_barrel.pop()
                health[who] -= shot
                
                if shot == 1:
                    print("Boom!")
                    print_health(health)
                else:
                    print("Click")
                
                if not (shot == 0 and who == current_player):
                    current_player = (current_player + 1) % 2
        
        print("\n\nRound over")
        game_round += 1
        health = [1 + game_round, 1 + game_round]
