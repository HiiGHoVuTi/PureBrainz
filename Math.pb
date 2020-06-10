
#add(*a*b*c){
    *c $(-) $a(+) $b(+)
}
#addTo(*a*b){
    *b $a(+)
}

#sub(*a*b*c){
    *c $(-) $a(+) $b(-)
}
#subFrom(*a*b){
    *b $a(-)
}

#mult(*a*b*c){
    *c $(-) $a ($b (+))
}
#multBy(*a*b*t){
    *t $(-) $a(+) *a $(-)
    $t ($b (+))
    *t $(-) *a
}

#pow(*a*b*c*t){
    *c $(-) *t $(-)
    *a ?{
        *c +
        $b(
            *t $a($c(+))
            *c $(-) $t(+)
            *t $(-)
        )
    }
    *c
}

#greater(*a*b*c){
    *c $c(-) $a(+)
    $b(!{$(-)+}-)
    ?{$(-)+}
}