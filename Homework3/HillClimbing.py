import random
import numpy as np
import matplotlib.pyplot as plt

def random_move(x, y):
   x = random.uniform(-3,  12.1)
   y = random.uniform(4.1, 5.8)
   return x, y

def check_constraints(x, y):
    return True if -3 <= x <= 12.1 and 4.1 <= y <= 5.8 else False
 
def optimizing_function(x, y):
    result = 21.5 + x*np.sin(4*np.pi*x) + y*np.sin(20*np.pi*y)
    return {"x": x, "y" : y, "result" : result}

def HillClimbing(x, y, threshold, Function):
    ctr = 1
    iteration = []
    result = []
    current_state = best_so_far = optimizing_function(x, y)
    iteration.append(current_state)

    while ctr <= threshold:
        while not check_constraints(x, y):
            x, y = random_move(x, y)

        next_state = optimizing_function(x, y)
        iteration.append(next_state)
        result.append(next_state["result"])

        if next_state["result"] > current_state["result"]:
            current_state = best_so_far = next_state
            print("Best_so_far", best_so_far)
            
        x, y = random_move(x, y)
        ctr += 1
    return best_so_far, iteration, result

initial_x, initial_y = {random.uniform(-3,  12.1), random.uniform(4.1, 5.8)}
solution, result, z = HillClimbing(initial_x, initial_y, 1000, optimizing_function)
print("Solution : ", solution["result"])

# Plot the iteration 
plt.plot(range(1, len(result)), result)
plt.title("Hill Climbing")
plt.xlabel("Iteration")
plt.ylabel("Fitness")
plt.show()

