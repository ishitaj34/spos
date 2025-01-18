import os

lc = 0      # to initailise location counter

mnemonics = {'STOP': ('00', 'IS', 0), 'ADD': ('01', 'IS', 2), 'SUB': ('02', 'IS', 2), 'MUL': ('03', 'IS', 2),
             'MOVER': ('04', 'IS', 2), 'MOVEM': ('05', 'IS', 2), 'COMP': ('06', 'IS', 2), 'BC': ('07', 'IS', 2),
             'DIV': ('08', 'IS', 2), 'READ': ('09', 'IS', 1), 'PRINT': ('10', 'IS', 1), 'LTORG': ('05', 'AD', 0),
             'ORIGIN': ('03', 'AD', 1), 'START': ('01', 'AD', 1), 'EQU': ('04', 'AD', 2), 'DS': ('01', 'DL', 1),
             'DC': ('02', 'DL', 1), 'END': ('AD', 0)}

file = open("input.txt")

opf = open("ic.txt", "a")       # output file having intermediate code
opf.truncate(0)                 # cleaning file to remove previous data

reg = {'AREG': 1, 'BREG': 2, 'CREG': 3, 'DREG': 4} 

lit = open("literals.txt", "a+")        # file containing literals and their addresses
lit.truncate(0)

tmp = open("tmp.txt", "a+")
tmp.truncate(0)

symtab = {}  
pooltab = [] 
words = []

def littab():
    print("Literal table: ")
    lit.seek(0, 0)
    for x in lit:
        print(x)

def pooltab2():
    global pooltab
    print("Pool table: ", pooltab)

def symbol():
    global symtab
    print("Symbol table:")
    print(symtab, "\n")
    
# handles END directive
def END():
    global lc
    pool = 0
    z = 0
    
    opf.write("\t (AD,02) \n")
    lit.seek(0, 0)
    
    for x in lit:
        if "**" in x:
            pool += 1
            if pool == 1:
                pooltab.append(z)
            y = x.split()
            tmp.write(y[0] + "\t" + str(lc) + "\n")
            lc += 1
            
        else:
            tmp.write(x)
            
        z += 1
        
    lit.truncate(0)
    tmp.seek(0, 0)
    
    for x in tmp:
        lit.write(x)
    tmp.truncate(0)

# handles LTORG mnemonic
def LTORG():
    global lc
    pool = 0
    z = 0

    lit.seek(0, 0)
    x = lit.readlines()

    i = 0
    while i < len(x):
        if "**" in x[i]:
            pool += 1
            if pool == 1:
                pooltab.append(z)

            y = x[i].split()
            # Extract the literal's value and assign address
            literal_value = y[0].split('=')[1].strip("'")
            opf.write(f"\t (AD,05) \t (DL,02)(C, {literal_value}) \n")
            tmp.write(y[0] + "\t" + str(lc) + "\n")  # Assign address
            lc += 1
        else:
            tmp.write(x[i])
        z += 1
        i += 1

    lit.truncate(0)
    tmp.seek(0, 0)

    for x in tmp:
        lit.write(x)
    tmp.truncate(0)

# handles ORIGIN mnemonic
def ORIGIN(addr):
    global lc
    opf.write("\t (AD,03) \t (C, " + str(addr) + ") \n")
    lc = int(addr)

# handles DS mnemonic
def DS(size):
    global lc
    opf.write("\t (DL,01) \t (C, " + size + ") \n")
    lc = lc + int(size)

# handles DC mnemonic
def DC(value):
    global lc
    opf.write("\t (DL,02) \t (C, " + value + ") \n")
    lc += 1

''' identifies type of operands i.e. registers, literals, symbols and add approprite data in intermediate code 
file, literal table and symbol table as well as pool table. '''

def OTHERS(mnemonic, k):
    global words
    global mnemonics
    global symtab
    global lc, symindex

    z = mnemonics[mnemonic]
    opf.write("\t (" + z[1] + ", " + z[0] + ") \t")
    y = z[-1]

    for i in range(1, y + 1):
        words[k + i] = words[k + i].replace(",", " ")

        if words[k + i] in reg.keys():
            opf.write("(RG, " + str(reg[words[k + i]]) + ")")

        elif "=" in words[k + i]:
            lit.seek(0, 2)  # Seek to the end of the literal file
            lit.write(words[k + i] + "\t ** \n")  # Mark literal with no address
            lit.seek(0, 0)  # Go back to the start of the file
            x = lit.readlines()
            opf.write("(L," + str(len(x)) + ")")  # Reference the literal index

        else:
            if words[k + i] not in symtab.keys():
                symtab[words[k + i]] = (" ** ", symindex)  # Symbol with no address
                opf.write("(S, " + str(symindex) + ")")
                symindex += 1
            else:
                w = symtab[words[k + i]]
                opf.write("(S, " + str(w[-1]) + ")")

    opf.write("\n")
    lc += 1

# idenifies mnemonic and redirects to respective function
def detect_mn(k):
    global words, lc
    if (words[k] == "START"):
        lc= int(words[1])
        opf.write("\t (AD,01) \t (C, " + str(lc) + ') \n')
    elif (words[k] == 'END'):
        END()
    elif (words[k] == "LTORG"):
        LTORG()
    elif (words[k] == "ORIGIN"):
        ORIGIN(words[k + 1])
    elif (words[k] == "DS"):
        DS(words[k + 1])
    elif (words[k] == "DC"):
        DC(words[k + 1])
    # elif(words[k]=="EQU"):
    # EQU(words)
    else:
        OTHERS(words[k], k)
        
    littab()
    pooltab2()
    symbol()


# actual code execution starts from here
symindex = 0
for line in file:
    words = line.split()
    
    if (lc > 0):
        opf.write(str(lc))
    print("\nLocation counter = ", lc)
    print(line)
    print(words)
    k = 0

    if words[0] in mnemonics.keys():
        print("Mnemonic: ", words[0])
        val = mnemonics[words[0]]
        k = 0
        detect_mn(k)
        
    else:
        if len(words) > 1:
            print("Label: ", words[0], "\nMnemonic: ", words[1])
        else:
            print("Label: ", words[0])

        if words[k] not in symtab.keys():
            symtab[words[k]] = (lc, symindex)
            # opf.write("\t (S, " + str(symindex) + ") \t")
            symindex += 1
            symbol()
            
        else:
            # print(words)
            x = symtab[words[k]]
            if x[0] == " ** ":
                print("Yes")
                symtab[words[k]] = (lc, x[1])
            # opf.write("\t(S,"+str(symindex)+")\t")
            symbol()
        k = 1
        detect_mn(k)
        
# print(symtab)
# print(pooltab)
opf.close()
lit.close()
tmp.close()

sym = open("SymTab.txt", "a+")
sym.truncate(0)
for x in symtab:
    sym.write(x + "\t" + str(symtab[x][0]) + "\n")
sym.close()

pool = open("PoolTab.txt", "a+")
pool.truncate(0)
for x in pooltab:
    pool.write(str(x) + "\n")
pool.close()

if os.path.exists("tmp.txt") == True:
    os.remove("tmp.txt")
