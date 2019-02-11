# Propositional Logic

## Description
This project is used to build a parser for logic language. The tokens are as follows:

- ID = [A-Z]+
- LAPR = (
- RPAR = )
- NOT = !
- AND = /\
- OR = \\/
- IMPLIES = ‘=>’
- IFF = ‘<=>’

The grammar is the following:

- propositions -> proposition more-proposition
- more-proposition -> , propositions | e
- proposition -> atomic | compound
- atomic -> 0 | 1 | ID
- compound -> atomic connective proposition | LPAR proposition RPAR | NOT proposition
- connective -> AND | OR | IMPLIES | IFF

## Structure

- lexer.py builds tokens consumed by parser.py
- parser.py builds syntax tree in prefix order
- main.py initiates the program using an input file


### LICENSE
This code is for educational/demonstration purposes only! Copying of this code is strictly prohibited!
