#Aqui vocês irão colocar seu algoritmo de aprendizado
from email.charset import BASE64
from connection import connect, get_state_reward
import math
import random as rd

PLATS = 24
DIRS = 4
ACTIONS = ['left', 'right', 'jump']
ITERATIONS = 10
MAXSTEPS = 100
QTABLEFILE = 'test.txt' # resultado.txt

BASEALPHA = 0.05
BASEGAMMA = 0.95


### Problem Info's
# columns = actions_num = 3 (rotate left, rotate right, jump)
# rows = states_num = PLATFORMS * DIRECTIONS = 96
# states are 7bits binary: 5 for platform_num and 2 for direction
# 00 -> north; 01 -> east; 10 -> south; 11 -> west


def read_q_table(filename):
    q_table = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                actions_values = line.split()
                q_table.append([float(value) for value in actions_values])
    except FileNotFoundError:
        pass
    return q_table

def write_q_table(filename, q_table):
    with open(filename, 'w') as file:
        for state_values in q_table:
            file.write(' '.join(map(str, state_values)) + "\n")

def getAlpha(i):
    return max(BASEALPHA, BASEALPHA * (1 - i / ITERATIONS))

def getGamma(i):
    return min(BASEGAMMA, 0.6 + BASEGAMMA * (i / ITERATIONS))

def update_q_table(q_table, state, action, reward, next_state, i):
    alpha = getAlpha(i)
    gamma = getGamma(i)
    max_next_q = max(q_table[next_state])
    q_table[state][action] += alpha * (reward + gamma * max_next_q - q_table[state][action])
    
    

def choose_action(state, q_table, epsilon):
    
    q_table[state] = [q / sum(q_table[state]) for q in q_table[state]]
    if rd.uniform(0, sum(q_table[state])) < epsilon:
        action = rd.randint(0, len(ACTIONS) - 1)
    else:
        action = q_table[state].index(max(q_table[state]))
    return action



q_table = read_q_table(QTABLEFILE)

s = connect(2037)
if s == 0: exit(1)

state = 0 # init state
for i in range(ITERATIONS):
    print("It: ",(i+1))
    for j in range(MAXSTEPS):
        epsilon = 1 / ((i + 1) * 5)
        action = choose_action(state, q_table, epsilon)
        new_state, reward = get_state_reward(s, ACTIONS[action])
        new_state = int(new_state, base=2)

        update_q_table(q_table, state, action, reward, new_state, i)
        state = new_state
    print("Final epsilon:  ", epsilon)

write_q_table(QTABLEFILE, q_table)
s.close()