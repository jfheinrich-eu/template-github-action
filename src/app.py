#!/usr/bin/env python
"""Main entrypoint for the action"""
import sys

from github_action import GitHubAction
sys.path.append('.')


def main() -> None:  # pragma no cover
    print(GitHubAction.get_info())


if __name__ == "__main__":  # pragma no cover
    main()
