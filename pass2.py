import os

class Pass2Assembler:
    def __init__(self):
        # Machine operation codes (from Pass 1 mnemonics)
        self.machine_ops = {
            'STOP': '00',
            'ADD': '01',
            'SUB': '02',
            'MUL': '03',
            'MOVER': '04',
            'MOVEM': '05',
            'COMP': '06',
            'BC': '07',
            'DIV': '08',
            'READ': '09',
            'PRINT': '10'
        }
        
        # Register codes (from Pass 1)
        self.registers = {
            'AREG': '1',
            'BREG': '2',
            'CREG': '3',
            'DREG': '4'
        }
        
        # Load tables created by Pass 1
        self.symtab = self.load_symbol_table()
        self.littab = self.load_literal_table()
        self.pooltab = self.load_pool_table()
        
    def load_symbol_table(self):
        symtab = {}
        with open("SymTab.txt", "r") as f:
            for line in f:
                symbol, address = line.strip().split('\t')
                symtab[symbol] = address
        return symtab
    
    def load_literal_table(self):
        littab = {}
        with open("literals.txt", "r") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    literal = parts[0]
                    address = parts[1] if parts[1] != "**" else "0"
                    # Extract the actual value from the literal (remove '=' and quotes)
                    value = literal.split('=')[1].strip("'")
                    littab[literal] = (value, address)
        return littab
    
    def load_pool_table(self):
        pooltab = []
        with open("PoolTab.txt", "r") as f:
            for line in f:
                pooltab.append(int(line.strip()))
        return pooltab
    
    def generate_machine_code(self):
        output_file = open("machine_code.txt", "w")
        ic_file = open("ic.txt", "r")
        
        for line in ic_file:
            if not line.strip():
                continue
                
            machine_code = ""
            parts = line.strip().split('\t')
            
            # Skip empty parts
            parts = [p for p in parts if p.strip()]
            
            # If line starts with location counter
            if parts[0].isdigit():
                machine_code += parts[0].zfill(4) + " "
                parts = parts[1:]
            
            for part in parts:
                part = part.strip("() ")
                if not part:
                    continue
                    
                tokens = part.split(",")
                tokens = [t.strip() for t in tokens]
                
                # Handle different types of tokens
                if tokens[0] == "IS":  # Imperative Statement
                    machine_code += tokens[1].zfill(2) + " "
                
                elif tokens[0] == "RG":  # Register
                    machine_code += tokens[1] + " "
                
                elif tokens[0] == "S":  # Symbol
                    symbol_key = next((s for s in self.symtab if str(self.symtab[s][1]) == tokens[1]), None)
                    if symbol_key:
                        machine_code += str(self.symtab[symbol_key][0]).zfill(4) + " "
                
                elif tokens[0] == "L":  # Literal
                    literal_idx = int(tokens[1]) - 1
                    literal_entry = list(self.littab.items())[literal_idx]
                    machine_code += literal_entry[1][1].zfill(4) + " "
                
                elif tokens[0] == "C":  # Constant
                    machine_code += tokens[1].zfill(4) + " "
                
                elif tokens[0] in ("AD", "DL"):  # Assembler Directive or Declaration
                    # Skip assembler directives in machine code
                    continue
            
            if machine_code.strip():
                output_file.write(machine_code.strip() + "\n")
        
        ic_file.close()
        output_file.close()
    
    def print_tables(self):
        print("\nSymbol Table:")
        for symbol, value in self.symtab.items():
            print(f"{symbol}: {value}")
            
        print("\nLiteral Table:")
        for literal, (value, address) in self.littab.items():
            print(f"{literal}: value={value}, address={address}")
            
        print("\nPool Table:")
        print(self.pooltab)

def main():
    # Create instance of Pass2Assembler
    assembler = Pass2Assembler()
    
    # Generate machine code
    assembler.generate_machine_code()
    
    print("Pass 2 assembly completed successfully!")
    print("Machine code has been written to 'machine_code.txt'")
    
    # Print the tables for verification
    assembler.print_tables()

if __name__ == "__main__":
    main()
