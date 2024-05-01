from os import wait
import pygame
from pathlib import Path

from sprite import Sprite
from turn_combat import CombatPlayer, Combat
from pygame_ai_player import PyGameAICombatPlayer
from pygame_human_player import PyGameHumanCombatPlayer
from util import write_to_timestamp_file

AI_SPRITE_PATH = Path("assets/ai.png")

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


class PyGameComputerCombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        if 30 < self.health <= 50:
            self.weapon = 2
        elif self.health <= 30:
            self.weapon = 1
        else:
            self.weapon = 0
        return self.weapon


def draw_combat_on_window(combat_surface, screen, player_sprite, opponent_sprite):
    screen.blit(combat_surface, (0, 0))
    player_sprite.draw_sprite(screen)
    opponent_sprite.draw_sprite(screen)
    text_surface = game_font.render("Choose s-Sword a-Arrow f-Fire!", True, (0, 0, 150))
    screen.blit(text_surface, (50, 50))
    pygame.display.update()


def run_turn(currentGame, player, opponent, timestamp_file):
    players = [player, opponent]
    states = list([tuple(player.health for player in players)] * 2)
    for current_player, state in zip(players, states):
        current_player.selectAction(state)

    currentGame.newRound()
    currentGame.takeTurn(player, opponent, timestamp_file)
    print("%s's health = %d" % (player.name, player.health))
    write_to_timestamp_file(
        timestamp_file, "%s's health = %d" % (player.name, player.health)
    )

    print("%s's health = %d" % (opponent.name, opponent.health))
    write_to_timestamp_file(
        timestamp_file, "%s's health = %d" % (opponent.name, opponent.health)
    )
    reward = currentGame.checkWin(player, opponent)

    # pygame.time.wait(50)


def run_pygame_combat(combat_surface, screen, player_sprite, timestamp_file):
    currentGame = Combat()

    player = PyGameAICombatPlayer("Oillill")

    opponent = PyGameComputerCombatPlayer("Computer")
    opponent_sprite = Sprite(
        AI_SPRITE_PATH, (player_sprite.sprite_pos[0] - 100, player_sprite.sprite_pos[1])
    )

    # Main Game Loop
    while not currentGame.gameOver:
        draw_combat_on_window(combat_surface, screen, player_sprite, opponent_sprite)

        run_turn(currentGame, player, opponent, timestamp_file)

    return currentGame.playerWon
