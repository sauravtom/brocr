#!/usr/local/bin/python
# encoding: UTF-8

postfix = []
temp = []
decimal=[0,1,2,3,4,5,6,7,8,9]
operator = -10
operand = -20
leftpar = -30
rightpar = -40
empty = -50
 
def precedence(s):
    if s is '(':
        return 0
    elif s is '+' or s is '-':
        return 1
    elif s is '*' or s is '/' or s is '%':
        return 2
    else:
        return 99
                 
def typeof(s):
    if s is '(':
        return leftpar
    elif s is ')':
        return rightpar
    elif s is '+' or s is '-' or s is '*' or s is '%' or s is '/':
        return operator
    elif s is ' ':
        return empty   
    else :
        return operand     


def postfixEval(postfixExpr):
    operandStack = []
    for token in postfixExpr:
        if token in decimal :
            operandStack.append(int(token))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = doMath(token,operand1,operand2)
            operandStack.append(result)
    return operandStack.pop()

def doMath(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2

 
def makepostfix(infix) : 
    for i in infix :
        type = typeof(i)
        if type is leftpar :
            temp.append(i)
        elif type is rightpar :
            next = temp.pop()
            while next is not '(':
                postfix.append(next)
                next = temp.pop()
        elif type is operand:
            postfix.append(int(i))
        elif type is operator:
            p = precedence(i)
            while len(temp) is not 0 and p <= precedence(temp[-1]) :
                postfix.append(temp.pop())
            temp.append(i)
        elif type is empty:
            continue
                 
    while len(temp) > 0 :
        postfix.append(temp.pop())
  








