from .errors import VerificationError

"""
verifier.py
Phase 3 : Static Verifier
"""


class Verifier:

    VALID_REGISTERS = {f"R{i}" for i in range(8)}

    def __init__(self, memory_size=256):
        self.memory_size = memory_size

    def validate_register(self, reg, i):
        if reg not in self.VALID_REGISTERS:
            raise VerificationError(
                f"Invalid register at instruction {i}: {reg}"
            )

    def verify(self, program):

        if not program:
            raise VerificationError("Program is empty")

        program_length = len(program)

        # ----------------------------
        # Step 1: Build Control Flow Graph
        # ----------------------------

        successors = {i: [] for i in range(program_length)}

        for i, instruction in enumerate(program):
            opcode = instruction[0]

            if opcode == "JMP":
                _, target = instruction
                if target < 0 or target >= program_length:
                    raise VerificationError(
                        f"Invalid jump target at instruction {i}: {target}"
                    )
                successors[i].append(target)

            elif opcode in {"JZ", "JNZ"}:
                _, reg, target = instruction
                self.validate_register(reg, i)

                if target < 0 or target >= program_length:
                    raise VerificationError(
                        f"Invalid jump target at instruction {i}: {target}"
                    )

                if i + 1 < program_length:
                    successors[i].append(i + 1)
                successors[i].append(target)

            elif opcode == "HALT":
                pass

            else:
                if i + 1 < program_length:
                    successors[i].append(i + 1)

        # ----------------------------
        # Step 2: Termination Check
        # ----------------------------

        reachable = set()
        stack = [0]

        while stack:
            node = stack.pop()
            if node not in reachable:
                reachable.add(node)
                stack.extend(successors[node])

        reverse = {i: [] for i in range(program_length)}
        for src, dests in successors.items():
            for dest in dests:
                reverse[dest].append(src)

        halt_nodes = [
            i for i, instr in enumerate(program) if instr[0] == "HALT"
        ]

        if not halt_nodes:
            raise VerificationError("Program has no HALT instruction")

        can_reach_halt = set()
        stack = halt_nodes.copy()

        while stack:
            node = stack.pop()
            if node not in can_reach_halt:
                can_reach_halt.add(node)
                stack.extend(reverse[node])

        for node in reachable:
            if node not in can_reach_halt:
                raise VerificationError(
                    f"Unbounded loop detected involving instruction {node}"
                )

        # ----------------------------
        # Step 3: Register Initialization (Data-Flow)
        # ----------------------------

        in_states = {i: set() for i in range(program_length)}
        out_states = {i: set() for i in range(program_length)}

        in_states[0] = set()
        worklist = [0]

        while worklist:
            i = worklist.pop()

            current_in = in_states[i].copy()
            current_out = current_in.copy()

            instruction = program[i]
            opcode = instruction[0]

            # -------- Binary Ops --------
            if opcode in {
                "ADD", "SUB", "MUL", "DIV", "MOD",
                "AND", "OR", "XOR",
                "SHL", "SHR",
                "EQ", "LT", "GT", "LE", "GE"
            }:
                _, dest, r1, r2 = instruction

                self.validate_register(dest, i)
                self.validate_register(r1, i)
                self.validate_register(r2, i)

                if r1 not in current_in:
                    raise VerificationError(
                        f"Uninitialized register use at instruction {i}: {r1}"
                    )
                if r2 not in current_in:
                    raise VerificationError(
                        f"Uninitialized register use at instruction {i}: {r2}"
                    )

                current_out.add(dest)

            # -------- Unary Ops --------
            elif opcode in {"NEG", "NOT"}:
                _, dest, r1 = instruction

                self.validate_register(dest, i)
                self.validate_register(r1, i)

                if r1 not in current_in:
                    raise VerificationError(
                        f"Uninitialized register use at instruction {i}: {r1}"
                    )

                current_out.add(dest)

            elif opcode in {"INC", "DEC"}:
                _, reg = instruction

                self.validate_register(reg, i)

                if reg not in current_in:
                    raise VerificationError(
                        f"Uninitialized register use at instruction {i}: {reg}"
                    )

                current_out.add(reg)

            # -------- LOAD --------
            elif opcode == "LOAD":
                _, reg, _ = instruction
                self.validate_register(reg, i)
                current_out.add(reg)

            # -------- LOADM --------
            elif opcode == "LOADM":
                _, reg, mem_index = instruction

                self.validate_register(reg, i)

                if mem_index < 0 or mem_index >= self.memory_size:
                    raise VerificationError(
                        f"Invalid memory read at instruction {i}: {mem_index}"
                    )

                current_out.add(reg)

            # -------- STORE --------
            elif opcode == "STORE":
                _, reg, mem_index = instruction

                self.validate_register(reg, i)

                if reg not in current_in:
                    raise VerificationError(
                        f"Uninitialized register use at instruction {i}: {reg}"
                    )

                if mem_index < 0 or mem_index >= self.memory_size:
                    raise VerificationError(
                        f"Invalid memory write at instruction {i}: {mem_index}"
                    )

            # -------- JZ / JNZ --------
            elif opcode in {"JZ", "JNZ"}:
                _, reg, _ = instruction

                self.validate_register(reg, i)

                if reg not in current_in:
                    raise VerificationError(
                        f"Uninitialized register use at instruction {i}: {reg}"
                    )

            # -------- Safe Instructions --------
            elif opcode in {"JMP", "HALT", "NOP"}:
                pass

            else:
                raise VerificationError(
                    f"Unknown instruction at {i}: {opcode}"
                )

            # ---- Update out state ----
            if current_out != out_states[i]:
                out_states[i] = current_out

                for succ in successors[i]:
                    if not in_states[succ]:
                        new_in = current_out.copy()
                    else:
                        new_in = in_states[succ].intersection(current_out)

                    if new_in != in_states[succ]:
                        in_states[succ] = new_in
                        worklist.append(succ)
