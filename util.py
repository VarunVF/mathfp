import os
import sys


def try_read_file(filepath: str):
    with open(filepath) as f:
        return f.read()
