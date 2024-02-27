"""
Lab 4: Rock-Paper-Scissor AI Agent

In this lab you will build one AI agent for the game of Rock-Paper-Scissors, that can defeat a few different kinds of 
computer players.

You will update the AI agent class to create your first AI agent for this course.
Use the precept sequence to find out which opponent agent you are facing,  
so that it can beat these three opponent agents:

    Agent Single:  this agent picks a weapon at random at the start, 
                   and always plays that weapon.  
                   For example: 2,2,2,2,2,2,2,.....

    Agent Switch:  this agent picks a weapon at random at the start,
                   and randomly picks a weapon once every 10 rounds.  
                   For example:  2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,...

    Agent Mimic:  this agent picks a weapon at random in the first round, 
                  and then always does what you did the previous round.  
                  For example:  if you played 1,2,0,1,2,0,1,2,0,...  
                   then this agent would play 0,1,2,0,1,2,0,1,2,...

Discussions in lab:  You don't know ahead of time which opponent you will be facing, 
so the first few rounds will be used to figure this out.   How?

Once you've figured out the opponent, apply rules against that opponent. 
A model-based reflex agent uses rules (determined by its human creator) to decide which action to take.

If your AI is totally random, you should be expected to win about 33% of the time, so here is the requirement:  
In 100 rounds, you should consistently win at least 85 rounds to be considered a winner.

You get a 0 point for beating the single agent, 1 points for beating the switch agent, 
and 4 points for beating the mimic agent.

"""

import math
from random import randint
from typing import Dict
from rock_paper_scissor import Player
from rock_paper_scissor import run_game
from rock_paper_scissor import random_weapon_select


def beats(move_to_beat: int) -> int:
    # 0: rock, 1: paper, 2: scissors
    matchups: Dict = {0: 1, 1: 2, 2: 0}
    return matchups[move_to_beat]


class AiPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.initial_weapon = random_weapon_select()

    def weapon_selecting_strategy(self):
        # make a random move to bait mimic
        if len(self.opponent_choices) < 1:
            return randint(0, 2)

        # this slice gets the last three elements BEFORE the actual last one
        # [0, 1, 2, 3, 4, 5][three_bef_last] = [2, 3, 4]
        three_bef_last = slice(-4, -1)
        # check for mimic condition
        is_mimicking = self.opponent_choices[-3:] == self.my_choices[three_bef_last]
        # if so, play the move that beats the player's last move (mimic's next move)
        if is_mimicking:
            return beats(self.my_choices[-1])

        # otherwise, play the move that beats the opponent's last move
        # if it's single, player always wins
        # if it's switch, player always wins except each time switch occurs
        return beats(self.opponent_choices[-1])


if __name__ == "__main__":
    final_tally: list[int] = [0] * 3
    for agent in range(3):
        for i in range(100):
            tally: list[int] = [
                score for _, score in run_game(AiPlayer("AI"), 100, agent)
            ]
            if sum(tally) == 0:
                final_tally[agent] = 0
            else:
                final_tally[agent] += tally[0] / sum(tally)

    print("Final tally: ", final_tally)
