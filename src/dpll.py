"""
"""
import logging
import random
import sys
from errors import *


def dpll(problem, args):
    """ DPLL algorithm.

    Initializes an empty model and starts recursing.

    Args:
        problem(Problem): The problem to solve.
        args: arguments of the DPLL algorithm (None)

    Returns:
        standard_model(list): The achieved model that satisfies the problem.
        or
        False(bool): If there is no possible solution. 
    """

    # Extend recursion limit over to the worst case scenario
    if (sys.getrecursionlimit() < len(problem.symbols) + 20):
        sys.setrecursionlimit(len(problem.symbols) + 20)

    model = {}
    if not dpllRecurse(problem, model):
        return False
    standard_model = []
    for i in range(1, len(problem.symbols)+1):
        if i in model:
            standard_model.append(model[i])
        else:
            standard_model.append(None)
    return standard_model


def dpllRecurse(problem, model={}):
    """ Recursive DPLL

    Args:
        problem(Problem): The problem to solve.
        model(dict): Empty model.

    Returns:
        True(bool): If a solution was found.
        False(bool): If there is no possible solution
    """
    values = []
    for i in range(1, len(problem.symbols)+1):
        if i in model:
            values.append(model[i])
        else:
            values.append(None)

    problem.set(values)

    try:
        # if all clauses are True
        if problem.expression:
            return True

        # if any clause is False
        else:
            return False

    except UndefinedError:
        pass

    # check if there are any pure symbols
    (p, value) = pureSymbol(problem.expression, model)
    if p is not None:
        #logging.debug("pure symbol found! {}:{}".format(p, value))
        model[p] = value

        ret = dpllRecurse(problem, model)
        if not ret:
            # remove assumption from model if it did not work
            del model[p]
        return ret

    # check if there is any unit clause
    (p, value) = unitClause(problem.expression, model)
    if p is not None:
        #logging.debug("unit symbol! {}:{}".format(p, value))
        model[p] = value

        ret = dpllRecurse(problem, model)
        if not ret:
            # remove assumption from model if it did not work
            del model[p]
        return ret

    # look for the first unassigned symbol
    for p in range(1, len(problem.symbols)+1):
        if p not in model:
            break

    #logging.debug("trying a value for {}:{}".format(p, True))
    model[p] = True
    if dpllRecurse(problem, model):
        return True

    #logging.debug("trying a value for {}:{}".format(p, False))
    model[p] = False
    if dpllRecurse(problem, model):
        return True

    # remove assumption from model
    del(model[p])
    return False


def pureSymbol(clauses, model):
    """ Check for pure symbols

    Args:
        clauses(Expression): A propositional sentence.
        model(dict): The model constructed until the moment.

    Returns:
        A tuple with the pure symbol found and its value
    """

    pure = {}
    non_pure = []

    for clause in clauses:
        try:
            # if the clause is true...
            # No need to worry about it anymore.
            if clause:
                continue
        except UndefinedError:
            # There are still symbols left to define in the clause
            for literal in clause:
                if literal.symbol.number in model:
                    # the literal is in the model
                    continue
                if literal.symbol.truth is not None:
                    # the literal already has a value
                    continue
                if literal.symbol in non_pure:
                    # the literal is not pure already
                    continue
                if literal.symbol in pure:
                    # the literal is pure (so far)
                    if pure[literal.symbol] != literal.negation:
                        # the literal has 2 different negation values
                        # it is not pure afterall
                        del pure[literal.symbol]
                        non_pure.append(literal.symbol)
                else:
                    # the literal has not been seen yet, so it is pure
                    pure[literal.symbol] = literal.negation

    if pure:
        symbol, negation = pure.popitem()
        symbol = symbol.number
        value = not negation
    else:
        symbol = None
        value = None

    return (symbol, value)


def unitClause(clauses, model):
    """ Check for Unit Clauses

    Args:
        clauses(Expression): A propositional sentence.
        model(dict): The model constructed until the moment.

    Returns:
        A tuple with the pure symbol found and its value
    """

    for clause in clauses:
        try:
            # if the clause is true...
            # No need to worry about it anymore.
            if clause:
                continue
        except UndefinedError:
            # There are still symbols left to define in the clause
            undefined = checkUnitClause(clause, model)
            if undefined is not None:
                return undefined

    return (None, None)


def checkUnitClause(clause, model):
    """ Check if a clause is a unit clause.

    Args:
        clause(Clause): Clause to check.
        model(dict): The model constructed until the moment.
    """

    undefined = None
    for literal in clause:
        if literal.symbol.number in model:
            # symbol already in the model
            continue
        if literal.symbol.truth is None:
            if undefined is None:
                undefined = (literal.symbol.number, not literal.negation)
            else:
                return None

    return undefined
