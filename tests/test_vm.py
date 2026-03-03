import unittest
from sandbox_vm.vm import Virtual_Machine


class TestVM(unittest.TestCase):

    def test_add(self):
        program = [
            ("LOAD", "R1", 10),
            ("LOAD", "R2", 20),
            ("ADD", "R3", "R1", "R2"),
            ("HALT",)
        ]

        vm = Virtual_Machine()
        vm.load_program(program)
        vm.run()

        self.assertEqual(vm.registers["R3"], 30)


if __name__ == "__main__":
    unittest.main()
