#Norah Swatland 
#CSE 30151 
#source code for project 1 



import csv 
import argparse

def dppl(filename): 
    pass

if __name__ == "__main__": 
    #parse command line argument (containing file of wffs in cnf form) to be solved 
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    print(args.filename)
