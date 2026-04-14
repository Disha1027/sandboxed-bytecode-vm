"""
You just created:
two queues → q1, q2
rule system → quantum values
counter → for starvation handling later
one VM instance → shared executor
"""

from collections import deque
from .vm import Virtual_Machine


class Scheduler:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

        self.q1_quantum = 5
        self.q2_quantum = 10

        self.cycle_limit = 2
        self.cycle_count = 0

        self.vm = Virtual_Machine()

        self.debug = True

    def load_processes(self, processes):
        for p in processes:
            self.q1.append(p)

    # run ONE process ONCE
    def run_once(self):
        if self.q1:
            process = self.q1.popleft()
            quantum = self.q1_quantum
            queue_name = "Q1"
        elif self.q2:
            process = self.q2.popleft()
            quantum = self.q2_quantum
            queue_name = "Q2"
        else:
            if self.debug:
                print("No processes to run")
            return

        process, used, finished = self.vm.run_step(process, quantum)
        process.ema = 0.5 * used + 0.5 * process.ema

        if self.debug:
            print(f"From {queue_name} → Used: {used}, Finished: {finished}")

        if finished:
            if self.debug:
                print("Process completed and removed")
        else:
            if used == quantum:
                if self.debug:
                    print("Moving to Q2 (CPU-heavy)")
                self.q2.append(process)
            else:
                if self.debug:
                    print("Staying in Q1 (short job)")
                self.q1.append(process)

        self.cycle_count += 1

        if self.cycle_count % self.cycle_limit == 0:
            if self.debug:
                print("Starvation prevention: moving all Q2 → Q1")

            while self.q2:
                self.q1.append(self.q2.popleft())

    # run ALL processes until everything finishes
    def run_all(self):
        while self.q1 or self.q2:
            self.run_once()
