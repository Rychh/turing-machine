start 1 0 golong1 0 0 R S
start 2 0 golong2 0 0 R S
start 0 0 accept 0 0 S S
golong1 1 0 golong1 1 0 R S
golong1 2 0 golong1 2 0 R S
golong1 0 0 checklast1 0 0 L S
golong2 1 0 golong2 1 0 R S
golong2 2 0 golong2 2 0 R S
golong2 0 0 checklast2 0 0 L S
checklast1 1 0 goback 0 0 L S
checklast1 0 0 accept 0 0 S S
checklast2 2 0 goback 0 0 L S
checklast2 0 0 accept 0 0 S S
goback 1 0 goback 1 0 L S
goback 2 0 goback 2 0 L S
goback 0 0 start 0 0 R R