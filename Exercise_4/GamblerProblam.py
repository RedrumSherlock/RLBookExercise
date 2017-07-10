import numpy as np
import matplotlib.pyplot as plt

goal = 100
p_h = 0.25

V = np.zeros(goal + 1) # Value 0,1,2,..,goal
V[goal] = 1.0

pi = np.zeros(goal + 1) # Policy

thres = np.exp(-100)

def new_value(s, action):
    return p_h * V[int(min(s + action, goal))] + (1 - p_h) * V[int(max(s - action, 0))]


while True:
    delta = 0
    for i in range(1, goal):
#       we only go through 1 to 99 since V(0) and V(100) are fixed
        max_action_value = -1
        temp = V[i]
        for action in range(0, int(min(i, goal - i)) + 1) :
            new_v = new_value(i, action)
            if new_v > max_action_value:
                max_action_value = new_v
        V[i] = max_action_value
        delta = max(delta, np.absolute(temp - V[i]))
    print delta
    if delta < thres:
        break


for i in range(1, goal):
    max_action_value = -99999
    max_action = -1
    for action in range(1, int(min(i, goal - i)) + 1):
        new_v = new_value(i, action)
        if new_v > max_action_value:
            max_action_value = new_v
            max_action = action
    pi[i] = max_action

print V
print pi

plt.plot(range(1, goal), V[range(1, goal)], label='Value')    
plt.legend()
plt.ylabel('Value Estimates')    
plt.xlabel('Capital')
plt.show()

plt.plot(range(1, goal), pi[range(1, goal)], label='Policy')
plt.legend()
plt.ylabel('Final Policy')
plt.xlabel('Capital')
plt.show()

