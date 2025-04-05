#Aqui vocês irão colocar seu algoritmo de aprendizado
from connection import connect, get_state_reward
import math
import random as rd

PLATNUM = 24
DIRNUM = 4
ACTIONS = {'l': 'left', 'r': 'right', 'j': 'jump'}
ITERATIONS = 10
QTABLEFILE = 'test.txt' # resultado.txt

def read_q_table(filename):
    q_table = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                state, action, value = line.strip().split()
                q_table[(int(state), action)] = float(value)
    except FileNotFoundError:
        pass
    return q_table

def write_q_table(filename, q_table):
    with open(filename, 'w') as file:
        for (state, action), value in q_table.items():
            file.write(f"{state} {action} {value}\n")



s = connect(2037)



