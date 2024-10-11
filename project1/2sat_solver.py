#Norah Swatland 
#CSE 30151 
#source code for project 1

import csv 
import argparse

def dppl(filename): 
    pass

def csv_to_wff_dict(csv_data): 
    list_of_probs = []
    total = 1
    for i in range(len(csv_data)):
        temp_dict = {}
        bigger_list = []
        if csv_data[i][0] == 'c': 
            #count initial input
            
            count=1
            while(total < len(csv_data) and csv_data[i+count][0] != 'c'):
                count += 1
                total += 1
            total += 1
            num_vars = csv_data[i][2]
            
            for j in range(2,count): 
                temp_list = []
                for k in range(int(num_vars)):
                    print(int(num_vars))
                    temp_list.append(csv_data[j][k])
                    print(csv_data[j][k])
                    print(' ')
                bigger_list.append(temp_list)
                temp_dict[csv_data[i][1]] = bigger_list
        list_of_probs.append(temp_dict)
    print(list_of_probs)


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
