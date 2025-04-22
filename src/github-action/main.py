#!/usr/bin/env python3

import os
import sys

def get_argument(arg_position: int, env_name: str) -> str:
    """
      Helper function to get the program arguments from the commandline or the environment

      Args:
          arg_position: Index in sys.argv
          env_name: Name of the environment variable
    """
    if len(sys.argv) > arg_position:
        return sys.argv[arg_position]

    return os.getenv(env_name)


if __name__ == '__main__':
    argument: str = get_argument(1, "INPUT_ARGUMENT")
