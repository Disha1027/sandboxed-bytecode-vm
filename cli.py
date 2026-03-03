import sys
import ast

from sandbox_vm.vm import Virtual_Machine
from sandbox_vm.verifier import Verifier
from sandbox_vm.errors import VMError, VerificationError


def print_help():
    print("Sandboxed Bytecode VM")
    print("---------------------")
    print("Usage:")
    print("  python3 cli.py help")
    print("  python3 cli.py run <program.bc>")


def load_program_from_file(filename):
    try:
        with open(filename, "r") as f:
            return ast.literal_eval(f.read())
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception:
        print("Error: Invalid bytecode format.")
        sys.exit(1)


def run_program(filename):
    program = load_program_from_file(filename)

    verifier = Verifier()

    try:
        # ---- Static Verification ----
        verifier.verify(program)
        print("Verification successful.\n")

        # ---- Execution ----
        vm = Virtual_Machine()
        vm.load_program(program)
        vm.run()

        print("Execution finished.")
        print("Final Registers:")

        # Print registers in sorted order (R0 → R7)
        for reg in sorted(vm.registers.keys()):
            print(f"  {reg}: {vm.registers[reg]}")

    except VerificationError as e:
        print(f"Verification failed: {e}")
        sys.exit(1)

    except VMError as e:
        print(f"Runtime error: {e}")
        sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "help":
        print_help()

    elif command == "run":
        if len(sys.argv) != 3:
            print("Error: Missing program file.")
            print("Usage: python3 cli.py run <program.bc>")
            sys.exit(1)

        run_program(sys.argv[2])

    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)
