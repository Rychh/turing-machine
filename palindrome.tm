start 1 golong1 0 R
start 2 golong2 0 R
start 0 accept 0 S
golong1 1 golong1 1 R
golong1 2 golong1 2 R
golong1 0 checklast1 0 L
golong2 1 golong2 1 R
golong2 2 golong2 2 R
golong2 0 checklast2 0 L
checklast1 1 goback 0 L
checklast1 0 accept 0 S
checklast2 2 goback 0 L
checklast2 0 accept 0 S
goback 1 goback 1 L
goback 2 goback 2 L
goback 0 start 0 R