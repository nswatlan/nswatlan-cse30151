from collections import deque
import argparse
import csv


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
    # Start with the initial configuration
    start_config = ["", tm["start"], input_string]
    tree = [[start_config]]  # Tree to trace all configurations
    queue = deque([start_config])  # BFS queue
    depth = 0
    
    while queue and depth < max_depth:
        next_level = []  # Store configurations for the next depth level
        
        for _ in range(len(queue)):
            tape_left, state, tape_right = queue.popleft()
            
            # Check for accept or reject
            if state == tm["accept"]:
                print(f"String accepted at depth {depth}!")
                print_path(tree, state)
                return tree
            if state == tm["reject"]:
                continue
            
            # Read the symbol under the tape head
            head_symbol = tape_right[0] if tape_right else "_"
            transitions = tm["transitions"].get((state, head_symbol), [])
            
            # Process each possible transition
            for next_state, write_symbol, direction in transitions:
                new_tape_left = tape_left
                new_tape_right = tape_right
                
                # Handle tape writing and movement
                if direction == "R":  # Move right
                    new_tape_left += write_symbol
                    new_tape_right = tape_right[1:] if len(tape_right) > 1 else "_"
                elif direction == "L":  # Move left
                    new_tape_right = write_symbol + tape_right
                    new_tape_left = tape_left[:-1] if tape_left else "_"
                
                # Handle blanks correctly
                if new_tape_left == "_":
                    new_tape_left = ""
                if new_tape_right == "_":
                    new_tape_right = ""
                
                # Create a new configuration
                new_config = [new_tape_left, next_state, new_tape_right]
                next_level.append(new_config)
                queue.append(new_config)
        
        if next_level:
            tree.append(next_level)
        depth += 1
    
    print("String rejected or step limit reached.")
    return tree

def print_path(tree, accept_state):
    print("Trace to acceptance:")
    for level in tree:
        for config in level:
            if config[1] == accept_state:
                print(f"Config: {config}")

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
