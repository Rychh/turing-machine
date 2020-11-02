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


new_instructions_forms: List[str] = [
    "go_right_to_2nd_{lit_02}_{dir_LRS} X go_right_to_2nd_{lit_02}_{dir_LRS}  X R",
    "go_right_to_2nd_{lit_02}_{dir_LRS} 9 go_right_to_2nd_{lit_02}_{dir_LRS}_and_push_9 0 R",
    "go_right_to_2nd_{lit_02}_{dir_LRS}_and_push_9 0 go_left_to_2nd_{lit_02}_{dir_LRS} 9 L",

    "go_left_to_2nd_{lit_02}_{dir_LRS} {lit_05} go_left_to_2nd_{lit_02}_{dir_LRS} X L",
    "go_left_to_2nd_{lit_02}_{dir_LRS} {lit_02_plus_6} move_2nd_{dir_LRS} {lit_02} {dir_LRS}",
    "move_2nd_{dir_LRS} X set_2nd X {dir_LRS}",

    "set_2nd {lit_02} go_right_to_1st_head_{lit_02_plus_6} {lit_02_plus_6} R",

    "go_left_to_2nd {lit_02_plus_6} go_right_to_1st_head_{lit_02_plus_6} {lit_02_plus_6} R",

    "go_right_to_1st_head_{lit_02_plus_6} X go_right_to_1st_head_{lit_02_plus_6} X R",
    "go_right_to_1st_head_{lit_02_plus_6} 9 go_right_to_1st_head_{lit_02_plus_6}_and_push_9 0 R",
    "go_right_to_1st_head_{lit_02_plus_6}_and_push_9 0 go_left_to_1st_head_{lit_02_plus_6} 9 L",

    "go_left_to_1st_head_{lit_02_plus_6} X go_left_to_1st_head_{lit_02_plus_6} X L",

    "move_1st_{dir_LRS}_2nd_{lit_02}_{dir_LRS} {lit_02} X {dir_LRS} set_1st_{lit_02}_{dir_LRS} X {dir_LRS}",
    "set_1st_{lit_02}_{dir_LRS} X go_right_to_2nd_{lit_02}_{dir_LRS} {lit_02_plus3} S",
]


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


def main():
    file_name: str = sys.argv[1]

    assert os.path.isfile(file_name)

    turing_machine = generate_turing_machine(file_name)
    all_states = get_all_states(turing_machine)

    new_instructions: List[str] = []
    format_arguments = {}
    for form in new_instructions_forms:
        for state in all_states:
            form_x_state: List[str] = []
            for lit_02_value in range(3):
                format_arguments['lit_02'] = lit_02_value
                format_arguments['lit_02_plus_6'] = Letter(lit_02_value + 6)
                for lit_05_value in range(6):
                    format_arguments['lit_05'] = Letter(lit_05_value)
                    for dir_LRS in DIRS:
                        format_arguments['dir_LRS'] = dir_LRS
                        form_x_state.append(state + "::" + form.format(**format_arguments))
            form_x_state = list(set(form_x_state))
            form_x_state.sort()
            new_instructions = new_instructions + form_x_state

    for situation in turing_machine.keys():
        for move in turing_machine[situation]:
            format_arguments = {'state': situation.state,
                                'let1': situation.letter_1,
                                'let2': situation.letter_2,
                                'target_state': move.state,
                                'out_let1': move.letter_1,
                                'out_let2': move.letter_2,
                                'dir1': move.direction_1,
                                'dir2': move.direction_2,
                                'let1_plus_3': situation.letter_2 + 3,
                                'let2_plus_6': situation.letter_2 + 6,
                                }

            normal_state_transition = "{state}::go_left_to_1st_head_{let2_plus_6} {let1_plus_3} " \
                                      "{target_state}::move_1st_{dir1}_2nd_{out_let2}_{dir1} {out_let1} {dir2}"

            final_state_transition = "{state}::go_left_to_1st_head_{let2_plus_6} {let1_plus_3} " \
                                     "{target_state} {out_let1} {dir2}"

            state_transition = final_state_transition if move.state in FINAL_STATES else normal_state_transition

            new_instructions.append(state_transition.format(**format_arguments))


if __name__ == "__main__":
    main()
