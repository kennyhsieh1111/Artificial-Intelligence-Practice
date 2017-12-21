# Using Hill Climbing Algorithm(HC) to find the maximum value of the specific function in the constraint area. 
import random
import numpy as np
import matplotlib.pyplot as plt

def random_move(x, y):
    ''' 
    Random move around the current point
    '''
    x = (random.uniform(0.0001, 0.9999) - 0.5) * 0.1 + x
    y = (random.uniform(0.0001, 0.9999) - 0.5) * 0.1 + y
    return x, y

def check_constraints(x, y):
    '''
    Check whether the points are located in the constraints or not
    '''
    return True if -3 <= x <= 12.1 and 4.1 <= y <= 5.8 else False
 
def optimizing_function(x, y, temp, length, outctr):
    '''
    Setting the optimizing function
    '''
    result = 21.5 + x*np.sin(4*np.pi*x) + y*np.sin(20*np.pi*y)
    return {"outctr" : outctr, "x": x, "y" : y, "temp" : temp, "length" : length, "result" : result}

def boltzman_probability(next_result, current_result, temp):
    dE = next_result - current_result
    if dE >= 0:
        prob = 1
    else:
        prob = np.exp(-dE / temp)
    return prob

def SimulatedAnnealing(x, y, temp, minTemp, coolingRate, length):
    '''
    Implement SimulatedAnnealing

    Returns:
        iteration: record every trials that have been explored
        best_iteration: record the trails that have improved the value
    '''

    ctr = 1
    out_ctr = 1

    iteration = []
    best_iteration = []

    current_state = optimizing_function(x, y, temp, 1, out_ctr)
    iteration.append(current_state)
    best_iteration.append(current_state)
    best_result = best_iteration[-1]["result"]

    while minTemp < temp:
        while ctr <= length:
            while not check_constraints(x, y):
                new_x, new_y = random_move(x, y)
                if check_constraints(new_x, new_y): 
                    x, y = new_x, new_y
                    break
            
            next_state = optimizing_function(x, y, temp, ctr, out_ctr)
            iteration.append(next_state)

            prob = boltzman_probability(next_state["result"], current_state["result"], temp)
            prob_accept = random.choice([1] * int(prob*100) + [0] * int(100 - (prob*100)))
            if prob == 1 or prob_accept == 1:
                if next_state["result"] > best_result:
                    best_iteration.append(next_state) 
                    best_result = best_iteration[-1]["result"]
                    print("Best_so_far", next_state)
                current_state = next_state
                
            x, y = random_move(x, y)
            ctr += 1
            out_ctr += 1
        ctr = 1
        temp = temp * coolingRate

    return best_iteration, iteration

# Main Function
## Random start at the point in the constraint area
initial_x, initial_y = {random.uniform(-3,  12.1), random.uniform(4.1, 5.8)}
temp = 100
minTemp = 1
coolingRate = 0.99
length = 100
best_solution, iteration = SimulatedAnnealing(initial_x, initial_y, temp, minTemp, coolingRate, length)

#print(iteration)
print("Best Solution : ", best_solution[-1]["result"])

plt.plot(range(len(iteration)), [item['result'] for item in iteration], label = "Trials")
plt.plot([item['outctr'] for item in best_solution], [item['result'] for item in best_solution], '.r-', label = "Best_so_far")
plt.annotate(s = 'x : [{:.6f}, {:.6f}]\ny : {:.6f}'.format(best_solution[-1]["x"], best_solution[-1]["y"], best_solution[-1]["result"]), xy = (best_solution[-1]["outctr"], best_solution[-1]["result"]), xytext=(best_solution[-1]["outctr"], best_solution[-1]["result"]-3))
plt.title("Simulated Annealing")
plt.legend(loc='lower right')
plt.show()