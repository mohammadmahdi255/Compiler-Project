class Quadruple:

    def __init__(self, result, arg1, op, arg2=None):
        self.result = result
        self.arg1 = arg1
        self.op = op
        self.arg2 = arg2

    def __str__(self) -> str:
        return "{} {} {} {}".format(self.result, self.arg1, self.op, self.arg2)
