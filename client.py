from connection import connect, get_state_reward
import math
import random as rd


### Parameters ###

SAVE = False # Enable save Q-table after execution 

## Problem parameters
PLATS = 24
DIRS = 4
ACTIONS = ['left', 'right', 'jump']
ITERATIONS = 12
MAXSTEPS = 180
QTABLEFILE = 'resultado' # resultado.txt

## Q-learning parameters ##
MIN_ALPHA = 0.1
ALPHA_DECRESE = 0.955
BASEALPHA = 0.8
BASEGAMMA = 0.4
DECAY_BASE = 0.785
MIN_EPSILON = 0.01

INIT_ITERATIONS = 30

### Problem Info's ###
# columns = actions_num = 3 (rotate left, rotate right, jump)
# rows = states_num = PLATFORMS * DIRECTIONS = 96
# states are 7bits binary: 5 for platform_num and 2 for direction
# 00 -> north; 01 -> east; 10 -> south; 11 -> west


## Helper Functions ##
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
    return max(MIN_ALPHA, BASEALPHA * ALPHA_DECRESE ** i)

def getGamma(i):
    return BASEGAMMA + 0.35 * math.log(1 + i) / math.log(1 + ITERATIONS)


def update_q_table(q_table, state, action, reward, next_state, i):
    alpha = getAlpha(i)
    gamma = getGamma(i)
    max_next_q = max(q_table[next_state])
    q_table[state][action] += alpha * (reward + gamma * max_next_q - q_table[state][action])
    
    
def choose_action(state, q_table, epsilon):
    action = q_table[state].index(max(q_table[state]))
    if rd.uniform(0, 1) < epsilon:
        action = min(rd.randint(0, len(ACTIONS)), 2)
    return action


### Algorithm Execution ###

q_table = read_q_table(QTABLEFILE+'.txt')

s = connect(2037)
if s == 0: exit(1)

state = 0 # init state
try:
    for i in range(ITERATIONS):
        i+= INIT_ITERATIONS
        print("It: ",(i+1))
        epsilon = max(DECAY_BASE ** i, MIN_EPSILON)
        print("epsilon, alpha, gamma:  ", epsilon, getAlpha(i), getGamma(i))
        for j in range(MAXSTEPS):
            action = choose_action(state, q_table, epsilon)
            new_state, reward = get_state_reward(s, ACTIONS[action])
            new_state = int(new_state, base=2)

            update_q_table(q_table, state, action, reward, new_state, i)
            state = new_state
            
    if SAVE:
        write_q_table(QTABLEFILE+f'.txt', q_table)
except KeyboardInterrupt:
    if SAVE:
        write_q_table(QTABLEFILE+f'_save.txt', q_table)


s.close()