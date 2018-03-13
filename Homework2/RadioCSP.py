# Artificial Intelligence Hw2 - Constraints Satisfaction Problem
# B036060017 Kenny Hsieh

import sys
from collections import OrderedDict
from pprint import pprint
import os

unassignedStates = []
Frequency = ['A', 'B', 'C', 'D']
tmpFreq = Frequency[:]
ctrBacktrack = 0
constState = [] 
constFreq = [] 

# Load the US 50 states information
AllStates = []
with open('adjacent-states','r') as f:
    for line in f:
        AllStates.append(line.split(None, 1)[0]) 

# Load the neighbor of each states
neighbors = {}
with open('adjacent-states', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        line = line.split(' ')
        neighbors.update({line[0]: line[1:]})

# Construct a dictionary to store the State as key and it's frequency as value
AssignedFreuency = {}  
 

# Function : Check whether there is same frequency between neighbors or not
def IsValidFrequency(state, frequency):
    for neighbor in neighbors.get(state): 
        frequency_of_neighbor = AssignedFreuency.get(neighbor)  
        if frequency_of_neighbor == frequency:
            return False
    return True

# Function : Assign the frequency to state
def Assign_frequency(state):
    for frequency in Frequency:
        if (IsValidFrequency(state, frequency) == True):
            return frequency

# Function : Backtracking
def backtrack(state):
    global ctrBacktrack
    ctrBacktrack += 1    
    for neighbor in neighbors.get(state):
        tmpFreq.remove(AssignedFreuency[neighbor])  
        for freq in tmpFreq:
            if (IsValidFrequency(neighbor, freq) == True):
                tmpFreq.append(freq)
                return freq
        break
               
def main():
    constState = []
    constFreq = []
    ConstrainFileInput=sys.argv[1]

    # Read the external constraint file
    if os.stat(ConstrainFileInput).st_size <= 1:
        print("Empty Constrains")
    else:
        with open(ConstrainFileInput,'r') as f1:
            for line in f1:
                constState.append(line.split(None, 1)[0])
                constFreq.append(line.split(None)[1])
    
    # Sort the states according to the numbers of it's neighbor
    orderedState = OrderedDict(sorted(neighbors.items(), key=lambda x: len(x[1])))
    unassignedStates = orderedState.keys()
    
    # Allocate the frequency based on the constraint file
    for i in range(0, len(constState)):        
        AssignedFreuency[constState[i]] = constFreq[i]
        unassignedStates.remove(constState[i])
    
    # Assign frequency to each state, using Backtracking to reallocate if the dead end occur
    for state in reversed(unassignedStates):      
        AssignedFreuency[state] = Assign_frequency(state)
        if AssignedFreuency[state] is None:
            AssignedFreuency[state]=backtrack(state)
    return AssignedFreuency


# Print out the solution
AssignedFreuency = main()
for key, value in AssignedFreuency.iteritems() :
    print key, value
print "Number of backtracks:", ctrBacktrack

