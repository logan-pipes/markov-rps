"""
"  rps.py
"
"  Author: Logan Pipes
"  Date:   30-01-2023
"
"  AI for rock, paper, scissors that repeatedly updates a Markov model
"  with the frequency that the user plays certain options in response to the throws of the last round.
"
"""

import random


# Given the state of the last round, the key for which moves lose against other moves,
# and the frequencies by which the opponent repeats moves, make a random (but optimal) move
def pick_move(state, loses_to, frequencies):
    response_freqs = frequencies[state]
    if sum(response_freqs.values()) == 0: # Not encountered this state before
        return random.choice(tuple(loses_to.keys())) # So do anything
    # Otherwise, use the knowledge of what the opponent likes to follow given state from
    return random.choice(loses_to[random.choices(valid_moves, weights=[response_freqs[move] for move in valid_moves])[0]])


if __name__ == "__main__":
    # A dictionary with entries "A":["B", "C"] which implies "B" and "C" both beat "A" in a game of rock paper scissors
    # Should contain all possible options for a player to throw, and what beats each of them
    loses_to = {'R':['P'], 'S':['R'], 'P':['S']}

    valid_moves = list(loses_to.keys()) # Get list of all valid throws
    frequencies = { (first_player,second_player) : {move:0 for move in valid_moves}
            for first_player in valid_moves for second_player in valid_moves}

    print("""Let's play Rock Paper Scissors.

The rules are as follows:
Each turn, you and the computer can play either rock (R), paper (P), or scissors (S).
Rock beats scissors, paper beats rock, and scissors beats paper.
If you and the computer choose the same option, it's a tie.
Alternatively, you can type Q to quit.
""")
    wins = 0
    losses = 0
    ties = 0
    games_played = 0
    
    state = (random.choice(valid_moves), random.choice(valid_moves)) # Initial state is random
    ai_move = pick_move(state, loses_to, frequencies)
    
    print("Enter ", ', '.join(valid_moves), ", or Q to quit: ", sep='', end='') # Get input
    response = input().upper()
    while response != 'Q' and response != 'QUIT':
        if response not in valid_moves: # Repeat until input is valid
            print("That is not one of the valid options. Please try again.")
            print("Enter ", ', '.join(valid_moves), ", or Q to quit: ", sep='', end='')
            response = input().upper()
            continue
        human_move = response

        print("You played %s while the computer played %s." % (human_move, ai_move)) # Print outcome
        if ai_move in loses_to[human_move]:
            print("You lost.")
            losses += 1
        elif human_move in loses_to[ai_move]:
            print("You won.")
            wins += 1
        else:
            print("You tied.")
            ties += 1
        games_played += 1
        print("Of {} games played, you have won {}, lost {}, and tied {}. That's a win rate of {:2.2f}%.".format(games_played, wins, losses, ties, 100*wins/games_played))

        frequencies[state][human_move] += 1 # Update known info
        state = (human_move, ai_move)
        ai_move = pick_move(state, loses_to, frequencies) # Pick new move

        print()
        print("Would you like to play another game?") # Prompt for replay
        print("Enter ", ', '.join(valid_moves), ", or Q to quit: ", sep='', end='')
        response = input().upper()
