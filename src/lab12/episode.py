import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from lab11.turn_combat import CombatPlayer, Combat, ComputerCombatPlayer
from lab11.pygame_ai_player import PyGameAICombatPlayer

""" 
Lab 12: Beginnings of Reinforcement Learning

Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.  
Reward is the reward for the player for that turn.
"""


def run_episode(player1: CombatPlayer, player2: CombatPlayer):
    episode_history = []

    # Initialize Combat system
    current_game = Combat()

    while not current_game.gameOver:
        # Player 1's turn
        observation = (player1.health, player2.health)
        player1_action = player1.selectAction(observation)
        # current_game.takeTurn(player1, player2)  # Execute turn using the Combat class
        # reward = calculate_reward(player1.action, player2.action)
        # episode_history.append((observation, action, reward))

        # Player 2's turn
        observation = (player1.health, player2.health)
        player2_action = player2.selectAction(observation)
        current_game.takeTurn(player1, player2)
        player1_reward = calculate_reward(player1.action, player2.action)
        player2_reward = calculate_reward(player2.action, player1.action)
        episode_history.append(
            (
                observation,
                (player1_action, player2_action),
                (player1_reward, player2_reward),
            )
        )
        # episode_history.append((observation, action, reward))

        current_game.checkWin(player1, player2)

    return episode_history


def calculate_reward(action1, action2):
    if action1 == 0 and action2 == 2:  # Sword vs Fire
        return 1
    elif action1 == 1 and action2 == 0:  # Arrow vs Sword
        return 1
    elif action1 == 2 and action2 == 1:  # Fire vs Arrow
        return 1
    elif action1 == action2:  # Draw
        return 0
    else:
        return -1


if __name__ == "__main__":

    player1 = PyGameAICombatPlayer("Player1")
    player2 = PyGameAICombatPlayer("Player2")
    episode = run_episode(player1, player2)
    for i, turn in enumerate(episode):
        print(i, turn)
