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
 
def optimizing_function(ctr, x, y):
    '''
    Setting the optimizing function
    '''
    result = 21.5 + x*np.sin(4*np.pi*x) + y*np.sin(20*np.pi*y)
    return {"ctr" : ctr, "x": x, "y" : y, "result" : result}

def HillClimbing(x, y, threshold):
    '''
    Implement Hill Climbing

    Returns:
        iteration: record every trials that have been explored
        best_iteration: record the trails that have improved the value
    '''
    ctr = 1
    iteration = []
    best_iteration = []

    # Random Start
    current_state = optimizing_function(ctr, x, y)
    iteration.append(current_state)
    best_iteration.append(current_state)

    # Start explore the neighbor of the point
    while ctr <= threshold:
        while not check_constraints(x, y):
            new_x, new_y = random_move(x, y)
            if check_constraints(new_x, new_y): 
                x, y = new_x, new_y
                break
            
        next_state = optimizing_function(ctr, x, y)
        iteration.append(next_state)

        # Update the best_so_far if the value is improved
        if next_state["result"] > current_state["result"]:
            best_iteration.append(next_state)
            print("Best_so_far", next_state)
            current_state = next_state
        
        # Try another neighbor
        x, y = random_move(x, y)
        ctr += 1
    return best_iteration, iteration

# Main Function
## Random start at the point in the constraint area
initial_x, initial_y = {random.uniform(-3,  12.1), random.uniform(4.1, 5.8)}
threshold = 10000
best_solution, iteration = HillClimbing(initial_x, initial_y, threshold)
print("Best Solution : ", best_solution[-1]["result"])

# Plot the iteration and best_iteration
plt.plot(range(len(iteration)), [item['result'] for item in iteration], label = "Trials")
plt.plot([item['ctr'] for item in best_solution], [item['result'] for item in best_solution], '.r-', label = "Best_so_far")
plt.annotate(s = 'x : [{:.6f}, {:.6f}]\ny : {:.6f}'.format(best_solution[-1]["x"], best_solution[-1]["y"], best_solution[-1]["result"]), xy = (best_solution[-1]["ctr"], best_solution[-1]["result"]), xytext=(best_solution[-1]["ctr"], best_solution[-1]["result"]-3))
plt.title("Hill Climbing")
plt.legend(loc='lower right')
plt.show()

