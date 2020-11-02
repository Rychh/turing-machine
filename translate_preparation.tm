start 1 preparation_one_step_right 3 R
start 2 preparation_one_step_right 4 R
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
preparation_set_2nd_head 0 accept 6 L

go_right_to_2nd_<0-2>_<L/R> X go_right_to_2nd_<0-2>_<L/R>  X R
go_right_to_2nd_<0-2>_<L/R>  9 go_right_to_2nd_<0-2>_<L/R>_and_push_9 0 R
go_right_to_2nd_<0-2>_<L/R>_and_push_9 0 go_left_to_2nd_<0-2>_<L/R> 9 L

go_left_to_2nd_<0-2>_<L/R> <0-5> go_left_to_2nd_<0-2>_<L/R> X L
go_left_to_2nd_<0-2>_<L/R> <6-8> move_2nd_<L/R> <0-2> L/R
move_2nd_<L/R> X set_2nd X <L/R>

set_2nd <0-2> go_right_to_1st_head_<6-8> <6-8> R

go_left_to_2nd <6-8> go_right_to_1st_head_<6-8> <6-8> R

go_right_to_1st_head_<6-8> X go_right_to_1st_head_<6-8> X R
go_right_to_1st_head_<6-8> 9 go_right_to_1st_head_<6-8>_and_push_9 0 R
go_right_to_1st_head_<6-8>_and_push_9 0 go_left_to_1st_head_<6-8> 9 L

go_left_to_1st_head_<6-8> X go_left_to_1st_head_<6-8> X L
go_left_to_1st_head_<6-8> <3-5> _inny_prefiks_move_1st_<L/R>_2nd_<0-2>_<L/R> <0-2> <L/R>
move_1st_<L/R>_2nd_<0-2>_<L/R> <0-2> X <L/R> set_1st_<0-2>_<L/R> X <L/R>
set_1st_<0-2>_<L/R> X go_right_to_2nd_<0-2>_<L/R> (X+3) S