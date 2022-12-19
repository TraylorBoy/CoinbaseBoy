"""Tests the CoinbaseBoy Module"""

import os
from coinbaseboy import CBoy
from dotenv import load_dotenv

load_dotenv()

# Tests public methods
def test_one():
    client = CBoy()

    tokens = client.tokens()
    print(tokens)
    assert len(tokens) != 0

    return True


# Tests connection
# def test_?():
#    client = CBoy(silent=False)
#    client.connect(os.getenv("KEY"), os.getenv("SECRET"))


if __name__ == "__main__":
    tests = [test_one]
    i = 1
    for test in tests:
        if test():
            print(f"Test {i} passed")
        else:
            print(f"Test {i} failed")
        i += 1
