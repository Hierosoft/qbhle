import os
import sys
import unittest

TESTS_MODULE = os.path.dirname(os.path.realpath(__file__))
TESTS = os.path.dirname(TESTS_MODULE)
REPO_DIR = os.path.dirname(TESTS)
TEST_DATA = os.path.join(TESTS_MODULE, "data")

if __name__ == "__main__":
    sys.path.insert(0, REPO_DIR)
    from qbhle.qbparser import run_file


class TestOrderOfOperation(unittest.TestCase):
    def test_order_of_operation(self):
        path = os.path.join(TEST_DATA, "ORDER_OF_OPERATION.BAS")
        run_file(path)


if __name__ == "__main__":
    unittest.main()