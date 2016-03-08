class ProblemError(Exception):
    """
    """

    def __init__(self):
        pass

    def __str__(self):
        return repr("Tried to redefine of the problem!")


class ProblemTypeError(Exception):
    """
    """

    def __init__(self, desired_type):
        self.desired_type = desired_type

    def __str__(self):
        return repr(
            "Problem type {} not supported!".format(
                self.desired_type
            )
        )


class UndefinedError(Exception):
    """
    """

    def __init__(self):
        pass

    def __str__(self):
        return repr("Not enough information to evaluate!")
