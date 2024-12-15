#NFA TO DFA script

import csv
import argparse
from collections import deque, defaultdict


def parse_nfa_csv(csv_file):
    nfa = {
        "start": None,
        "accept": set(),
        "transitions": defaultdict(lambda: defaultdict(set))
    }

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            state = row["state"]
            input_symbol = row["input"] if row["input"] else "ε"  # Treat blank as epsilon
            next_state = row["next_state"]

            # Identify start state
            if row["start"].lower() == "yes":
                nfa["start"] = state
            
            # Identify accept states
            if row["accept"].lower() == "yes":
                nfa["accept"].add(state)
            
            # Add transitions
            nfa["transitions"][state][input_symbol].add(next_state)
    
    return nfa

def epsilon_closure(nfa, states):
    """ Compute the epsilon closure for a set of states in the NFA. """
    closure = set(states)
    stack = list(states)
    
    while stack:
        state = stack.pop()
        for next_state in nfa["transitions"][state].get("ε", []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def nfa_to_dfa(nfa):
    """ Convert an NFA to its equivalent DFA. """
    dfa = {
        "start": frozenset(epsilon_closure(nfa, {nfa["start"]})),
        "accept": set(),
        "transitions": {}
    }
    queue = deque([dfa["start"]])
    visited = set()

    while queue:
        current_states = queue.popleft()
        if current_states in visited:
            continue
        visited.add(current_states)

        # Check if any state in the current set is an accept state
        if any(state in nfa["accept"] for state in current_states):
            dfa["accept"].add(current_states)

        dfa["transitions"][current_states] = {}

        # Find all possible input symbols (excluding epsilon)
        input_symbols = set()
        for state in current_states:
            input_symbols.update(nfa["transitions"][state].keys())
        input_symbols.discard("ε")

        # Process transitions for each input symbol
        for input_symbol in input_symbols:
            next_states = set()
            for state in current_states:
                next_states.update(nfa["transitions"][state].get(input_symbol, []))
            
            # Compute the epsilon closure of the next states
            next_states_closure = frozenset(epsilon_closure(nfa, next_states))
            dfa["transitions"][current_states][input_symbol] = next_states_closure

            if next_states_closure not in visited:
                queue.append(next_states_closure)
    
    return dfa

def print_dfa(dfa):
    print("DFA Start State:", set(dfa["start"]))
    print("DFA Accept States:", [set(state) for state in dfa["accept"]])
    print("\nDFA Transitions:")
    for state, transitions in dfa["transitions"].items():
        for symbol, next_state in transitions.items():
            print(f"{set(state)} --({symbol})--> {set(next_state)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    nfa = parse_nfa_csv(args.filename)
    print("NFA Parsed Successfully:")
    print("Start State:", nfa["start"])
    print("Accept States:", nfa["accept"])
    print("\nNFA Transitions:")
    for state, transitions in nfa["transitions"].items():
        for input_symbol, next_states in transitions.items():
            print(f"{state} --({input_symbol})--> {next_states}")
    
    print("\nConverting NFA to DFA...\n")
    dfa = nfa_to_dfa(nfa)
    print_dfa(dfa)