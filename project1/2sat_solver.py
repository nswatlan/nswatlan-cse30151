#Norah Swatland 
#CSE 30151 
#source code for project 1 



import csv 
import argparse

def dppl(filename): 
    pass

def csv_to_wff_dict(csv_data): 
    list_of_probs = []
    count  = 0
    for i in range(len(csv_data)):
        if csv_data[i][0] == 'c': 
            print(count)
            print(f"{csv_data[i]}")
            print(count)
            count = 0
        else:
            count += 1 



if __name__ == "__main__": 
    #parse command line argument (containing file of wffs in cnf form) to be solved 
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    #read in wff from csv 
    with open(args.filename) as file: 
        CSV_data = list(csv.reader(file))
        print(len(CSV_data))
    csv_to_wff_dict(CSV_data)
