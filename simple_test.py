import sys
from pathlib import Path


def hello_world():
    message = "Hello, World!"
    return message


class TestClass:
    def __init__(self):
        self.value = 42

    def get_value(self):
        return self.value


if __name__ == "__main__":
    obj = TestClass()
    print(obj.get_value())
    print(hello_world())
