'''
Created on Jul 14, 2017

@author: mwang
'''
from RaceTrack import RaceTrack
from matplotlib import pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

if __name__ == '__main__':
    
    RaceTest = RaceTrack(
        max_velocity = 5, 
        step_reward = -1,
        gamma = 1, 
        stop_prob = 0.1)
    
    # Draw Field
    fig = plt.figure()
    plt.imshow(RaceTest.field, interpolation='nearest')
    #plt.show()
    

    max_steps = 100
    ite = 0
    
    for i in range(max_steps):
        ite = ite + 1
        print(ite)
        seq = RaceTest.generate_episode(True)
        G = 0
        W = 1
        while len(seq) > 0:
            G = seq.pop() + RaceTest.gamma * G
            action = tuple(seq.pop())
            state = tuple(seq.pop())
            pair = state + action
            
            if pair in RaceTest.C:
                RaceTest.C[pair] =  RaceTest.C[pair] + W
            else:
                RaceTest.C[pair] = W
                
            if pair in RaceTest.Q:
                RaceTest.Q[pair] =  RaceTest.Q[pair] + W * (G - RaceTest.Q[pair]) / RaceTest.C[pair]
            else:
                RaceTest.Q[pair] = W * G / RaceTest.C[pair]
                
            RaceTest.max_pi(state)
            
            if RaceTest.pi[state] != action:
                break;
            
            choices = RaceTest.possible_actions(state)
            assert(len(choices) > 0)
            W = W * len(choices)
    
    
    seq = RaceTest.generate_episode(False)
    
    # Draw car driving path
    show_steps = 100
    destination = seq.pop()
    verts = [(destination[1], destination[0])]
    while len(seq) > 0:
        seq.pop()
        seq.pop()
        state = seq.pop()
        verts.append((state[1], state[0]))
    
    path = Path(verts)
    print verts
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor='none', lw=2)
    ax.add_patch(patch)
    ax.set_xlim(0, RaceTest.width + 1)
    ax.set_ylim(RaceTest.height + 1, 0)
    plt.show()