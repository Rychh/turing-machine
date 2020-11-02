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
class Situation2Tape:
    state: State
    letter_1: Letter
    letter_2: Letter

    def __str__(self):
        return "Situ: " + " St:" + str(self.state) + " Lt1:" + str(self.letter_1) + " Lt2:" + str(self.letter_2)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)


@dataclass
class Move2Tape:
    state: State
    letter_1: Letter
    letter_2: Letter
    direction_1: Direction
    direction_2: Direction

    def __str__(self):
        return "Move:" + " St:" + str(self.state) + " Lt1:" + str(self.letter_1) + " Lt2:" + str(
            self.letter_2) + " Dr1:" + str(self.direction_1) + " Dr2:" + str(self.direction_2)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)


def generate_turing_machine(file_name: str) -> Dict[Situation2Tape, List[Move2Tape]]:
    generated_turing_machine: Dict[Situation2Tape, List[Move2Tape]] = {}
    file = open(file_name, 'r')
    instructions = file.readlines()
    try:
        for instruction in instructions:
            words = instruction.split(" ")
            # <state> <let1> <let2> <target_state> <out_let1> <out_let2> <dir1> <dir2>
            state: State = State(words[0])
            let1: Letter = Letter(int(words[1]))
            let2: Letter = Letter(int(words[2]))
            target_state: State = State(words[3])
            out_let1: Letter = Letter(int(words[4]))
            out_let2: Letter = Letter(int(words[5]))
            dir1: Direction = Direction(words[6][0])
            dir2: Direction = Direction(words[7][0])

            situation = Situation2Tape(state, let1, let2)
            move = Move2Tape(target_state, out_let1, out_let2, dir1, dir2)
            if situation not in generated_turing_machine:
                generated_turing_machine[situation] = []

            generated_turing_machine[situation].append(move)
    except Exception as e:
        print("Error: During parsing Turing Machine's description. Machine may not be complete.", file=sys.stderr)
        print(e)

    return generated_turing_machine


def get_all_states(turing_machine: Dict[Situation2Tape, List[Move2Tape]]) -> List[State]:
    result: List[State] = []
    for situation in turing_machine.keys():
        result += situation.state
        for move in turing_machine[situation]:
            result += move.state

    result = list(set(result))
    result.sort()
    return result
