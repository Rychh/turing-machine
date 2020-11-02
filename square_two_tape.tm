start 1 go_right 7 0 R S
start 2 0 go_right 8 0 R S
start 0 0 accept 0 0 S
go_right 1 go_right 1 R S
go_right 2 0 go_right 2 0 R S
go_right 0 0 one_step_left 0 0 L S 
go_right 3 0 one_step_left 3 0 L S 
go_right 4 0 one_step_left 4 0 L S 
go_left 1 go_left 1 L S 
go_left 2 0 go_left 2 0 L S 
go_left 3 0 one_step_right 3 0 R S
go_left 4 0 one_step_right 4 0 R S
go_left 7 0 one_step_right 7 0 R S
go_left 8 0 one_step_right 8 0 R S
one_step_right 1 go_right 3 0 R S
one_step_right 2 0 go_right 4 0 R S
one_step_right 3 0 go_left_check_5_skip 5 0 S
one_step_right 4 0 go_left_check_6_skip 6 0 S
one_step_left 1 go_left 3 0 L S 
one_step_left 2 0 go_left 4 0 L S 
one_step_left 3 0 reject 3 0 S
one_step_left 4 0 reject 4 0 S
go_left_check_5_skip 3 0 go_left_check_5_next 3 0 S
go_left_check_5_skip 4 0 go_left_check_5_next 4 0 S
go_left_check_5_skip 5 0 go_left_check_5_skip 5 0 L S 
go_left_check_5_skip 6 0 go_left_check_5_skip 6 0 L S 
go_left_check_5_next 3 0 go_left_check_5_next 3 0 L S 
go_left_check_5_next 4 0 go_left_check_5_next 4 0 L S 
go_left_check_5_next 5 0 one_step_right_check_5 5 0 R S
go_left_check_5_next 6 0 one_step_right_check_5 6 0 R S
go_left_check_5_next 7 0 go_right_skip 5 0 R S
go_left_check_5_next 8 0 reject 8 0 S
go_left_check_6_skip 3 0 go_left_check_6_next 3 0 S
go_left_check_6_skip 4 0 go_left_check_6_next 4 0 S
go_left_check_6_skip 5 0 go_left_check_6_skip 5 0 L S 
go_left_check_6_skip 6 0 go_left_check_6_skip 6 0 L S 
go_left_check_6_next 3 0 go_left_check_6_next 3 0 L S 
go_left_check_6_next 4 0 go_left_check_6_next 4 0 L S 
go_left_check_6_next 5 0 one_step_right_check_6 5 0 R S
go_left_check_6_next 6 0 one_step_right_check_6 6 0 R S
go_left_check_6_next 7 0 reject 7 0 S
go_left_check_6_next 8 0 go_right_skip 6 0 R S
go_right_skip 3 0 go_right_skip 3 0 R S
go_right_skip 4 0 go_right_skip 4 0 R S
go_right_skip 5 0 go_right_next 5 0 S
go_right_skip 6 0 go_right_next 6 0 S
go_right_next 0 0 accept 0 0 S
go_right_next 3 0 go_left_check_5_skip 5 0 S
go_right_next 4 0 go_left_check_6_skip 6 0 S
go_right_next 5 0 go_right_next 5 0 R S
go_right_next 6 0 go_right_next 6 0 R S
one_step_right_check_5 3 0 go_right_skip 5 0 R S
one_step_right_check_5 4 0 reject 4 0 S
one_step_right_check_6 3 0 reject 3 0 S
one_step_right_check_6 4 0 go_right_skip 6 0 R