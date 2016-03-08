"""
"""
from errors import *


class Problem(object):
    """ A SAT problem.

    Attributes:
        expression(Expression): Propositional sentence to evaluate.
        format(str): Sentence format (always CNF)
        variables(str): Number of variables
        clauses(str): Number of clauses
        symbols(list): List of proposition symbols (1:variables)
        filename(str): DIMACS input file.
    """

    P_TYPES = [
        "cnf",
        # "sat"
    ]

    def __init__(self, filename):
        self.expression = Expression()
        self.format = None
        self.variables = None
        self.clauses = None
        self.symbols = None
        self.filename = filename

        f = open(self.filename, 'r')

        cur_clause = Clause()

        for line in f:
            line = line.replace("\n", "")
            params = line.split()

            # Skip empty lines
            if not params:
                pass

            # Skip comments
            elif params[0] == 'c':
                pass

            # Problem definition
            elif params[0] == 'p':
                if self.format:
                    raise ProblemError()
                elif params[1] not in Problem.P_TYPES:
                    raise ProblemTypeError(params[1])
                self.define(*params[1:])

            # Problem statement
            elif (
                params[0].isdigit() or
                (params[0].startswith("-") and params[0][1:].isdigit())
            ):
                for var in params:
                    if var == "0":
                        if len(cur_clause):
                            self.expression.append(cur_clause)
                            cur_clause = Clause()
                    else:
                        cur_clause.append(
                            Literal(
                                int(var),
                                self.symbols[abs(int(var))]
                            )
                        )

        if len(cur_clause) > 0:
            self.expression.append(cur_clause)

    def define(self, format, variables, clauses):
        """ Define the problem.

        Args: 
            format(str): Sentence format (always CNF).
            variables(str): Number of variables.
            clauses(str): Number of clauses.
        """

        self.format = format
        self.variables = int(variables)
        self.clauses = int(clauses)

        self.symbols = {
            i: Symbol(i) for i in range(1, self.variables + 1)
        }

    def set(self, values):
        """ Set the values of the symbols.

        Args:
            values(list): Model with truth assignments to the symbols.
        """
        for i in range(len(values)):
            self.symbols[i+1].set(values[i])

    def setSymbol(self, index, value):
        """ Set the value of one symbol.

        Args:
            index(int): Index of the symbol.
            value(Bool): Truth value of the symbol.
        """

        self.symbols[index].set(value)

    def get(self):
        """ Gets the current value for each symbol.

        Returns:
            List with the current truth values for all the symbols.
        """

        return [
            True if self.symbols[i+1]
            else False
            for i in range(self.variables)
        ]

    def checkConsistency(self):
        """ Check if the problem is well defined.

        Returns:
            Boolean.
        """

        return len(self.expression) != self.clauses

    def writeOutput(self, alg, result):
        """ Write output file

        Args:
            alg(str): Name of the used SAT solving algorithm
            result(list): List with the achieved model (solution).
        """

        dict_solution = {
            True: 1,
            False: 0,
            None: -1,
        }

        # output file will be named equal to the input file with
        # .out extension
        out = open(self.filename[:self.filename.rfind('.')]+".out", 'w')

        # Comments
        out.write(
            'c\n' +
            'c Used algorithm: ' + alg + '\n' +
            'c\n'
        )

        if result is False:
            out.write('c ' + 'Unsatisfiable Problem' + '\n')
        elif result is None:
            out.write('c ' + 'No solution was found' + '\n')
        else:
            out.write('c ' + 'Satisfiable Problem' + '\n')

        # Solution Line
        if result:
            k = True
        else:
            k = result
        out.write('s ' + self.format + ' ' + str(dict_solution[k]))
        out.write(' ' + str(self.variables) +
        ' ' + str(self.clauses) + '\n')

        # Variable Line        
        if result:
            out.write('v ')
            for i in range(0, len(result)):
                if result[i] is True:
                    out.write(str(i+1) + ' ')
                elif result[i] is False:
                    out.write('-' + str(i+1) + ' ')


    def __str__(self):
        ret = ""
        for clause in self.expression:
            if ret:
                ret += "∧"

            ret += str(clause)
        return ret

    def __bool__(self):
        if self.expression:
            return True
        else:
            return False


class Expression(list):
    """ A Propositional Sentence in CNF.

    Conjunction of clauses.

    Attributes:
        None
    """

    def __bool__(self):
        n = False
        for clause in self:
            try:
                if not clause:
                    return False
            except UndefinedError:
                n = True
        if n:
            raise UndefinedError
        return True

    def score(self):
        """ Calculates the expression's score
            (number of satisfied clauses)
        """

        s = 0
        for clause in self:
            if clause:
                s += 1
        return s


class Clause(list):
    """ A Clause.

    Disjunction of literals.

    Attributes:
        None
    """

    def __bool__(self):
        n = False
        for literal in self:
            try:
                if literal:
                    return True
            except UndefinedError as e:
                n = True
        if n:
            raise UndefinedError

        return False

    def __str__(self):
        c = ""
        for var in self:
            if c:
                c += "∨"
            c += str(var)
        return "({})".format(c)


class Literal(object):
    """ A Literal.

    Proposition symbol or its negation.

    Attributes:
        symbol(Symbol): A symbol.
        negation(Bool): Its truth value.
    """
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    def __init__(self, value, symbol):
        self.symbol = symbol
        self.negation = value < 0

    def __bool__(self):
        if self.symbol.truth is None:
            raise UndefinedError
        if self.negation:
            return not bool(self.symbol)
        else:
            return bool(self.symbol)

    def __str__(self):
        return "x{}{}".format(
            "\u0304" if self.negation else "",
            str(self.symbol).translate(Literal.SUB)
        )


class Symbol(object):
    """ A Symbol.

    Attributes:
        number(int): Index of the symbol from 1 to 'variables'.
        truth(Bool): Truth value of the symbol according to the
                    model at the moment. Starts with None.
    """

    def __init__(self, number, truth=None):
        self.number = number
        self.truth = truth

    def set(self, value):
        """
        """
        self.truth = value

    def flip(self):
        """
        """

        self.truth = not self.truth

    def __str__(self):
        return str(self.number)

    def __bool__(self):
        return self.truth
