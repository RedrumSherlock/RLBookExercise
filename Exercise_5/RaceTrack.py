'''
Created on Jul 14, 2017

@author: mwang
'''
import numpy as np
import random

class RaceTrack(object):
    '''
    classdocs
    '''


    def __init__(self, max_velocity, step_reward, gamma, stop_prob):
        '''
        Constructor
        '''
        self.max_velocity = max_velocity
        self.step_reward = step_reward
        self.stop_prob = stop_prob
        self.gamma = gamma
        
        self.width = 18
        self.height = 30
        self.create_field(self.width, self.height)
        
        self.Q = {}
        self.C = {}
        self.pi = {}
        
        self.actions_ver = range(-1, 2)
        self.actions_hor = range(-1, 2)
        
    def create_field(self, width, height):
        # Use custom field for now
        
        self.field = np.zeros((height, width))
        self.field[:height-4, 6:12] = 1
        self.field[height-11:height-4, 6:width - 1] = 1
        self.field[height-11:height-4, width - 1] = 2 # Destination
        self.field[5:height-5, 5] = 1
        self.field[10:height-6, 4] = 1
        self.field[15:height-7, 3] = 1
        self.field[20:height-8, 2] = 1
    
    def possible_actions(self, state):
        possible_action = []
        [velocity_ver, velocity_hor] = [state[2], state[3]]
        for i in self.actions_ver:
            for j in self.actions_hor:
                if (velocity_ver + i) >=0 and (velocity_hor + j) >= 0 and (velocity_ver + i) <= self.max_velocity \
                and (velocity_hor + j) <= self.max_velocity and (velocity_ver + i + velocity_hor + j) > 0:
                    possible_action.append([i, j])
        return possible_action            
                    
    def behaviour_policy(self, state):
        # Here we use equiprobable policy
        return random.choice(self.possible_actions(state))
    
    def target_policy(self, state):
        # Here we use target policy - evaluation only
        if tuple(state) in self.pi:
            return list(self.pi[tuple(state)])
        else:
            return self.behaviour_policy(state)
        
    
    def start_state(self):
        start = np.random.choice(np.ravel(np.where(self.field[0, :] == 1)))
        return (0, start, 0, 0)
        
    def transition(self, state, action, Training):
        
        not_working = np.random.random()
        if not Training or not_working > self.stop_prob:
            [velocity_ver, velocity_hor] = np.add(state[2:4], action)
        else:
            [velocity_ver, velocity_hor] = state[2:4]
            
        new_state = [state[0] + velocity_ver, state[1] + velocity_hor, velocity_ver, velocity_hor]
        
        if new_state[0] >= self.height or new_state[1] >= self.width or self.field[new_state[0], new_state[1]] == 0:
            new_state = self.start_state()
            return [self.step_reward, new_state]
        else:
            for i in range(state[0], new_state[0] + 1):
                for j in range(state[1], new_state[1] + 1):
                    if self.field[i, j] == 0:
                        new_state = self.start_state()
                        return [self.step_reward, new_state]
            return [self.step_reward, new_state]
            
        

    def is_terminal(self, state):
        return self.field[state[0], state[1]] == 2
            
    def generate_episode(self, training):
        seq = []
        state = self.start_state()
        seq.append(state)
        if training:
            action = self.behaviour_policy(state)
        else:
            action = self.target_policy(state)
        seq.append(action)
        [reward, next_state] = self.transition(state, action, training)
        seq.append(reward)
        
        while not self.is_terminal(next_state):
            state = next_state
            seq.append(state)
            if training:
                action = self.behaviour_policy(state)
            else:
                action = self.target_policy(state)
            seq.append(action)
            [reward, next_state] = self.transition(state, action, training)
            seq.append(reward)
            
        if not training:
            seq.append(next_state)
        return seq
    
    def max_pi(self, state):
        max_value = float("-inf")
        for action in self.possible_actions(state):
            if (state + tuple(action)) in self.Q and self.Q[state + tuple(action)] > max_value:
                max_value = self.Q[state + tuple(action)]
                self.pi[state] = tuple(action)
    