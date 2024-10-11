#Norah Swatland 
#CSE 30151 
#source code for project 1

import csv 
import argparse
from csv_reader import csv_to_wff_dict

def dpll(filename): 
    pass

if __name__ == "__main__": 
    #parse command line argument (containing file of wffs in cnf form) to be solved 
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    #read in wff from csv 
    with open(args.filename) as file: 
        CSV_data = list(csv.reader(file))
    problems = csv_to_wff_dict(CSV_data)
    for prob in problems:
        for key, list in prob.items(): 
            print(list)