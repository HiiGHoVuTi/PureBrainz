
#print(*s){
    *s +[-.>+]-
}

#print_sep(*s*tmp){
    *tmp 32(+) *s +[-.#i*tmp.@i>+]- *tmp $(-)
}

#print_int(*s){
    *s +[-48(+).48(-)>+]-
}

#print_int_sep(*s*tmp){
    *tmp 32(+) *s +[-48(+).48(-)#i*tmp.@i>+]- *tmp $(-)
}

#print_lb(*tmp){
    *tmp $(-) 10(+) . $(-)
}

#rto(*x){
    *x ?{$(-)+}
}

#strint(*s){
    *s 48(-)
}

#intstr(*i){
    *i 48(+)
}

#listint(*l*e*i*tmp1){

}