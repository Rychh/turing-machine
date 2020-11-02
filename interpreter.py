import argparse
import sys
from typing import NewType, Dict, List
from dataclasses import dataclass
import os

DEBUG = True
sys.setrecursionlimit(251000)

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


@dataclass
class Tape:
    tape: List[Letter]
    limit_of_moves: int
    number_of_moves: int = 0
    index: int = 0

    def next_situation(self, current_move: Move) -> Situation:
        self.tape[self.index] = current_move.letter
        self.index += current_move.shift()
        self.number_of_moves += 1

        if self.index < 0 or self.number_of_moves >= self.limit_of_moves:
            return Situation(STATE_REJECT, Letter(0))

        if self.index == len(self.tape):
            self.tape.append(Letter(0))

        return Situation(current_move.state, self.tape[self.index])

    def get_initial_situation(self) -> Situation:
        return Situation(STATE_START, self.tape[0])

    def copy(self):
        return Tape(tape=self.tape.copy(),
                    limit_of_moves=self.limit_of_moves,
                    number_of_moves=self.number_of_moves,
                    index=self.index)


def simulate_turing_machine(current_situation: Situation, tape: Tape,
                            turing_machine: Dict[Situation, List[Move]]) -> State:
    if DEBUG:
        print(tape, " ", current_situation)
    if current_situation.state in FINAL_STATES:
        return current_situation.state
    elif current_situation not in turing_machine:
        return STATE_REJECT
    else:
        deterministic_move: bool = len(turing_machine[current_situation]) == 1
        for current_move in turing_machine[current_situation]:
            new_tape = tape if deterministic_move else tape.copy()
            new_situation = new_tape.next_situation(current_move=current_move)
            final_state = simulate_turing_machine(new_situation, new_tape, turing_machine)
            if final_state == STATE_ACCEPT:
                return STATE_ACCEPT
        return STATE_REJECT


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


def main():
    try:
        file_name: str = sys.argv[1]
        limit_of_moves: int = int(sys.argv[2])

        assert len(sys.argv) == 3
        assert os.path.isfile(file_name)

        input_word = input()
        if len(input_word) == 0:
            input_word = "00"

        inner_tape: List[Letter] = [Letter(int(letter)) for letter in input_word]
        tape: Tape = Tape(inner_tape, limit_of_moves)
        turing_machine = generate_turing_machine(file_name)
        final_state = simulate_turing_machine(tape.get_initial_situation(), tape, turing_machine)

        if final_state == STATE_ACCEPT:
            print("YES")
        else:
            print("NO")

    except Exception as e:
        print("Error: Wrong arguments", file=sys.stderr)
        print(e)


if __name__ == "__main__":
    main()
