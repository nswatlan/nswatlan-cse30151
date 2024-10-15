#Norah Swatland 
#CSE 30151 
#source code for project 1

import csv 
import argparse
from csv_reader_nswat import csv_to_wff_dict

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


if __name__ == "__main__": 
    #parse command line argument (containing file of wffs in cnf form) to be solved 
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    #read in wff from csv 
    with open(args.filename) as file: 
        CSV_data = list(csv.reader(file))
    problems = csv_to_wff_dict(CSV_data)
    for problem in problems: 
        for number, clauses in problem.items(): 
            if DPLL(clauses): 
                print(f"Problem {number}: Satisfiable")
            else: 
                print(f"Problem {number}: Unsatisfiable")
    