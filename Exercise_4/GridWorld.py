import numpy as np

V = np.zeros((5,4))
temp = np.zeros((5,4))
max_step = 1000

def v_action(i, j, action):
    if (i == 0 and j == 0) or (i == 3 and j == 3):
        return 0
    elif (i == 4 and j == 1 and action == 'left'):
        return V[3, 0]
    elif (i == 4 and j == 1 and action == 'right'):
        return V[3, 2]
    elif (i == 4 and j == 1 and action == 'up'):
        return V[3, 1]
    elif (i == 0 and action == 'up') or (i == 3 and action == 'down') or \
    (j == 0 and action == 'left') or (j == 3 and action == 'right') or \
    (i == 4 and j == 1 and action == 'down'):
        return V[i,j]
    elif action == 'up':
        return V[i-1, j]
    elif action == 'down':
        return V[i+1, j]
    elif action == 'left':
        return V[i, j-1]
    elif action == 'right':
        return V[i, j+1]
    else:
        return -99999
        

for k in range(max_step):
    for i in range(5):
        for j in range(4):
            if (i == 4 and j == 1) or not ( ( i == 0 and j == 0) or (i == 3 and j == 3) or i == 4):
                temp[i,j] = 0.25 * (-1 + v_action(i,j, 'up')) + 0.25 * (-1 + v_action(i,j,'down')) \
                 + 0.25 * (-1 + v_action(i,j,'left')) + 0.25 * (-1 + v_action(i,j,'right'))
    V = temp.copy()
    print V


