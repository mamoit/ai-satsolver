"""
"""
import random


def walksat(problem, args):
    """ Walksat algorithm.

    Args:
        problem(Problem): The problem to solve.
        args: arguments of the WalkSAT algorithm:
            p(float): Probability of picking a symbol at random
            max_flips(int): Maximum number of flips

    Returns:
        A list with the achieved model that satisfies the problem.
        or
        None: If no solution was found. 
    """

    p = args.p
    max_flips = args.max_flips

    # Random truth assignment to all the symbols in the problem
    A = [bool(random.getrandbits(1)) for x in range(problem.variables)]
    problem.set(A)

    # Try to solve the problem up to a maximum number of flips
    for i in range(max_flips):
        # Stop if problem is solved
        if problem.expression:
            return problem.get()

        # Flip a symbol
        flip_symbol(problem, p)

    # No solution was found (this doesn't mean it doesn't exist!)
    return None


def flip_symbol(problem, p):
    """ Flips, with probability p, the truth value of a randomly 
        selected symbol or flips a symbol that maximizes the
        number of satisfied clauses.

    Args:
        problem(Problem): The problem to solve.
        p(float): Probability of picking a symbol at random and flip it.
    """

    # Find all unsatisfied clauses
    unsatisfied_clauses = []
    for clause in problem.expression:
        if not clause:
            unsatisfied_clauses.append(clause)

    # From the unsatisfied clauses pick one at random
    clause = random.choice(unsatisfied_clauses)

    # with a certain probability, just flip a random symbol from that clause
    if random.random() < p:
        random.choice(clause).symbol.flip()
        return

    # find the best symbols to flip in that clause
    best_score = 0
    best_flips = []

    for literal in clause:
        # extract the symbol from the literal
        symbol = literal.symbol

        # flip the symbol
        symbol.flip()

        # calculate the score
        score = problem.expression.score()

        if score == best_score:
            best_flips.append(symbol)
        elif score > best_score:
            best_score = score
            best_flips = [symbol]

        # undo flip
        symbol.flip()

    # flip one of the best symbols at random
    random.choice(best_flips).flip()
