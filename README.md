# Prototipo_Compilador

Compilador simples para uma linguagem semelhante ao Pascal (basicamente um pascal adaptado)

## Gramatica base

Prog -> inicio Coms fim.
Coms -> LAMBDA | Com Coms
Com -> Ler | Escrever | If | Atrib | Bloco
Ler -> leia ( string, ident ) ;
Escrever -> escreva ( string, ident ) ;
| escreva ( string ) ;
If -> if ( Exp ) Com else Com
| if ( Exp ) Com
Bloco -> { Coms }
Atrib -> ident = Exp ;

Exp -> Exp and Nao | Exp or Nao | Nao
Nao -> not Nao | Rel
Rel -> Soma opRel Soma | Soma
Soma -> Soma + Mult | Soma - Mult | Mult
Mult -> Mult \* Uno | Mult / Uno | Mult % Uno | Uno
Uno -> + Uno | - Uno | Folha
Folha -> num | ident | ( Exp )
