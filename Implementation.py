#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP TL1: implémentation des automates
"""

import sys

###############
# Cadre général

V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

INPUT_STREAM = sys.stdin
END = '\n' # WARNING: test_tp modifies the value of END.

# Initialisation: on vérifie que END n'est pas dans V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Accès au caractère suivant dans l'entrée
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')


############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    assert (len(char) <= 1)
    return '1' <= char <= '9'

def digit(char):
    assert (len(char) <= 1)
    return '0' <= char <= '9'


############
# Question 2 : integer et pointfloat sans valeur

def integer_Q2():
    init_char()
    return integer_Q2_state_0()

def integer_Q2_state_0():
    ch = next_char()
    if nonzerodigit(ch):
        return integer_Q2_state_1()
    elif ch=='0':
        return integer_Q2_state_2()
    else:
        return False


def integer_Q2_state_1():
    ch = next_char()
    if digit(ch):
        return integer_Q2_state_1()
    elif ch==END:
        return True
    else:
        return False


def integer_Q2_state_2():
    ch = next_char()
    if ch=="0":
        return integer_Q2_state_2()
    elif ch==END:
        return True
    else:
        return False

def pointfloat_Q2():
    init_char()
    return pointfloat_Q2_state_0()

def pointfloat_Q2_state_0():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_1()
    elif ch=='.':
        return pointfloat_Q2_state_3()
    else:
        return False

def pointfloat_Q2_state_1():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_1()
    elif ch==".":
        return pointfloat_Q2_state_2()
    else:
        return False

def pointfloat_Q2_state_2():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    elif ch==END:
        return True
    else:
        return False

def pointfloat_Q2_state_3():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    else:
        return False
############
# Question 5 : integer avec calcul de la valeur
# si mot accepté, renvoyer (True, valeur)
# si mot refusé, renvoyer (False, None)

# Variables globales pour se transmettre les valeurs entre états
int_value = 0
exp_value = 0

def integer():
    init_char()
    return integer_state_0()


def integer_state_0():
    global int_value
    int_value=0
    ch = next_char()
    if nonzerodigit(ch):
        int_value= int_value*10 + int(ch)
        return integer_state_1()
    elif ch=='0':
        int_value= int_value*10 + int(ch)
        return integer_state_2()
    else:
        return False, None


def integer_state_1():
    global int_value
    ch = next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return integer_state_1()
    elif ch==END:
        return True, int_value
    else:
        return False, None

def integer_state_2():
    global int_value
    ch = next_char()
    if ch=="0":
        int_value= int_value*10 + int(ch)
        return integer_state_2()
    elif ch==END:
        return True, int_value
    else:
        return False, None

############
# Question 7 : pointfloat avec calcul de la valeur

def pointfloat():
    global int_value
    global exp_value
    init_char()
    int_value = 0
    exp_value = 0
    return pointfloat_state_0()

def pointfloat_state_0():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return pointfloat_state_1()
    elif ch=='.':
        return pointfloat_state_3()
    else:
        return False,None

def pointfloat_state_1():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return pointfloat_state_1()
    elif ch==".":
        return pointfloat_state_2()
    else:
        return False,None

def pointfloat_state_2():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        exp_value+=1
        return pointfloat_state_2()
    elif ch==END:
        return True,int_value*(10**(-exp_value))
    else:
        return False,None

def pointfloat_state_3():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        exp_value+=1
        return pointfloat_state_2()
    else:
        return False,None

############
# Question 8 : exponent, exponentfloat et number

# La valeur du signe de l'exposant : 1 si +, -1 si -
sign_value = 0
exponent_value=0
int_value=0

def exponent():
    global sign_value
    global exponent_value
    sign_value=0
    exponent_value=0
    init_char()
    return exponent_state_0()

def exponent_state_0():
    ch=next_char()
    if ch=='e' or ch=='E':
        return exponent_state_1()
    else:
        return False,None

def exponent_state_1():
    global sign_value
    global exponent_value
    ch=next_char()
    if ch=='+':
        sign_value+=1
        return exponent_state_2()
    elif ch=='-':
        sign_value-=1
        return exponent_state_2()
    elif digit(ch):
        sign_value+=1
        exponent_value+=int(ch)
        return exponent_state_3()
    else:
        return False,None

def exponent_state_2():
    global exponent_value
    ch=next_char()
    if digit(ch):
        exponent_value = exponent_value*10 + int(ch)
        return exponent_state_3()
    else:
        return False,None
    
def exponent_state_3():
    global exponent_value
    global sign_value
    ch=next_char()
    if digit(ch):
        exponent_value= exponent_value*10 + int(ch)
        return exponent_state_3()
    elif ch==END:
        return True, exponent_value*sign_value
    else:
        return False, None
## exponentfloat

def exponentfloat():
    global sign_value
    global expfloat_value
    global int_value
    global exponent_value
    sign_value=0
    int_value=0
    expfloat_value=0
    exponent_value=0
    init_char()
    return exponentfloat_state_0()

def exponentfloat_state_0():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value+=int(ch)
        return exponentfloat_state_1()
    elif ch=='.':
        return exponentfloat_state_6()
    else:
        return False,None

def exponentfloat_state_1():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return exponentfloat_state_1()
    elif ch=='e' or ch=='E':
        return exponentfloat_state_3()
    elif ch==".":
        return exponentfloat_state_2()
    else:
        return False,None

def exponentfloat_state_2():
    global int_value
    global exponent_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        exponent_value+=1
        return exponentfloat_state_2()
    elif ch=='e' or ch=='E':
        return exponentfloat_state_3()
    else:
        return False,None

def exponentfloat_state_3():
    global expfloat_value
    global sign_value
    ch=next_char()
    if ch=='+':
        sign_value+=1
        return exponentfloat_state_4()
    elif ch=='-':
        sign_value-=1
        return exponentfloat_state_4()
    elif digit(ch):
        sign_value+=1
        expfloat_value+=int(ch)
        return exponentfloat_state_5()
    else:
        return False,None

def exponentfloat_state_4():
    global expfloat_value
    ch=next_char()
    if digit(ch):
        expfloat_value +=int(ch)
        return exponentfloat_state_5()
    else:
        return False,None
    
def exponentfloat_state_5():
    global int_value
    global expfloat_value
    global sign_value
    global exponent_value
    ch=next_char()
    if digit(ch):
        expfloat_value= expfloat_value*10 + int(ch)
        return exponentfloat_state_5()
    elif ch==END:
        return True, int_value*(10**((sign_value)*expfloat_value))*10**(-exponent_value)
    else:
        return False, None

def exponentfloat_state_6():
    global int_value
    global exponent_value
    ch=next_char()
    if digit(ch):
        exponent_value+=1
        int_value= int_value*10 + int(ch)
        return exponentfloat_state_6()
    elif ch=='e' or 'E':
        return exponentfloat_state_3()
    else:
        return False,None
## number

def number():
    global sign_value
    global expfloat_value
    global int_value
    global exponent_value
    sign_value=0
    int_value=0
    expfloat_value=0
    exponent_value=0
    init_char()
    return number_state_0()

def number_state_0():
    global int_value
    ch=next_char()
    if ch=='0':
        return number_state_1()
    elif nonzerodigit(ch):
        int_value+=int(ch)
        return number_state_2()
    elif ch=='.':
        return number_state_3()
    else:
        return (False,None)

def number_state_1():
    global int_value
    ch=next_char()
    if ch=='0':
        return number_state_1()
    elif ch=='e' or ch=='E':
        return number_state_6()
    elif nonzerodigit(ch):
        int_value= int_value*10 + int(ch)
        return number_state_5()
    elif ch=='.':
        return number_state_4()
    elif ch==END or ch == ' ':
        return (True, int_value)
    else:
        return (False,None)

def number_state_2():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return number_state_2()
    elif ch=='.':
        return number_state_4()
    elif ch=='e' or ch=='E':
        return number_state_6()
    elif ch==END or ch == ' ':
        return (True,int_value)
    else:
        return (False,None)

def number_state_3():
    global expfloat_value
    global int_value
    ch=next_char()
    if digit(ch):
        expfloat_value+=1
        int_value= int_value*10 + int(ch)
        return number_state_4()
    else:
        return (False,None)
    
def number_state_4():
    global expfloat_value
    global int_value
    ch=next_char()
    if digit(ch):
        expfloat_value+=1
        int_value=int_value*10 + int(ch)
        return number_state_4()
    elif ch=='e' or ch=='E':
        return number_state_6()
    elif ch==END or ch == ' ':
        return (True,int_value*(10**(-expfloat_value)))
    else:
        return (False,None)

def number_state_5():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return number_state_5()
    elif ch=='e' or ch=='E':
        return number_state_6()
    elif ch=='.':
        return number_state_4()
    else:
        return (False,None)
    
def number_state_6():
    global sign_value
    global exponent_value
    ch=next_char()
    if ch=='+':
        sign_value+=1
        return number_state_7()
    elif ch=='-':
        sign_value-=1
        return number_state_7()
    elif digit(ch):
        sign_value+=1
        exponent_value= exponent_value*10+ int(ch)
        return number_state_8()
    else:
        return (False,None)

def number_state_7():
    global exponent_value
    ch=next_char()
    if digit(ch):
        exponent_value+=int(ch)
        return number_state_8()
    else:
        return (False,None)

def number_state_8():
    global sign_value
    global expfloat_value
    global int_value
    global exponent_value
    ch=next_char()
    if digit(ch):
        exponent_value= exponent_value*10 + int(ch)
        return number_state_8()
    elif ch==END or ch ==' ':
        return True,int_value*(10**((sign_value)*exponent_value))*10**(-expfloat_value)
    else:
        return False,None

########################
#####    Projet    #####
########################
V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
    + tuple(str(i) for i in range(10)))
############
# Question 10 : eval_exp

def eval_exp():
    ch = next_char()
    if ch == '+':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 + n2
    elif ch == '*':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 * n2
    elif ch == '-':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 - n2
    elif ch == '/':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 / n2
    else:
        return number()

############
# Question 12 : eval_exp corrigé

current_char = ''

# Accès au caractère suivant de l'entrée sans avancer
def peek_char():
    global current_char
    if current_char == '':
        current_char = INPUT_STREAM.read(1)
    ch = current_char
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch in END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

def consume_char():
    global current_char
    current_char = ''

def number_V2():
    global sign_value
    global expfloat_value
    global int_value
    global exponent_value
    sign_value=0
    int_value=0
    expfloat_value=0
    exponent_value=0
    init_char()
    return number_V2_state_0()

def number_V2_state_0():
    global int_value
    ch=next_char()
    if ch=='0':
        return number_V2_state_1()
    elif nonzerodigit(ch):
        int_value+=int(ch)
        return number_V2_state_2()
    elif ch=='.':
        return number_V2_state_3()
    else:
        return False,None

def number_V2_state_1():
    global int_value
    ch=next_char()
    if ch=='0':
        return number_V2_state_1()
    elif ch=='e' or ch=='E':
        return number_V2_state_6()
    elif nonzerodigit(ch):
        int_value= int_value*10 + int(ch)
        return number_V2_state_5()
    elif ch=='.':
        return number_V2_state_4()
    elif ch==END or ch == ' ':
        return int_value
    else:
        return False,None

def number_V2_state_2():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return number_V2_state_2()
    elif ch=='.':
        return number_V2_state_4()
    elif ch=='e' or ch=='E':
        return number_V2_state_6()
    elif ch==END or ch == ' ':
        return int_value
    else:
        return False,None

def number_V2_state_3():
    global int_value
    global exponent_value
    ch=next_char()
    if digit(ch):
        expfloat_value+=1
        int_value= int_value*10 + int(ch)
        return number_V2_state_4()
    else:
        return False,None
    
def number_V2_state_4():
    global expfloat_value
    global int_value
    ch=next_char()
    if digit(ch):
        expfloat_value+=1
        int_value=int_value*10 + int(ch)
        return number_V2_state_4()
    elif ch=='e' or ch=='E':
        return number_V2_state_6()
    elif ch==END or ch == ' ':
        return int_value*(10**(-expfloat_value))
    else:
        return False,None

def number_V2_state_5():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return number_V2_state_5()
    elif ch=='e' or ch=='E':
        return number_V2_state_6()
    elif ch=='.':
        return number_V2_state_4()
    else:
        return False,None
    
def number_V2_state_6():
    global sign_value
    global exponent_value
    ch=next_char()
    if ch=='+':
        sign_value+=1
        return number_V2_state_7()
    elif ch=='-':
        sign_value-=1
        return number_V2_state_7()
    elif digit(ch):
        sign_value+=1
        exponent_value= exponent_value*10+ int(ch)
        return number_V2_state_8()
    else:
        return False,None

def number_V2_state_7():
    global exponent_value
    ch=next_char()
    if digit(ch):
        exponent_value+=int(ch)
        return number_V2_state_8()
    else:
        return False,None

def number_V2_state_8():
    global expfloat_value
    global int_value
    global exponent_value
    global sign_value
    ch=next_char()
    if digit(ch):
        exponent_value= exponent_value*10 + int(ch)
        return number_V2_state_8()
    elif ch==END or ch ==' ':
        return int_value*(10**((sign_value)*exponent_value))*10**(-expfloat_value)
    else:
        return (False,None)


def eval_exp_v2():
    ch = peek_char()
    if ch!=' ':
        consume_char()
    if ch == '+':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 + n2
    elif ch == '*':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 * n2
    elif ch == '-':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 - n2
    elif ch == '/':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 / n2
    else:
        return number_V2()


############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])

def FA_Lex():
    init_char()
    return FA_Lex_state_0()

def FA_Lex_state_0():
    global operator
    ch=next_char()
    if ch in operator or ch=='(' or ch==')':
        if next_char()!=END:
            return False
        else:
            return True
    if ch=='0':
        return FA_Lex_state_1()
    elif nonzerodigit(ch):
        return FA_Lex_state_2()
    elif ch=='.':
        return FA_Lex_state_3()
    else:
        return False

def FA_Lex_state_1():
    ch=next_char()
    if ch=='0':
        return FA_Lex_state_1()
    elif ch=='e' or ch=='E':
        return FA_Lex_state_6()
    elif nonzerodigit(ch):
        return FA_Lex_state_5()
    elif ch=='.':
        return FA_Lex_state_4()
    elif ch==END:
        return True
    else:
        return False

def FA_Lex_state_2():
    ch=next_char()
    if digit(ch):
        return FA_Lex_state_2()
    elif ch=='.':
        return FA_Lex_state_4()
    elif ch=='e' or ch=='E':
        return FA_Lex_state_6()
    elif ch==END:
        return True
    else:
        return False

def FA_Lex_state_3():
    ch=next_char()
    if digit(ch):
        return FA_Lex_state_4()
    else:
        return False
    
def FA_Lex_state_4():
    ch=next_char()
    if digit(ch):
        return FA_Lex_state_4()
    elif ch=='e' or ch=='E':
        return FA_Lex_state_6()
    elif ch==END:
        return True
    else:
        return False

def FA_Lex_state_5():
    ch=next_char()
    if digit(ch):
        return FA_Lex_state_5()
    elif ch=='e' or ch=='E':
        return FA_Lex_state_6()
    elif ch=='.':
        return FA_Lex_state_4()
    else:
        return False
    
def FA_Lex_state_6():
    ch=next_char()
    if ch=='+':
        return FA_Lex_state_7()
    elif ch=='-':
        return FA_Lex_state_7()
    elif digit(ch):
        return FA_Lex_state_8()
    else:
        return False

def FA_Lex_state_7():
    ch=next_char()
    if digit(ch):
        return True
    else:
        return False

def FA_Lex_state_8():
    ch=next_char()
    if digit(ch):
        return FA_Lex_state_8()
    elif ch==END:
        return True
    else:
        return False

############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0


def ch_value(ch):
    if ch=='+':
        return (True,ADD)
    elif ch=='-':
        return (True,SOUS)
    elif ch=='*':
        return (True,MUL)
    elif ch=='/':
        return (True,DIV)
    elif ch=='(':
        return (True,OPAR)
    elif ch==')':
        return (True,FPAR)

def FA_Lex_w_token():
    init_char()
    return FA_Lex_w_token_state_0()

def FA_Lex_w_token_state_0():
    global sign_value
    global expfloat_value
    global int_value
    global exponent_value
    global operator
    sign_value=0
    int_value=0
    expfloat_value=0
    exponent_value=0
    ch=next_char()
    if ch in operator or ch=='(' or ch==')':
        return ch_value(ch)
    elif ch=='0':
        return FA_Lex_w_token_state_1()
    elif nonzerodigit(ch):
        int_value+=int(ch)
        return FA_Lex_w_token_state_2()
    elif ch=='.':
        return FA_Lex_w_token_state_3()
    else:
        return (False,None)

def FA_Lex_w_token_state_1():
    global int_value
    global token_value
    ch=next_char()
    if ch=='0':
        return FA_Lex_w_token_state_1()
    elif ch=='e' or ch=='E':
        return FA_Lex_w_token_state_6()
    elif nonzerodigit(ch):
        int_value= int_value*10 + int(ch)
        return FA_Lex_w_token_state_5()
    elif ch=='.':
        return FA_Lex_w_token_state_4()
    elif ch==END or ch==' ' or ch in operator or ch=='(' or ch==')':
        token_value=int_value
        return (True,NUM)
    else:
        return (False,None)

def FA_Lex_w_token_state_2():
    global int_value
    global token_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return FA_Lex_w_token_state_2()
    elif ch=='.':
        return FA_Lex_w_token_state_4()
    elif ch=='e' or ch=='E':
        return FA_Lex_w_token_state_6()
    elif ch==END or ch==' ' or ch in operator or ch=='(' or ch==')':
        token_value=int_value
        return (True,NUM)
    else:
        return (False,None)

def FA_Lex_w_token_state_3():
    global expfloat_value
    global int_value
    ch=next_char()
    if digit(ch):
        expfloat_value+=1
        int_value= int_value*10 + int(ch)
        return FA_Lex_w_token_state_4()
    else:
        return (False,None)
    
def FA_Lex_w_token_state_4():
    global expfloat_value
    global int_value
    global token_value
    ch=next_char()
    if digit(ch):
        expfloat_value+=1
        int_value=int_value*10 + int(ch)
        return FA_Lex_w_token_state_4()
    elif ch=='e' or ch=='E':
        return FA_Lex_w_token_state_6()
    elif ch==END or ch==' ' or ch in operator or ch=='(' or ch==')':
        token_value=int_value*(10**(-expfloat_value))
        return (True,NUM)
    else:
        return (False,None)

def FA_Lex_w_token_state_5():
    global int_value
    ch=next_char()
    if digit(ch):
        int_value= int_value*10 + int(ch)
        return FA_Lex_w_token_state_5()
    elif ch=='e' or ch=='E':
        return FA_Lex_w_token_state_6()
    elif ch=='.':
        return FA_Lex_w_token_state_4()
    else:
        return (False,None)
    
def FA_Lex_w_token_state_6():
    global sign_value
    global expfloat_value
    global exponent_value
    ch=next_char()
    if ch=='+':
        sign_value+=1
        return FA_Lex_w_token_state_7()
    elif ch=='-':
        sign_value-=1
        return FA_Lex_w_token_state_7()
    elif digit(ch):
        sign_value+=1
        exponent_value= exponent_value*10+ int(ch)
        return FA_Lex_w_token_state_8()
    else:
        return (False,None)

def FA_Lex_w_token_state_7():
    global exponent_value
    ch=next_char()
    if digit(ch):
        exponent_value+=int(ch)
        return FA_Lex_w_token_state_8()
    else:
        return (False,None)

def FA_Lex_w_token_state_8():
    global sign_value
    global expfloat_value
    global int_value
    global exponent_value
    global operator
    global token_value
    ch=next_char()
    if digit(ch):
        exponent_value= exponent_value*10 + int(ch)
        return FA_Lex_w_token_state_8()
    if ch==END or ch==' ' or ch in operator or ch=='(' or ch==')':
        token_value=int_value*(10**((sign_value)*exponent_value))*10**(-expfloat_value)
        return (True,NUM)
    else:
        return (False,None)

# Fonction de test
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        #ok = FA_Lex() # changer ici pour tester un autre automate sans valeur
        #ok, val = FA_Lex_w_token() # changer ici pour tester un autre automate avec valeur
        #ok, val =True, eval_exp() # changer ici pour tester eval_exp et eval_exp_v2
        if ok:
            print("Accepted!")
            print("value:",val) # décommenter ici pour afficher la valeur (question 4 et +)
        else:
            print("Rejected!")
            #print("value so far:",int_value)# décommenter ici pour afficher la valeur en cas de re
    except Error as e:
        print("Error:", e)