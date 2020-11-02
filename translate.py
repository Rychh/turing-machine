import argparse
import sys
from typing import NewType, Dict, List
from dataclasses import dataclass
import os

DEBUG = False

Letter = NewType('Letter', int)
State = NewType('State', str)
Direction = NewType('Direction', str)

STATE_ACCEPT = State("accept")
STATE_REJECT = State("reject")
STATE_START = State("start")
FINAL_STATES = [STATE_ACCEPT, STATE_REJECT]

DIR_STAY = Direction("S")
DIR_RIGHT = Direction("R")
DIR_LEFT = Direction("L")
DIRS = [DIR_STAY, DIR_RIGHT, DIR_LEFT]


@dataclass
class Situation:
    state: State
    letter: Letter

    def end_of_calculations(self) -> bool:
        return self.state in FINAL_STATES

    def __str__(self):
        return "Situ: " + " St:" + str(self.state) + " Lt:" + str(self.letter)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.state == other.state and self.letter == other.letter


@dataclass
class Move:
    state: State
    letter: Letter
    direction: Direction

    def accepting_word(self) -> bool:
        return self.state == State("accept")

    def shift(self) -> int:
        if self.direction == DIR_RIGHT:
            return 1
        elif self.direction == DIR_LEFT:
            return -1
        else:
            return 0

    def __str__(self):
        return "Move:" + " St:" + str(self.state) + " Lt:" + str(self.letter) + "Dr:" + str(self.direction)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.state == other.state and self.letter == other.letter and self.direction == other.direction


def generate_turing_machine(file_name: str) -> Dict[Situation, List[Move]]:
    generated_turing_machine: Dict[Situation, List[Move]] = {}
    file = open(file_name, 'r')
    instructions = file.readlines()
    try:
        for instruction in instructions:
            words = instruction.split(" ")
            current_state: State = State(words[0])
            currently_seen_letter: Letter = Letter(int(words[1]))
            target_state: State = State(words[2])
            letter_to_write: Letter = Letter(int(words[3]))
            direction: Direction = Direction(words[4][0])

            assert direction in DIRS
            situation = Situation(current_state, currently_seen_letter)
            move = Move(target_state, letter_to_write, direction)

            if situation not in generated_turing_machine:
                generated_turing_machine[situation] = []

            generated_turing_machine[situation].append(move)
    except Exception as e:
        print("Error: During parsing Turing Machine's description. Machine may not be complete.", file=sys.stderr)
        print(e)

    return generated_turing_machine

