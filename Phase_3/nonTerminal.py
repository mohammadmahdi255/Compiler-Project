class NonTerminal:

    def __init__(self):
        self.place = None
        self.value = None
        self.code = ""
        self.type = None
        self.nextList = []
        self.trueList = []
        self.falseList = []
        self.instr = None

    def get_value(self):
        return self.place if self.value is None else self.value
