from .errors import VMError


class Virtual_Machine:

    VALID_REGISTERS = {f"R{i}" for i in range(8)}

    def __init__(self):
        self.registers = {reg: 0 for reg in self.VALID_REGISTERS}
        self.memory = [0] * 256

    def validate_register(self, reg):
        if reg not in self.VALID_REGISTERS:
            raise VMError(f"Invalid register: {reg}")

    def load_program(self, program):
        self.program = program
        self.ip = 0

    def run(self):
        while True:

            if self.ip < 0 or self.ip >= len(self.program):
                raise VMError(f"Instruction pointer out of bounds: {self.ip}")

            instruction = self.program[self.ip]
            opcode = instruction[0]

            # ---------------- Arithmetic (Binary) ----------------
            if opcode in {"ADD", "SUB", "MUL", "DIV", "MOD",
                          "AND", "OR", "XOR",
                          "SHL", "SHR",
                          "EQ", "LT", "GT", "LE", "GE"}:

                _, dest, r1, r2 = instruction

                self.validate_register(dest)
                self.validate_register(r1)
                self.validate_register(r2)

                a = self.registers[r1]
                b = self.registers[r2]

                if opcode == "ADD":
                    self.registers[dest] = a + b
                elif opcode == "SUB":
                    self.registers[dest] = a - b
                elif opcode == "MUL":
                    self.registers[dest] = a * b
                elif opcode == "DIV":
                    if b == 0:
                        raise VMError("Division by zero")
                    self.registers[dest] = a // b
                elif opcode == "MOD":
                    if b == 0:
                        raise VMError("Modulo by zero")
                    self.registers[dest] = a % b
                elif opcode == "AND":
                    self.registers[dest] = a & b
                elif opcode == "OR":
                    self.registers[dest] = a | b
                elif opcode == "XOR":
                    self.registers[dest] = a ^ b
                elif opcode == "SHL":
                    self.registers[dest] = a << b
                elif opcode == "SHR":
                    self.registers[dest] = a >> b
                elif opcode == "EQ":
                    self.registers[dest] = int(a == b)
                elif opcode == "LT":
                    self.registers[dest] = int(a < b)
                elif opcode == "GT":
                    self.registers[dest] = int(a > b)
                elif opcode == "LE":
                    self.registers[dest] = int(a <= b)
                elif opcode == "GE":
                    self.registers[dest] = int(a >= b)

            # ---------------- Unary ----------------
            elif opcode in {"NEG", "NOT"}:
                _, dest, r1 = instruction
                self.validate_register(dest)
                self.validate_register(r1)

                val = self.registers[r1]
                self.registers[dest] = -val if opcode == "NEG" else ~val

            elif opcode in {"INC", "DEC"}:
                _, reg = instruction
                self.validate_register(reg)

                if opcode == "INC":
                    self.registers[reg] += 1
                else:
                    self.registers[reg] -= 1

            # ---------------- Memory ----------------
            elif opcode == "LOAD":
                _, reg, value = instruction
                self.validate_register(reg)
                self.registers[reg] = value

            elif opcode == "LOADM":
                _, reg, mem_index = instruction
                self.validate_register(reg)

                if mem_index < 0 or mem_index >= len(self.memory):
                    raise VMError(f"Memory access out of bounds: {mem_index}")

                self.registers[reg] = self.memory[mem_index]

            elif opcode == "STORE":
                _, reg, mem_index = instruction
                self.validate_register(reg)

                if mem_index < 0 or mem_index >= len(self.memory):
                    raise VMError(f"Memory access out of bounds: {mem_index}")

                self.memory[mem_index] = self.registers[reg]

            # ---------------- Control Flow ----------------
            elif opcode == "JMP":
                _, target = instruction
                if target < 0 or target >= len(self.program):
                    raise VMError(f"Invalid jump target: {target}")
                self.ip = target
                continue

            elif opcode in {"JZ", "JNZ"}:
                _, reg, target = instruction
                self.validate_register(reg)

                condition = (self.registers[reg] == 0) if opcode == "JZ" else (
                    self.registers[reg] != 0)

                if condition:
                    if target < 0 or target >= len(self.program):
                        raise VMError(f"Invalid jump target: {target}")
                    self.ip = target
                    continue

            elif opcode == "NOP":
                pass

            elif opcode == "HALT":
                break

            else:
                raise VMError(f"Unknown instruction: {opcode}")

            self.ip += 1

    def run_step(self, process, instruction_limit):
        instructions_executed = 0

        while instructions_executed < instruction_limit:

            if process.finished:
                break

            if process.ip < 0 or process.ip >= len(process.program):
                raise VMError(
                    f"Instruction pointer out of bounds: {process.ip}")

            instruction = process.program[process.ip]
            opcode = instruction[0]

            # ---------------- Arithmetic (Binary) ----------------
            if opcode in {"ADD", "SUB", "MUL", "DIV", "MOD",
                          "AND", "OR", "XOR",
                          "SHL", "SHR",
                          "EQ", "LT", "GT", "LE", "GE"}:

                _, dest, r1, r2 = instruction

                self.validate_register(dest)
                self.validate_register(r1)
                self.validate_register(r2)

                a = process.registers[r1]
                b = process.registers[r2]

                if opcode == "ADD":
                    process.registers[dest] = a + b
                elif opcode == "SUB":
                    process.registers[dest] = a - b
                elif opcode == "MUL":
                    process.registers[dest] = a * b
                elif opcode == "DIV":
                    if b == 0:
                        raise VMError("Division by zero")
                    process.registers[dest] = a // b
                elif opcode == "MOD":
                    if b == 0:
                        raise VMError("Modulo by zero")
                    process.registers[dest] = a % b
                elif opcode == "AND":
                    process.registers[dest] = a & b
                elif opcode == "OR":
                    process.registers[dest] = a | b
                elif opcode == "XOR":
                    process.registers[dest] = a ^ b
                elif opcode == "SHL":
                    process.registers[dest] = a << b
                elif opcode == "SHR":
                    process.registers[dest] = a >> b
                elif opcode == "EQ":
                    process.registers[dest] = int(a == b)
                elif opcode == "LT":
                    process.registers[dest] = int(a < b)
                elif opcode == "GT":
                    process.registers[dest] = int(a > b)
                elif opcode == "LE":
                    process.registers[dest] = int(a <= b)
                elif opcode == "GE":
                    process.registers[dest] = int(a >= b)

            # ---------------- Unary ----------------
            elif opcode in {"NEG", "NOT"}:
                _, dest, r1 = instruction
                self.validate_register(dest)
                self.validate_register(r1)

                val = process.registers[r1]
                process.registers[dest] = -val if opcode == "NEG" else ~val

            elif opcode in {"INC", "DEC"}:
                _, reg = instruction
                self.validate_register(reg)

                if opcode == "INC":
                    process.registers[reg] += 1
                else:
                    process.registers[reg] -= 1

            # ---------------- Memory ----------------
            elif opcode == "LOAD":
                _, reg, value = instruction
                self.validate_register(reg)
                process.registers[reg] = value

            elif opcode == "LOADM":
                _, reg, mem_index = instruction
                self.validate_register(reg)

                if mem_index < 0 or mem_index >= len(process.memory):
                    raise VMError(f"Memory access out of bounds: {mem_index}")

                process.registers[reg] = process.memory[mem_index]

            elif opcode == "STORE":
                _, reg, mem_index = instruction
                self.validate_register(reg)

                if mem_index < 0 or mem_index >= len(process.memory):
                    raise VMError(f"Memory access out of bounds: {mem_index}")

                process.memory[mem_index] = process.registers[reg]

            # ---------------- Control Flow ----------------
            elif opcode == "JMP":
                _, target = instruction
                if target < 0 or target >= len(process.program):
                    raise VMError(f"Invalid jump target: {target}")
                process.ip = target
                instructions_executed += 1
                continue

            elif opcode in {"JZ", "JNZ"}:
                _, reg, target = instruction
                self.validate_register(reg)

                condition = (process.registers[reg] == 0) if opcode == "JZ" else (
                    process.registers[reg] != 0
                )

                if condition:
                    if target < 0 or target >= len(process.program):
                        raise VMError(f"Invalid jump target: {target}")
                    process.ip = target
                    instructions_executed += 1
                    continue

            elif opcode == "NOP":
                pass

            elif opcode == "HALT":
                process.finished = True
                instructions_executed += 1
                break

            else:
                raise VMError(f"Unknown instruction: {opcode}")

            process.ip += 1
            instructions_executed += 1

        return process, instructions_executed, process.finished
