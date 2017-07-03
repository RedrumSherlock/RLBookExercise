# Exercise 2.3 implementation:
# Design and conduct an experiment to demonstrate the difficulties that sample-average methods have for nonstationary problems. Use a
# modified version of the 10-armed testbed in which all the q_*(a) start out equal and then take independent random walks. Prepare plots like Figure 2.2 for an actionvalue
# method using sample averages, incrementally computed by alpha = 1/n, and another
# action-value method using a constant step-size parameter, alpha = 0.1. Use epsilon = 0:1 and, if necessary, runs longer than 1000 steps.

import numpy as np
import matplotlib.pyplot as plt

num_bandits = 10 # number of bandits

bandit_means = [] # list of the bandit mean values. Initialized to be all zero. 
bandit_var = 1 # the bandit distribution variance

walk_mean = 0.0 # the mean value for the random walks on bandit q_*(a)
walk_var = 0.1 # the variance for the random walks on bandit q_*(a)

epsilon = 0.1
alpha = 0.1

Q_Value_1 = [] # Q for each action calculated based on approach 1, i.e. average reward
Q_Value_2 = [] # Q for each action calculated based on approach 2, i.e. constant aplha
Num_Action = [] # N for each action

max_steps = 2000
Avg_Reward_1 = [] # Reward for approach 1
Avg_Reward_2 = [] # Reward for approach 2
Opt_Action_1 = [] # Optimal Action Percentage for approach 1
Opt_Action_2 = [] # optimal Action Percentage for approach 2

total_opt_actions_1 = 0.0
total_opt_actions_2 = 0.0

# Action on a bandit k. Return a award drawn from the bandit distribution
def action_bandit(bandit):
    return np.random.normal(bandit_means[bandit], bandit_var)

# Find the maximum action. Return the index of bandit that gives the maximum aciton. Take a chance of epsilon to do exploration
def max_action(approach):
    sample = np.random.uniform()
    if sample > epsilon:
        # Exploitation
        if approach == 'SA':
            # Sample Average Approach
            return Q_Value_1.index(max(Q_Value_1))
        else:
            # Constant-Alpha Approach
            return Q_Value_2.index(max(Q_Value_2))
    else:
        #Exploration
        return np.random.random_integers(0, num_bandits - 1)
        


# Update the mean values for the bandit based on a random value
def shift_means():
    for i in range(0, num_bandits):
        bandit_means[i] = bandit_means[i] + np.random.normal(walk_mean, walk_var)
    return

def init():
    for i in range(0, num_bandits):
        bandit_means.append(0)
        # bandit_means.append(np.random.normal(0, 1))
    for i in range(0, num_bandits):
        Q_Value_1.append(0)
    for i in range(0, num_bandits):
        Q_Value_2.append(0)
    for i in range(0, num_bandits):
        Num_Action.append(0)
    return


# Beginning of the main program        
init()

for t in range(0, max_steps):
    shift_means()
    k1 = max_action('SA') # Sample-Average Approach
    k2 = max_action('CA') # Constant-Alpha Approach
    R1 = action_bandit(k1)
    R2 = action_bandit(k2)
    Num_Action[k1] = Num_Action[k1] + 1

    Q_Value_1[k1] = Q_Value_1[k1] + 1/Num_Action[k1]*(R1 - Q_Value_1[k1])
    Q_Value_2[k2] = Q_Value_2[k2] + alpha*(R2 - Q_Value_2[k2])

    if t == 0:
        Avg_Reward_1.append(R1)
        Avg_Reward_2.append(R2)
    else:
        Avg_Reward_1.append(( Avg_Reward_1[t-1] * t + R1) / (t+1))
        Avg_Reward_2.append(( Avg_Reward_2[t-1] * t + R2) / (t+1))

    if k1 == bandit_means.index(max(bandit_means)):
        total_opt_actions_1 = total_opt_actions_1 + 1
    if k2 == bandit_means.index(max(bandit_means)):
        total_opt_actions_2 = total_opt_actions_2 + 1
    print(k2, bandit_means.index(max(bandit_means)), total_opt_actions_2)
    Opt_Action_1.append(total_opt_actions_1 / (t+1))
    Opt_Action_2.append(total_opt_actions_2 / (t+1))

plt.plot(range(0, max_steps), Avg_Reward_1, label='Sample-Average Approach')    
plt.plot(range(0, max_steps), Avg_Reward_2, label='Constant-Alpha Approach')
plt.legend()
plt.ylabel('Average Reward')    
plt.xlabel('Steps')
plt.show()


plt.plot(range(0, max_steps), Opt_Action_1, label='Sample-Average Approach')
plt.plot(range(0, max_steps), Opt_Action_2, label='Constant-Alpha Approach')
plt.legend()
plt.ylabel('% Optimal Action')    
plt.xlabel('Steps')
axes = plt.gca()
axes.set_ylim([0.0,1.0])
plt.show()

#print(Opt_Action_1)
#print(Opt_Action_2)
# print(Avg_Reward_1)    
