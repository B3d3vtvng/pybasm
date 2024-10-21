import itertools

def get_sublists(tup: tuple) -> list[tuple]:
    result = []
    
    for r in range(len(tup) + 1):
        result.extend(itertools.combinations(tup, r))
    
    for r in range(1, len(tup) + 1):
        for combo in itertools.combinations(tup, r):
            result.extend(itertools.permutations(combo))
    
    return result

def get_combinations(tup1: tuple, tup2: tuple) -> list[tuple]:
    return itertools.product(tup1, tup2)