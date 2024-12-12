#traceTM_nswat.py
#Norah Swatland
import csv
import argparse
from collections import deque

def load_turing_machine(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        name = next(reader)[0]
        states = next(reader)[0].split(',')
        input_alphabet = next(reader)[0].split(',')
        tape_alphabet = next(reader)[0].split(',')
        start_state = next(reader)[0]
        accept_state = next(reader)[0]
        reject_state = next(reader)[0]
        
        transitions = {}
        for line in reader:
            state, symbol, next_state, write_symbol, direction = line
            transitions.setdefault((state, symbol), []).append((next_state, write_symbol, direction))
    
    return {
        "name": name,
        "states": states,
        "start": start_state,
        "accept": accept_state,
        "reject": reject_state,
        "transitions": transitions
    }

def simulate_ntm(tm, input_string, max_depth=100):
    start_config = ["", tm["start"], input_string]
    tree = [[start_config]]
    queue = deque([start_config])
    depth = 0
    
    while queue and depth < max_depth:
        next_level = []
        for _ in range(len(queue)):
            tape_left, state, tape_right = queue.popleft()
            if state == tm["accept"]:
                print("String accepted!")
                return tree
            if state == tm["reject"]:
                continue
            
            head_symbol = tape_right[0] if tape_right else "_"
            transitions = tm["transitions"].get((state, head_symbol), [])
            
            for next_state, write_symbol, direction in transitions:
                new_tape_left = tape_left
                new_tape_right = tape_right
                if direction == "R":
                    new_tape_left += write_symbol
                    new_tape_right = new_tape_right[1:] if len(new_tape_right) > 1 else "_"
                elif direction == "L":
                    new_tape_right = head_symbol + new_tape_right
                    new_tape_left = new_tape_left[:-1] if new_tape_left else "_"
                
                new_config = [new_tape_left, next_state, new_tape_right]
                next_level.append(new_config)
                queue.append(new_config)
        
        if next_level:
            tree.append(next_level)
        depth += 1
    
    print("String rejected or step limit reached.")
    return tree

if __name__ == "__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("string", type=str)
    args = parser.parse_args()

    #formatted output
    print("Language: ", args.filename)
    print("Input String: ", args.string)

    tm = load_turing_machine(args.filename)
    simulate_ntm(tm, args.string)
