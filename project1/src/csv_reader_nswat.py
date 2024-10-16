#csv_reader.py
# Function to read in input CNF file 
import re 

def csv_to_wff_dict(csv_data): 
    list_of_probs = []
    count_literals = {}
    total = 1
    for i in range(len(csv_data)):
        temp_dict = {}
        bigger_list = []
        if re.findall(r'c', csv_data[i][0]):  # i keeps track of all comment lines in csv (#of problems)
            count=1
            while(i+count < len(csv_data) and csv_data[i+count][0] != 'c'): #count the number of clauses
                count += 1
                total += 1
            total += 1
            num_vars = int(csv_data[i][2])
            num_literals = int(csv_data[i+1][2])
            for j in range(2,count):        #iterate through clauses (not including c, p lines)
                temp_list = list(map(int,(csv_data[j+i][:num_vars]))) #put the two variable values for a clause into a list
                bigger_list.append(temp_list)        #add to bigger list of all clauses to be anded together
            temp_dict[csv_data[i][1]] = bigger_list    #the list of all the wff corresponds to the problem number 
            count_literals[csv_data[i][1]] = num_literals
        if len(temp_dict) > 0:          #skip if empty dictionary
            list_of_probs.append(temp_dict)
        
    return list_of_probs, count_literals

if __name__ == "__main__": 
    print("why are you running this separately")