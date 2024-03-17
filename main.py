from itertools import product

LETTERS = ["P","Q","R"]

class Proposition():
    def __init__(self, type:str=None, op1=None, op2=None) -> None:
        self.type = type
        self.op1 = op1
        self.op2 = op2

        if self.type == "atom":
            self.display = self.op1
        elif self.type == "not":
            self.display = f"¬({self.op1})"
        elif self.type == "and":
            self.display = f"({self.op1.display} ∧ {self.op2.display})"
        elif self.type == "or":
            self.display = f"({self.op1.display} V {self.op2.display})"
    
    def __repr__(self) -> str:
        return self.display

    # evaluate returns the evaluation of a single interpretation
    def evaluate(self, interp) -> bool:
        if interp == None:
            raise TypeError("Predicate's interpretation is empty")

        if self.type == None:
            raise ValueError("Predicate's type is None")

        if self.type == "atom":
            return interp[self.op1]
        elif self.type == "and":
            return self.op1.evaluate(interp) and self.op2.evaluate(interp)
        elif self.type == "or":
            return self.op1.evaluate(interp) or self.op2.evaluate(interp)
        elif self.type == "not":
            return not self.op1.evaluate(interp)
        

def generate_list_of_interps(letters:list) -> list[dict]:
    vals = product([0,1], repeat=len(letters))
    lis = []

    for val in vals:
        lis.append({letters[i]:val[i] for i in range(len(letters))})
    
    lis.reverse()

    return lis
"""
This function is not implemented as it should be. Instead of generating interpretations, it
should be given a list with the desired interpretations to display.

def show_table(prop:Proposition, letters:list[str]):
    abcs = generate_abc(letters)

    for l in letters:
        print(f" {l} |", end="")
    print(f" {prop}")

    for abc in abcs:
        for l in letters:
            print(f" {abc[l]} |", end="")
        print(f" {prop.evaluate(abc)}")
"""

# TODO: Proposition generator, instead of the shit that's in main()
# [[["P","atom"],or,["Q","atom"]],"and",[["R","atom"],"not"]] = ((P V Q) ∧ ¬(R))

def build_proposition(proptree:list) -> Proposition:
    if proptree[1] == "atom":
        return Proposition("atom",proptree[0])
    elif proptree[1] == "not":
        return Proposition("not",build_proposition(proptree[0]))
    elif proptree[1] == "and":
        return Proposition("and",build_proposition(proptree[0]),build_proposition(proptree[2]))
    elif proptree[1] == "or":
        return Proposition("or",build_proposition(proptree[0]),build_proposition(proptree[2]))

def main():
    proptree = [[["P","atom"],"or",["Q","atom"]],"and",[["R","atom"],"not"]]
    prop = build_proposition(proptree)
    print(prop)

if __name__=="__main__":
    main()