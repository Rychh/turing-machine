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
    "{state}::go_right_to_2nd_{lit_02}_{dir_LRS} {lit_08} {state}::go_right_to_2nd_{lit_02}_{dir_LRS} {lit_08} R",
    "{state}::go_right_to_2nd_{lit_02}_{dir_LRS} 9 {state}::go_right_to_2nd_{lit_02}_{dir_LRS}_and_push_9 0 R",
    "{state}::go_right_to_2nd_{lit_02}_{dir_LRS}_and_push_9 0 {state}::go_left_to_2nd_{lit_02}_{dir_LRS} 9 L",

    "{state}::go_left_to_2nd_{lit_02}_{dir_LRS} {lit_05} {state}::go_left_to_2nd_{lit_02}_{dir_LRS} {lit_05} L",
    "{state}::go_left_to_2nd_{lit_02}_{dir_LRS} {lit_68} {state}::move_2nd_{dir_LRS} {lit_02} {dir_LRS}",
    "{state}::move_2nd_{dir_LRS} {lit_05} {state}::set_2nd {lit_05} {dir_LRS}",

    "{state}::set_2nd {lit_02} {state}::go_right_to_1st_head_{lit_02_plus_6} {lit_02_plus_6} R",

    "{state}::go_right_to_1st_head_{lit_02_plus_6} {lit_05} {state}::go_right_to_1st_head_{lit_02_plus_6} {lit_05} R",
    "{state}::go_right_to_1st_head_{lit_02_plus_6} 9 {state}::go_right_to_1st_head_{lit_02_plus_6}_and_push_9 0 R",
    "{state}::go_right_to_1st_head_{lit_02_plus_6}_and_push_9 0 {state}::go_left_to_1st_head_{lit_02_plus_6} 9 L",

    "{state}::go_left_to_1st_head_{lit_02_plus_6} {lit_02_68} {state}::go_left_to_1st_head_{lit_02_plus_6} {lit_02_68} L",

    "{state}::move_1st_{dir_LRS}_2nd_{lit_02}_{dir_LRSp} {lit_02_68} {state}::set_1st_{lit_02}_{dir_LRSp} {lit_02_68} {dir_LRS}",
    "{state}::set_1st_{lit_02p}_{dir_LRS} {lit_02} {state}::go_right_to_2nd_{lit_02p}_{dir_LRS} {lit_02_plus_3} S",
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
        result.append(situation.state)
        for move in turing_machine[situation]:
            result.append(move.state)

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
            format_arguments['state'] = state
            for lit_02_value in range(3):
                format_arguments['lit_02'] = lit_02_value
                format_arguments['lit_02_plus_3'] = Letter(lit_02_value + 3)
                format_arguments['lit_02_plus_6'] = Letter(lit_02_value + 6)
                for lit_08_value in range(9):
                    format_arguments['lit_05'] = Letter(lit_08_value) if lit_08_value <= 5 else Letter(0)
                    format_arguments['lit_02_68'] = Letter(
                        lit_08_value) if lit_08_value <= 2 or 6 <= lit_08_value else Letter(0)
                    format_arguments['lit_08'] = Letter(lit_08_value)
                    format_arguments['lit_02p'] = Letter(lit_08_value) if lit_08_value <= 2 else Letter(0)
                    for lit_68_value in range(6, 9):
                        format_arguments['lit_68'] = Letter(lit_68_value)
                        for dir_LRS in DIRS:
                            format_arguments['dir_LRS'] = dir_LRS
                            for dir_LRSp in DIRS:
                                format_arguments['dir_LRSp'] = dir_LRSp
                                form_x_state.append(form.format(**format_arguments))
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
                                'let1_plus_3': situation.letter_1 + 3,
                                'let2_plus_6': situation.letter_2 + 6,
                                }

            normal_state_transition = "{state}::go_left_to_1st_head_{let2_plus_6} {let1_plus_3} " \
                                      "{target_state}::move_1st_{dir1}_2nd_{out_let2}_{dir2} {out_let1} {dir1}"

            final_state_transition = "{state}::go_left_to_1st_head_{let2_plus_6} {let1_plus_3} " \
                                     "{target_state} {out_let1} {dir1}"

            if move.state in FINAL_STATES:
                state_transition = final_state_transition
            else:
                state_transition = normal_state_transition

            new_instructions.append(state_transition.format(**format_arguments))
    new_instructions.append("start_part_2 4 start::go_left_to_1st_head_6 4 S")
    new_instructions.append("start_part_2 5 start::go_left_to_1st_head_6 5 S")

    # print(turing_machine)
    # print(all_states)

    print("""start 1 preparation_one_step_right 4 R
start 2 preparation_one_step_right 5 R
preparation_copy_right_1 0 preparation_go_back 1 S
preparation_copy_right_1 1 preparation_copy_right_1 1 R
preparation_copy_right_1 2 preparation_copy_right_2 1 R
preparation_copy_right_2 0 preparation_go_back 2 S
preparation_copy_right_2 1 preparation_copy_right_1 2 R
preparation_copy_right_2 2 preparation_copy_right_2 2 R
preparation_go_back 0 preparation_two_step_right 0 R
preparation_go_back 1 preparation_go_back 1 L
preparation_go_back 2 preparation_go_back 2 L
preparation_two_step_right 0 preparation_one_step_right 0 R
preparation_two_step_right 1 preparation_one_step_right 1 R
preparation_two_step_right 2 preparation_one_step_right 2 R
preparation_one_step_right 0 preparation_go_to_start 9 L
preparation_one_step_right 1 preparation_copy_right_1 0 R
preparation_one_step_right 2 preparation_copy_right_2 0 R
preparation_go_to_start 0 preparation_go_to_start 0 L
preparation_go_to_start 1 preparation_go_to_start 1 L
preparation_go_to_start 2 preparation_go_to_start 2 L
preparation_go_to_start 3 preparation_set_2nd_head 3 R
preparation_go_to_start 4 preparation_set_2nd_head 4 R
preparation_go_to_start 5 preparation_set_2nd_head 5 R
preparation_set_2nd_head 0 start_part_2 6 L
preparation_set_2nd_head 9 quick_fix_make_room_1 0 R
quick_fix_make_room_1 0 quick_fix_make_room_2 0 R
quick_fix_make_room_2 0 quick_fix_go_back 9 L
quick_fix_go_back 0 preparation_set_2nd_head 0 L""")
    for new_instruction in new_instructions:
        print(new_instruction)


if __name__ == "__main__":
    main()
