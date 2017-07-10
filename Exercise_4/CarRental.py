import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


# Parameter initialization
car_income = 10
car_move_cost = -2
req1_lambda = 3
req2_lambda = 4
ret1_lambda = 3
ret2_lambda = 2
max_cars_loc = 10
max_cars_mov = 5
max_overnight = 5
cost_parking = 4
gamma = 0.9
V = np.zeros((max_cars_loc + 1, max_cars_loc + 1)) # value matrix, from 0 to max_cars_loc inclusive
PI = np.zeros((max_cars_loc + 1, max_cars_loc + 1)) # policy mapping matrix
thres = 0.01

def pos_dist(n, lamb):
    return np.power(lamb, n) * np.exp(-lamb) / np.math.factorial(n)

def new_value(i, j, action):
    new_v = 0
    total_p = 0
    sum_req1 = 0
    total_p = 0

    chargable_action = 0
    if action >= 1:
        chargable_action = action - 1
    else:
        chargable_action = -action

    for req1 in range(i - action + 1): # request in location 1, maximum to be the current available 
        
        if req1 == i - action:
            p_req1 = 1 - sum_req1
        else:                                                           
            p_req1 = pos_dist(req1, req1_lambda)
        sum_req1 = sum_req1 + p_req1

        sum_req2 = 0

        for req2 in range(j + action + 1): # request in location 2, maximum to be the current available
            if req2 == j + action:
                p_req2 = 1 - sum_req2
            else:
                p_req2 = pos_dist(req2, req2_lambda)
            sum_req2 = sum_req2 + p_req2

            sum_ret1 = 0

            for ret1 in range(max_cars_loc - i + action + req1 + 1): # return in location 1, return + current + transferred - request < max_loc
                if ret1 == max_cars_loc - i + action + req1:
                    p_ret1 = 1 - sum_ret1
                else:
                    p_ret1 = pos_dist(ret1, ret1_lambda)
                sum_ret1 = sum_ret1 + p_ret1

                sum_ret2 = 0

                for ret2 in range(max_cars_loc - j - action + req2 + 1): # return in location 2                                             
                    if ret2 == max_cars_loc - j - action + req2:
                        p_ret2 = 1 - sum_ret2
                    else:
                        p_ret2 = pos_dist(ret2, ret2_lambda)
                    sum_ret2 = sum_ret2 + p_ret2                                        
                    new_v = new_v + p_req1 * p_req2 * p_ret1 * p_ret2 * (car_move_cost * chargable_action + car_income * (req1 + req2) + \
                            cost_parking * (max(i - max_overnight, 0) + max(j - max_overnight, 0)) + \
                            gamma * V[ int(min(max(0, i - action - req1 + ret1), max_cars_loc)), int(min(max(0, j + action - req2 + ret2), max_cars_loc))])
#    print i, j, 'total_p', total_p                                                                  
    return new_v                                                   

 
policy_iter = 0    
while True:
    value_iter = 0
    delta = 1
    policy_stable = True

    while delta > thres:
        delta = 0
        for i in range(max_cars_loc + 1):
            for j in range(max_cars_loc + 1):
                # Here we are at state S
#               print 'processing(', i, ',', j, ')'
                temp_v = V[i, j]
                V[i, j] = new_value(i, j, int(PI[i, j]))
                delta = max(delta, np.absolute(V[i, j] - temp_v))
        value_iter = value_iter + 1
        print value_iter
        print delta

#   policy evaluation completed, now update the policy    
    for i in range(max_cars_loc + 1):
        for j in range(max_cars_loc + 1):
            max_action = 0
            max_q_value = -99999
            for k in range(-max_cars_mov, max_cars_mov + 1):
#           iterate through all the actions
                temp = new_value(i, j, k)
                if temp > max_q_value:
                    max_action = k
                    max_q_value = temp
            if PI[i, j] != max_action:
                policy_stable = False
            PI[i, j] = max_action

    policy_iter = policy_iter + 1
    print 'policy #', policy_iter
    print V
    print PI
    if policy_stable:
        break


fig = plt.figure()
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(range(max_cars_loc + 1), range(max_cars_loc + 1))
surf = ax.plot_surface(X, Y, V, cmap=cm.coolwarm, linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()    

fig = plt.figure()
CS = plt.contour(X, Y, PI, levels = [0,1])
plt.clabel(CS, inline=1, fontsize=10)
plt.show()    
