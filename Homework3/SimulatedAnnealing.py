# Only support finding maximum of linear equation now
# Support finding minimum in the near futuress

import random
import numpy as np
from math import sin, cos, pi, exp
import matplotlib.pyplot as plt

class OptimizeFunction:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = lambda x, y: 21.5 + x*sin(4*pi*x) + y*sin(20*pi*y)

    # Constraints
    def calculate(self):
        x, y = {random.uniform(-3,  12.1), random.uniform(4.1, 5.8)}
        result = {"x" : x, "y" : y, "result" : self.f(x, y)}
        return result

class Probability:
    def calculate(self, current_result, next_result, Temp):
        delta = next_result - current_result
        if(delta >= 0) :
            return 1
        else:
            return np.exp(delta / Temp)

class SimulateAnnealing:
    def __init__(self, Temp, min_Temp, cooling_rate, length, Function, Probability):
        self.Temp = Temp
        self.min_Temp = min_Temp
        self.cooling_rate = cooling_rate
        self.length = length
        self.Function = Function
        self.Probability = Probability
        
    def getSolution(self):
        iteration = []
        Temp = self.Temp
        min_Temp = self.min_Temp
        cooling_rate = self.cooling_rate
        length = self.length

        current_result = best_so_far = self.Function.calculate()
        best_so_far["Temp"] = Temp
        iteration.append(current_result["result"])

        while Temp > min_Temp:
            i = 0
            while i <= length:
                next_result = self.Function.calculate()
                iteration.append(next_result["result"])

                # Update the result
                if(next_result["result"] > current_result["result"]):
                    best_so_far = next_result
                    best_so_far["Temp"] = Temp
                    print("Best_so_far", best_so_far, "Temp", Temp)

                # Calculate the probabiltity of accept next state
                prob = self.Probability.calculate(current_result["result"], next_result["result"], Temp)
                if prob > random.random():
                    current_result = next_result
                i += 1

            Temp = Temp * cooling_rate
        return best_so_far, iteration


initial_x, initial_y = {random.uniform(-3,  12.1), random.uniform(4.1, 5.8)}
Temp = 100
Min_Temp = 1
Length = 100
Cooling_Rate = 0.99

optimizeFunction = OptimizeFunction(initial_x, initial_y)
sa = SimulateAnnealing(Temp, Min_Temp, Cooling_Rate, Length, optimizeFunction, Probability())
solution, result = sa.getSolution()
print("Best Solution")
print(solution)
print("length of iteration",len(result))

# Plot the iteration
plt.scatter(len(result), solution["result"], facecolor='r')
plt.annotate(s = 'x : [{:.6f}, {:.6f}]\ny : {:.6f}'.format(solution["x"], solution["y"], solution["result"]), xy = (len(result), solution["result"]))
plt.plot(range(len(result)),result)
plt.title("Simulated Annealing\n" + "Temp : " + str(Temp) + ", Min_Temp : " + str(Min_Temp) + ", Cooling Rate : " + str(Cooling_Rate))
plt.xlabel("Iteration")
plt.ylabel("Fitness")
plt.show()
