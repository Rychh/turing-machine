start 1 0 copy_1 0 0 R R
start 2 0 copy_2 0 0 R R
copy_1 1 0 copy_1 1 1 R R
copy_1 2 0 copy_2 1 1 R R
copy_1 0 0 go_2nd_left 1 1 R S
copy_2 1 0 copy_1 2 2 R R
copy_2 2 0 copy_2 2 2 R R
copy_2 0 0 go_2nd_left 2 2 R S
go_2nd_left 0 1 go_2nd_left 0 1 S L
go_2nd_left 0 2 go_2nd_left 0 2 S L
go_2nd_left 0 0 check 0 0 L R
check 1 1 check 1 1 L R
check 2 2 check 2 2 L R
check 0 0 accept 0 0 S S