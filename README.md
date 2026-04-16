# Sandboxed Bytecode VM with Scheduler

## Overview
This project implements a sandboxed virtual machine that executes custom bytecode programs only after static safety verification. It also supports multiple programs using a scheduler.

Execution flow:

Program(s) → Verifier → Process → Scheduler → Virtual Machine → Output

Unsafe programs are rejected before execution.

---

## Features
- 8 general-purpose registers (R0–R7)
- Fixed memory size (256 cells)
- Arithmetic operations (ADD, SUB, MUL, DIV, MOD)
- Logical operations (AND, OR, XOR, NOT)
- Bitwise shift operations (SHL, SHR)
- Comparison operations (EQ, LT, GT, LE, GE)
- Conditional and unconditional jumps (JMP, JZ, JNZ)
- Static control-flow analysis
- Static termination detection
- Static register initialization analysis
- Memory bounds verification
- Multi-level feedback queue scheduler (Q1, Q2)
- Time-sliced execution of multiple programs
- Starvation prevention
- EMA (Exponential Moving Average) tracking

---

## Safety Guarantees

The verifier rejects programs that:
- Contain invalid jump targets
- Access memory out of bounds
- Use uninitialized registers
- Contain unbounded loops
- Do not contain a HALT instruction

The VM guarantees:
- No crashes on invalid input
- Clean runtime error handling

---

## Project Structure

sandbox_vm/
vm.py
verifier.py
process.py
scheduler.py
errors.py

tests/
test_vm.py
test_verifier.py
test_scheduler.py

examples/
safe.bc
uninit.bc
unsafe_loop.bc
long1.bc
long2.bc

cli.py
README.md


---

## How to Run

### Single Program
```bash
python3 cli.py run examples/safe.bc

### Multiple Programs (with scheduling)
```bash
python3 cli.py run examples/safe.bc examples/safe.bc

### Run tests

python3 -m unittest

### Example Outputs

examplesexamples/safe.bc: Verification successful

From Q1 → Used: 5, Finished: True
Process completed and removed

Execution finished.

Process 0:
  R0: 0
  R1: 5
  R2: 7
  R3: 12
  R4: 84
  R5: 0
  R6: 0
  R7: 0/safe.bc: Verification successful

From Q1 → Used: 5, Finished: True
Process completed and removed

Execution finished.

Process 0:
  R0: 0
  R1: 5
  R2: 7
  R3: 12
  R4: 84
  R5: 0
  R6: 0
  R7: 0

---

### Key Concepts

Verifier: Performs static analysis to ensure safety before execution
Virtual Machine (VM): Executes bytecode instructions
Process: Encapsulates execution state (registers, memory, instruction pointer)
Scheduler: Manages multiple processes using a multi-level feedback queue

### Summary

This project demonstrates:

Safe execution of low-level programs
Static program analysis
Virtual machine design
Basic operating system scheduling concepts


