grammar db_grammar;

script : (stmt ';')* EOF ;

stmt
    : CONNECT '"' STRING '"'
    | SELECT obj_expr FROM graph
    | DEF STRING ':' pattern
    ;

graph
    : gr
    | gr INTERSECT graph
    ;

gr
    : GRAMMAR
    | QUERY pattern
    | NAME '"' STRING '"'
    | '(' graph ')'
    | SET_START_AND_FINAL '(' vertices ';' vertices ')' graph
    ;

pattern
    : ct_pattern ALT pattern
    | ct_pattern
    ;

ct_pattern
    : pt CONCAT ct_pattern
    | pt
    ;

pt
    : pt OPT
    | pt PLUS
    | pt STAR
    | value
    | '(' pattern ')'
    | E
    ;

value
    : TERM '(' STRING ')'
    | NONTERM '(' STRING ')'
    ;

vertices
    : SET '(' lst ')'
    | RANGE INT ',' INT
    | NONE
    ;

lst : (INT ',')* INT ;

obj_expr
    : edges
    | COUNT edges
    ;

edges
    : EDGES
    | FILTER edges WITH predicate
    ;

predicate : '(' vert ',' edge ',' vert')' SATISFIES bool_expr
;


bool_expr
    : bool_and OR bool_expr
    | bool_and
    ;

bool_and
    : bl AND bool_and
    | bl
    ;

bl : NOT bool_term | bool_term ;

bool_term
    : edge LABEL_IS STRING
    | IS_START  vert
    | IS_FINAL  vert
    | '(' bool_expr ')'
    ;

vert : (INT | STRING)+ ;

edge : (INT | STRING)+ ;

/*
 * lexer
 */

GRAMMAR : 'grammar' ;
SELECT : 'select' ;
CONNECT : 'connect' ;
DEF : 'def' ;
FROM : 'from' ;
QUERY : 'query' ;
NAME : 'name' ;
TERM : 'term' ;
NONTERM : 'nonterm' ;
INTERSECT : 'intersect' ;
NONE : 'none' ;
RANGE : 'range' ;
SET : 'set' ;
SET_START_AND_FINAL : 'setStartAndFinal' ;
OF : 'of' ;
NOT : 'not' ;
AND : 'and' ;
OR : 'or' ;
LABEL_IS : 'labelIs' ;
IS_START : 'isStart' ;
IS_FINAL : 'isFinal' ;
CONCAT : '.' | 'concat' ;
ALT : '|' | 'alt' ;
COUNT : 'count' ;
EDGES : 'edges' ;
FILTER : 'filter' ;
WITH : 'with' ;
SATISFIES : 'satisfies' ;
OPT : 'opt' | '?' ;
PLUS : 'plus' | '+' ;
STAR : 'star' | '*' ;
E : 'eps' ;

fragment LOWERCASE : [a-z] ;
fragment UPPERCASE : [A-Z] ;
fragment DIGIT : [0-9] ;

INT : '0' | [1-9] DIGIT* ;
STRING : (LOWERCASE | UPPERCASE | '_' | '/') (LOWERCASE | UPPERCASE | DIGIT | '/' | '.' | '_')* ;
WS : [ \t\r\n]+ -> skip ;