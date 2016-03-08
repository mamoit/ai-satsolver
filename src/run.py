#!/usr/bin/python3

from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import logging
import sys

from dimacs import *
from gsat import gsat
from walksat import walksat
from dpll import dpll


# Dictionary for the implemented algorithms
ALGORITHMS = {
    "gsat": {
        "function": gsat,
        "help": "GSAT algorithm",
        "args": [
            {
                "name": "max_restarts",
                "type": int,
                "help": "Maximum number of restarts"
            },
            {
                "name": "max_climbs",
                "type": int,
                "help": "Maximum number of climbs per run"
            }
        ]
    }, "walksat": {
        "function": walksat,
        "help": "WalkSAT algorithm",
        "args": [
            {
                "name": "p",
                "type": float,
                "help": "Probability of picking a symbol at random"
            },
            {
                "name": "max_flips",
                "type": int,
                "help": "Maximum number of symbols to flip"
            }
        ]
    }, "dpll": {
        "function": dpll,
        "help": "DPLL algorithm",
        "args": [
        ]
    }
}


class ArgParser(ArgumentParser):
    """ Modify ArgumentParser error handling behaviour """

    def error(self, message):
        """ Writes the error message in arguments handling

        Args:
            message (str): Error message.
        """

        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    """ Main function of the program.

    Parses arguments and invokes the processing functions.
    """

    # Parse the arguments
    parser = ArgParser(description="", epilog="",
                       formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "dimacs",
        help="file with the satisfiability problem (in DIMACS format)"
    )

    # Mandatory to specify one and only one algorithm.
    subparsers = parser.add_subparsers(title="algorithms", dest="algorithm")
    subparsers.required = True

    for algorithm in ALGORITHMS:
        subparser = subparsers.add_parser(
            algorithm,
            help=ALGORITHMS[algorithm]["help"]
        )
        for var in ALGORITHMS[algorithm]["args"]:
            subparser.add_argument(
                var["name"],
                type=var["type"],
                help=var["help"]
            )
        subparser.set_defaults(func=ALGORITHMS[algorithm]["function"])

    parser.add_argument("-pp", "--print-problem",
                        action="store_true",
                        help="Print the problem")
    parser.add_argument("-ps", "--print-solution",
                        action="store_true",
                        help="Print solution to stdout")
    parser.add_argument("-l", "--logfile",
                        help="file where the log is to be written to (instead \
                            of the console)")
    parser.add_argument("-v", "--verbosity",
                        help="verbosity", action="count",
                        default=0)
    parser.add_argument("-r", "--runs",
                        help="number of runs",
                        type=int,
                        default=1)
    parser.add_argument("-ns", "--no-sol",
                        help="do not write solution file (to measure \
                        algorithm performance)",
                        action="store_false")

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        filename=args.logfile,
                        level=10*(
                            (4-args.verbosity) if args.verbosity < 4 else 1
                        ))

    # Parses the SAT problem file (DIMACS format)
    logging.debug("Parsing file {}".format(args.dimacs))
    p = Problem(args.dimacs)
    logging.debug("Done parsing file")

    if args.print_problem:
        logging.debug("Printing problem")
        print(p)
        logging.debug("Done printing problem")

    # Applies an algorithm to solve the SAT problem
    logging.debug("Solving problem")
    result = args.func(p, args)
    logging.debug("Problem solved")

    if args.print_solution:
        if result is None:
            print("No conclusion reached...")
        elif result:
            print("Solution found!")
            print(result)
        else:
            print("Problem not satisfiable!")

    # Writes the output file (DIMACS format)
    logging.debug("Writing output file")
    p.writeOutput(args.algorithm, result)
    logging.debug("Output file written")

if __name__ == '__main__':
    main()
