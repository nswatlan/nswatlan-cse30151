#Norah Swatland 
#CSE 30151 
#source code for project 1

import csv 
import argparse
from csv_reader_nswat import csv_to_wff_dict
import matplotlib.pyplot as plt 
import time 
from scipy.optimize import curve_fit 
import numpy as np

def DPLL(clauses): #takes in list of the form [[],[],[]]} where inner lists are clauses of literals 
    #base cases
    if len(clauses) == 0: #satisfiable
        return True
    elif [] in clauses: #unsatisfiable
        return False
    #unit propagation
    unit_clause = find_unit_clause(clauses)
    if unit_clause is not None: 
        return DPLL(unit_propagate(unit_clause[0], clauses))
    #pure literal elimination 
    pure_literals = find_pure_literals(clauses)
    if len(pure_literals) > 0: 
         return DPLL(pure_literal_assign(pure_literals[0], clauses))
    #choose literal 
    literal = choose_literal(clauses)
    if DPLL(unit_propagate(literal, clauses)): #test for original assignment (for chosen literal)
        return True
    return DPLL(unit_propagate(-literal, clauses)) #test for opposite assignment 

def find_unit_clause(clauses): 
    for clause in clauses: 
        if len(clause) == 1: 
            return clause
    return None

def unit_propagate(literal, clauses): 
    new_wff = []
    for clause in clauses: 
        if literal in clause:
            continue #clause is satisfied
        new_clause = [l for l in clause if l != -literal] #remove negation of current literal
        new_wff.append(new_clause)
    return new_wff

def find_pure_literals(clauses): 
    all_literals = set(lit for clause in clauses for lit in clause) #use set so no literals are repeated
    pure_literals = []
    for literal in all_literals: 
        if -literal not in all_literals:  #append if negation is not present (def of pure literal)
            pure_literals.append(literal) 
    return pure_literals

def pure_literal_assign(literal, clauses):
    return unit_propagate(literal, clauses)

def choose_literal(clauses): 
    #choose first literal (clauses is modified as alg goes on)
    return clauses[0][0]

def exp_func(x, a, b):
    return a * np.exp(b * x)

if __name__ == "__main__": 
    #parse command line argument (containing file of wffs in cnf form) to be solved 
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    #read in wff from csv 
    with open(args.filename) as file: 
        CSV_data = list(csv.reader(file))
    problems = csv_to_wff_dict(CSV_data)

    input_sizes = []            #lists for execution time plots 
    satisfiable_times = []
    unsatisfiable_times = []

    for problem in problems: 
        for number, clauses in problem.items(): 
            start_time = time.time()
            input_sizes.append(len(clauses))
            if DPLL(clauses): 
                print(f"Problem {number}: Satisfiable")
                satisfiable_times.append(time.time() - start_time)
                unsatisfiable_times.append(None)
            else: 
                print(f"Problem {number}: Unsatisfiable")
                unsatisfiable_times.append(time.time() - start_time)
                satisfiable_times.append(None)

    satisfiable_times = [t if t is not None else 0 for t in satisfiable_times]
    unsatisfiable_times = [t if t is not None else 0 for t in unsatisfiable_times]

    x_fit = np.linspace(min(input_sizes), max(input_sizes), 100)

    if len(satisfiable_times) > 0 and len(input_sizes) > 0:
        # Fit the exponential curve for satisfiable times
        params_satisfiable, _ = curve_fit(exp_func, input_sizes, satisfiable_times, p0=(1, 0.01))

    if len(unsatisfiable_times) > 0 and len(input_sizes) > 0:
        # Fit the exponential curve for unsatisfiable times
        params_unsatisfiable, _ = curve_fit(exp_func, input_sizes, unsatisfiable_times, p0=(1, 0.01))

    plt.scatter(input_sizes, satisfiable_times, color='green', label='Satisfiable')
    plt.scatter(input_sizes, unsatisfiable_times, color='red', label='Unsatisfiable' )

    if len(satisfiable_times) > 0:
        y_fit_satisfiable = exp_func(x_fit, *params_satisfiable)
        plt.plot(x_fit, y_fit_satisfiable, color='blue', label='Fitted Curve (Satisfiable)')
        a, b = params_satisfiable
        equation_satisfiable = f'y = {a:.2f} * e^({b:.2f} * x)'
        plt.text(0.05 * max(input_sizes), 0.8 * max(satisfiable_times), equation_satisfiable, color='blue')

    if len(unsatisfiable_times) > 0:
        y_fit_unsatisfiable = exp_func(x_fit, *params_unsatisfiable)
        plt.plot(x_fit, y_fit_unsatisfiable, color='orange', label='Fitted Curve (Unsatisfiable)')
        a, b = params_unsatisfiable
        equation_unsatisfiable = f'y = {a:.2f} * e^({b:.2f} * x)'
        plt.text(0.05 * max(input_sizes), 0.7 * max(unsatisfiable_times), equation_unsatisfiable, color='orange')

    plt.xlabel('Input Size (Number of Variables)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs Input Size for kSAT Solver')
    plt.legend()
    plt.savefig('execution_time_graph.png')