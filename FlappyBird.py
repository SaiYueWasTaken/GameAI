from os import stat
from turtle import st
import gym
import numpy as np
import math as mh
from collections import defaultdict
import random
import matplotlib.pyplot as plt
import pickle
import time
import flappy_bird_gym



q_table = dict()
learningRate = 0.1
gamma = 0.95
epsilon_initial = 0.1
epsilon_min = 0.01
render = 500

num_episodes = 200000
reward_history = []
epsilon_step_size = 1/num_episodes
score_history = []

env = flappy_bird_gym.make("FlappyBird-v0")


def factory():
    return [0, 0]

q_function = defaultdict(factory)

def descretize(obs):
    new_obs = [round(obs[0], 2), round(obs[1], 2)]

    return tuple(new_obs)


    


def update_epsilon(epsilon):
    return(max(epsilon_min, min(epsilon_initial, epsilon - epsilon_step_size)))

epsilon = epsilon_initial
for i in range(num_episodes):
    state = env.reset()
    state = descretize(state)


    done = False
    score = 0

    while not done:
        if (random.random() < epsilon):
            action = env.action_space.sample()
        else:
            if (q_function[state][0] == q_function[state][1]):
                action = env.action_space.sample()
            
            else:
                print(q_function[state])
                action = np.argmax(q_function[state])
        
        next_state, reward, done, _ = env.step(action)
        if (abs(next_state[1])>0.1):
            reward += -10000
        next_state = descretize(next_state)



        epsilon = update_epsilon(epsilon)

        #Update q_function
        q_function[state][action] = q_function[state][action]+learningRate*(reward + gamma + max(q_function[next_state])-q_function[state][action])
        
        state = next_state
        score += reward
        if (i%render == 0):
            env.render()
            time.sleep(1 / 30)  # FPS
    
    reward_history.append(score)
    



