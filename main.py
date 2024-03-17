from itertools import product
from copy import deepcopy

# Symbols: ¬ V ∧ → ⇔
# ------------------------
# TODO: Translator from formal logic language to lists
# ------------------------

LETTERS = ["P","Q"]

class Proposition():
    def __init__(self, type:str=None, op1=None, op2=None) -> None:
        self.type = type
        self.op1 = op1
        self.op2 = op2

        if self.type == "atom":
            self.display = self.op1
        elif self.type == "not":
            self.display = f"(¬{self.op1.display})"
        elif self.type == "and":
            self.display = f"({self.op1.display} ∧ {self.op2.display})"
        elif self.type == "or":
            self.display = f"({self.op1.display} V {self.op2.display})"
        elif self.type == "implies":
            self.display = f"({self.op1.display} → {self.op2.display})"
    
    def __repr__(self) -> str:
        return self.display

    # evaluate returns the evaluation of a single interpretation
    # In: interp Out: bool
    def evaluate(self, interp) -> bool:
        if interp == None:
            raise ValueError("Predicate's interpretation is empty")

        if self.type == None:
            raise ValueError("Predicate's type is None")

        if self.type == "atom":
            res = interp[self.op1]
        elif self.type == "and":
            res = self.op1.evaluate(interp) and self.op2.evaluate(interp)
        elif self.type == "or":
            res = self.op1.evaluate(interp) or self.op2.evaluate(interp)
        elif self.type == "not":
            res = not self.op1.evaluate(interp)
        elif self.type == "implies":
            res = (not self.op1.evaluate(interp)) or self.op2.evaluate(interp)
        
        return int(res)
    
    # In: interps Out: bevals
    def evaluate_all(self,interps:list[dict]):
        lis = []

        for interp in interps:
            beval = deepcopy(interp)
            beval["result"] = self.evaluate(beval)
            lis.append(beval)
        
        return lis
        
# In: letters, Out: Interps
def generate_interps(letters:list) -> list[dict]:
    vals = product([0,1], repeat=len(letters))
    lis = []

    for val in vals:
        lis.append({letters[i]:val[i] for i in range(len(letters))})
    
    lis.reverse()

    return lis


def show_table(prop:Proposition, evals:list[dict]) -> None:
    letters = list(evals[0].keys())
    letters.remove("result")

    for l in letters:
        print(f" {l} |", end="")
    print(f" {prop}")

    for eval in evals:
        for l in letters:
            print(f" {eval[l]} |", end="")
        print(f" {eval['result']}")


def build_proposition(proptree:list) -> Proposition:
    if proptree[1] == "atom":
        return Proposition("atom",proptree[0])
    elif proptree[1] in ["not"]:
        return Proposition(proptree[1],build_proposition(proptree[0]))
    elif proptree[1] in ["and","or","implies"]:
        return Proposition(proptree[1],build_proposition(proptree[0]),build_proposition(proptree[2]))

def are_equal(prop1:Proposition, prop2:Proposition, letters:list[str]) -> bool:
    interps = generate_interps(letters)
    return prop1.evaluate_all(interps) == prop2.evaluate_all(interps)

def main():
    proptree = [["P","atom"],"implies",["Q","atom"]]
    proptree2 = [[["P","atom"],"not"],"and",["Q","atom"]]
    prop = build_proposition(proptree)
    prop2 = build_proposition(proptree2)
    interps = generate_interps(LETTERS)
    evals = prop.evaluate_all(interps)
    evals2 = prop2.evaluate_all(interps)
    show_table(prop, evals)
    print()
    show_table(prop2,evals2)
    print()
    print(are_equal(prop,prop2,LETTERS))


if __name__=="__main__":
    main()