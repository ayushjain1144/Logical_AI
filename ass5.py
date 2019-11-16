from logic import * 



def form_CNF(fname):

    fp = open(fname)
    fout = open(f"KB-{fname}", 'w')
    clauses = []
    logic_kb = PropKB()

    for line in fp.readlines():

        if line:    
            try:
                ex = expr(line)
                clauses.append(ex)
                logic_kb.tell(ex)
                print(ex)
                #fout.write(ex)

            except Exception as e:
                print(str(e))
                print(line)


    
    print(logic_kb.clauses)

    for rule in logic_kb.clauses:
        fout.write(str(rule) + "\n")

    fp.close()
    fout.close()

def form_KB(fname):

    fp = open(fname)
    fout = open(f"KB-{fname}", 'w')
    clauses = []

    for line in fp.readlines():

        if line:    
            try:
                ex = expr(line)
                clauses.append(ex)
                #logic_kb.tell(ex)
                print(ex)
                #fout.write(ex)

            except Exception as e:
                print(str(e))
                print(line)

    logic_kb = FolKB(clauses)
    print(logic_kb.clauses)
    return logic_kb


def query(fname):
    logic_kb = form_KB('ruleFile1.txt')

    fp = open(fname)

    for line in fp.readlines(): 
        answer = fol_fc_ask(logic_kb, expr(line))
        q = list(answer)
        

        if not q:
            print(False)
        elif q and not q[0]:
            print(True)
        else:
            
            print(q[0])   
            
        #print(list(answer)) 

        #answer2 = pl_resolution(logic_kb, expr(line))
        #print(answer2)



#form_KB('ruleFile1.txt')
query('query1.txt')