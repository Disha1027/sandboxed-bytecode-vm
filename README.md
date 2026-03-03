# Sandboxed Bytecode VM with Static Safety Verifier

## Overview

This project implements a sandboxed virtual machine that executes custom bytecode programs only after static safety verification.

Execution flow:

Program → Verifier → Virtual Machine → Output

Unsafe programs are rejected before execution.

---

## Features

- 8 general-purpose registers (R0–R7)
- Fixed memory size (256 cells)
- Arithmetic operations
- Logical operations
- Conditional and unconditional jumps
- Static control-flow analysis
- Static termination detection
- Static register initialization analysis
- Memory bounds verification

---

## Safety Guarantees

The verifier rejects programs that:

- Contain invalid jump targets
- Access memory out of bounds
- Use uninitialized registers
- Contain unbounded loops
- Do not contain HALT

The VM guarantees:

- No crashes on invalid input
- Clean runtime error handling

---

## How to Run

```bash
python3 cli.py help
python3 cli.py run examples/safe.bc


## Example Expected output
Verification successful.

Execution finished.
Final Registers:
R7: 60300