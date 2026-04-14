import sys
import ast

from sandbox_vm.process import Process
from sandbox_vm.scheduler import Scheduler
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


def run_programs(filenames):
    verifier = Verifier()
    processes = []

    for file in filenames:
        try:
            program = load_program_from_file(file)
            verifier.verify(program)
            print(f"{file}: Verification successful")

            p = Process(program)
            processes.append(p)

        except VerificationError as e:
            print(f"{file}: Verification failed → {e}")

        except Exception as e:
            print(f"{file}: Error → {e}")

    if not processes:
        print("No valid programs to run")
        return

    scheduler = Scheduler()
    scheduler.load_processes(processes)
    scheduler.run_all()

    print("\nExecution finished.")
    print("Final Registers:")

    for i, p in enumerate(processes):
        print(f"\nProcess {i}:")
        for reg in sorted(p.registers.keys()):
            print(f"  {reg}: {p.registers[reg]}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "help":
        print_help()

    elif command == "run":
        if len(sys.argv) < 3:
            print("Error: Missing program file(s).")
            print("Usage: python3 cli.py run <program1.bc> <program2.bc> ...")
            sys.exit(1)

        run_programs(sys.argv[2:])

    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)
