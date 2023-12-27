import re
import sys
import argparse

# Define default conventional types
CONVENTIONAL_TYPES = ["feat", "fix"]

# Define default types
DEFAULT_TYPES = [
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
]

RESULT_SUCCESS = 0
RESULT_FAIL = 1


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"


def main(argv=[]):
    # Allow additiional params to be passed in configuration
    parser = argparse.ArgumentParser(
        prog="pre-commit-conventional-commits", description="Check a git commit message for Conventional Commits formatting."
    )
    parser.add_argument("types", type=str, nargs="*", default=DEFAULT_TYPES, help="Optional list of types to support")
    parser.add_argument("input", type=str, help="A file containing a git commit message")

    if len(argv) < 1:
        argv = sys.argv[1:]

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return RESULT_FAIL

    # Read the actual commit message
    with open(args.input, encoding="utf-8") as f:
        message = f.read()

    if is_commit_conventional(message, args.types):
        return RESULT_SUCCESS
    else:
        print(
            f"""
{Colors.LRED}Bad commit message: {Colors.RESTORE} {message}
{Colors.YELLOW}Your commit message does not follow Conventional Commits formatting.

Conventional Commits start with one of the below types, followed by a colon,
followed by the commit message:{Colors.RESTORE}

{" ".join(convnetional_types_list(args.types))}

{Colors.YELLOW}Good examples:{Colors.RESTORE}
feat: Added new feature
feat(billing): Improved invoices
fix: Fixed speed of execution
feat!: This is breaking change
            """
        )
        return RESULT_FAIL


def regex_types(types):
    """
    Join types with the "|" to form or chain for regex
    """
    return "|".join(types)


def regex_scope():
    """
    Regex for an optional scope (ie. feat(ci))
    """
    return r"(\([\w \/:-]+\))?"


def regex_delimiter():
    """
    Regex string for colon and/or breaking change delimiter
    """
    return r"!?:"


def regex_subject():
    """
    Regex for body, footer and subject
    """
    return r" .+"


def convnetional_types_list(types=[]):
    """
    Returns a final list of Convetional Commits types that is merged from passed types and CONVENTIONAL_TYPES
    """
    if set(types):
        return CONVENTIONAL_TYPES + types

    return CONVENTIONAL_TYPES


def is_commit_conventional(input, types=DEFAULT_TYPES):
    """
    Checks if commit message follows Conventional Commits formatting.
    """

    types = convnetional_types_list(types)
    pattern = f"^({regex_types(types)}){regex_scope()}{regex_delimiter()}{regex_subject()}$"
    regex = re.compile(pattern, re.DOTALL)

    return bool(regex.match(input))


if __name__ == "__main__":
    raise SystemExit(main())
