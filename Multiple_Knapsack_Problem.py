import sys
import pandas as pd
import time, numpy as np
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

#Parameters
v = np.array([10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]) # v_i

w = np.array([48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]) # w_i

C = np.array([100, 100, 100, 100, 100]) # C_j 

n = len(w) # Number of items
m = len(C) # Number of bins

range_i = range(0,n)
range_j = range(0,m)


#Create Model
model = pyo.ConcreteModel()

#Define variables
model.x = pyo.Var(range(n), # index i
                  range(m), # index j
                  within=Binary)

x = model.x

model.C1 = pyo.ConstraintList() 
for j in range_j:
    model.C1.add(expr = sum(w[i]*x[i,j] for i in range_i)  <= C[j])

model.C2 = pyo.ConstraintList() 
for i in range_i:
    model.C2.add(expr = sum(x[i,j] for j in range_j) <= 1)
    
    
    
# Define Objective Function
model.obj = pyo.Objective(expr = sum(x[i,j]*v[i] for i in range_i for j in range_j), 
                          sense = maximize)       
    
begin = time.time()
opt = SolverFactory('cplex')
results = opt.solve(model)

deltaT = time.time() - begin # Compute Exection Duration

model.pprint()

sys.stdout = open("Multiple_Knapsack_Problem_Results.txt", "w") #Print Results on a .txt file

print('Time =', np.round(deltaT,2))

if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):

    print('Total Packed Value (Obj value) =', pyo.value(model.obj))
    print('Solver Status is =', results.solver.status)
    print('Termination Condition is =', results.solver.termination_condition)
    print(" " )
    totalWeight = 0
    for j in range_j:
        bin_weight = 0
        bin_Value = 0
        print("Bin ", j)
        for i in range_i:
          if pyo.value(x[i, j]) == 1:
              print('Item:  ' ,i, ' - weight: ', w[i],' value: ', v[i])
              bin_weight += w[i]
              bin_Value += v[i]
        print("Packed bin weight: " , bin_weight)
        print("Packed bin value: " , bin_Value)
        print(" " )
        totalWeight += bin_weight   
    print("Total packed weight: " , totalWeight)
elif (results.solver.termination_condition == TerminationCondition.infeasible):
   print('Model is unfeasible')
  #print('Solver Status is =', results.solver.status)
   print('Termination Condition is =', results.solver.termination_condition)
else:
    # Something else is wrong
    print ('Solver Status: ',  result.solver.status)
    print('Termination Condition is =', results.solver.termination_condition)
    
sys.stdout.close()
 
