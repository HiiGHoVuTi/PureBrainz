
#true(*x){
    *x $(-) +
}

#false(*x){
    *x $(-)
}

#makenot(*x){
    *x ? {$ (-)-} +
}

#not(*x*y){
    *y $(-) $x(+) ? {$ (-)-} +
}

#or(*a*b*y){
    *y $(-)
    $a(+) $b(+) ?{$(-)+}
}

#and(*a*b*y){
    *y $(-)
    *a ?{*b ?{*y+}}
}

#equals(*a*b*c){
    *c $(-) $a(+) $b(-)
    :makenot(*c)
}