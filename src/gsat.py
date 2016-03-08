"""
"""
import random


def gsat(problem, args):
    """ GSAT algorithm.

    Args:
        problem(Problem): The problem to solve.
        args: arguments of the GSAT algorithm:
            max_restarts(int): Maximum number of restarts.
            max_climbs(int): Maximum number of climbs per run.

    Returns:
        A(list): The achieved model that satisfies the problem.
        or
        None: If no solution was found. 
    """

    max_restarts = args.max_restarts
    max_climbs = args.max_climbs

    # Try to solve the problem with a random truth assignment max_restarts
    #times
    for i in range(max_restarts):
        # Random truth assignment to all the symbols in the problem
        A = [bool(random.getrandbits(1)) for x in range(problem.variables)]
        for j in range(max_climbs):
            problem.set(A)
            # Stop if A is the solution
            if problem.expression:
                return A
            A = choose_successor(problem, A)

    return None


def choose_successor(problem, A):
    """ Chooses the best or one of the best truth assignments
        that maximizes the number of satisfied clauses.

    Args:
        problem(Problem): The problem to solve.
        A(list): The model achieved so far.

    Returns:
        A(list): The new and improved model.
    """

    best_score = 0
    best_solutions = []

    for var in range(len(A)):
        B = A
        B[var] = not A[var]
        problem.set(A)
        score = problem.expression.score()

        if score == best_score:
            best_solutions.append(var)

        if score > best_score:
            best_score = score
            best_solutions = [var]

    chosen = random.choice(best_solutions)
    A[chosen] = not A[chosen]
    return A
