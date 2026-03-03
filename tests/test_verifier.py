import unittest
from sandbox_vm.verifier import Verifier
from sandbox_vm.errors import VerificationError


class TestVerifier(unittest.TestCase):

    def test_safe_program(self):
        program = [
            ("LOAD", "R1", 5),
            ("LOAD", "R2", 6),
            ("ADD", "R3", "R1", "R2"),
            ("HALT",)
        ]

        verifier = Verifier()
        verifier.verify(program)

    def test_uninitialized(self):
        program = [
            ("ADD", "R1", "R2", "R3"),
            ("HALT",)
        ]

        verifier = Verifier()

        with self.assertRaises(VerificationError):
            verifier.verify(program)


if __name__ == "__main__":
    unittest.main()
