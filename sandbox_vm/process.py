class Process:
    def __init__(self, program):
        self.program = program
        self.ip = 0
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.memory = [0] * 256
        self.finished = False
        self.ema = 0
