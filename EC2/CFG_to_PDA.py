import csv
import argparse

class CFG_to_PDA:
    def __init__(self, cfg_file):
        self.cfg = self.read_cfg(cfg_file)
        self.pda = self.convert_to_pda()

    def read_cfg(self, cfg_file):
        cfg = {}
        with open(cfg_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header if there is one
            for row in reader:
                left, right = row[0], row[1]
                if left not in cfg:
                    cfg[left] = []
                cfg[left].append(right)
        return cfg

    def convert_to_pda(self):
        pda = {
            'states': set(self.cfg.keys()),  # States are the non-terminals
            'alphabet': set(),               # Alphabet will be the union of terminal symbols
            'stack_alphabet': set(self.cfg.keys()),  # Stack symbols are the non-terminals
            'transitions': [],
            'start_state': list(self.cfg.keys())[0],  # Pick the start non-terminal as start state
            'start_stack': [list(self.cfg.keys())[0]], # Start stack contains the start non-terminal
            'accept_states': ['accept']  # Accept state
        }

        # Add terminal symbols to the alphabet
        for productions in self.cfg.values():
            for production in productions:
                for symbol in production:
                    if symbol.islower():  # Terminals are lowercase
                        pda['alphabet'].add(symbol)
        
        # Generate transitions based on the CFG productions
        for state, productions in self.cfg.items():
            for production in productions:
                if production == 'ε':  # ε-productions, skip
                    continue
                # Create transition for each production rule
                for symbol in production:
                    if symbol.islower():  # If terminal, create a transition to consume the symbol
                        pda['transitions'].append(
                            (state, symbol, state, [symbol])
                        )
                    else:  # Non-terminal, replace with the right-hand side (push to the stack)
                        pda['transitions'].append(
                            (state, '', state, [symbol])
                        )
        return pda

    def display_pda(self):
        print("States:", self.pda['states'])
        print("Alphabet:", self.pda['alphabet'])
        print("Stack Alphabet:", self.pda['stack_alphabet'])
        print("Start State:", self.pda['start_state'])
        print("Start Stack:", self.pda['start_stack'])
        print("Accept States:", self.pda['accept_states'])
        print("Transitions:")
        for transition in self.pda['transitions']:
            print(transition)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    cfg_to_pda = CFG_to_PDA(args.filename)
    cfg_to_pda.display_pda()